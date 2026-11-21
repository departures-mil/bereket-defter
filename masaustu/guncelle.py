"""Uygulama içi güncelleme (ESITLEME_SPEC.md §8).

Yeni sürüm GitHub deposundaki "guncelleme/{kanal}.json" bildirgesinden okunur; paket (app klasörünün ZIP'i)
"guncelleme/" altındaki dosyadır ve sha256 ile doğrulanır. Kurulum yalnızca "app"
klasöründeki program dosyalarını yeniler; "Veriler" (kayıtlar, dekontlar, ayarlar) ve "runtime" hiç değişmez.
"""
import time
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import zipfile

# Güncellemeler GitHub'dan gelir (Firebase yalnızca canlı kayıt eşitlemesi içindir).
GITHUB_RAW = "https://raw.githubusercontent.com/departures-mil/bereket-defter/main"
CHANNEL = "masaustu"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROTECTED = ("Veriler", "runtime")  # pakette bunlar olamaz

# Güncelleme ayarları (⚙ Ayarlar). Veriler klasöründe ayrı dosyada durur; güncelleme ona dokunmaz.
# Yeni sürüm yalnızca program açılışında denetlenir; burada sadece bildirim açık/kapalı tutulur.
SETTINGS_FILE = "guncelleme_ayar.json"
DEFAULT_SETTINGS = {"notify": True}


def load_settings(data_dir):
    out = dict(DEFAULT_SETTINGS)
    try:
        with open(os.path.join(data_dir, SETTINGS_FILE), encoding="utf-8") as f:
            v = json.load(f)
        if isinstance(v, dict) and "notify" in v:
            out["notify"] = bool(v["notify"])
    except (OSError, ValueError, TypeError):
        pass
    return out


def save_settings(data_dir, settings):
    s = dict(DEFAULT_SETTINGS)
    s["notify"] = bool((settings or {}).get("notify", True))
    tmp = os.path.join(data_dir, SETTINGS_FILE + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(data_dir, SETTINGS_FILE))
    return s


def parse_version(v):
    out = []
    for part in str(v or "").strip().lstrip("vV").split("."):
        digits = "".join(ch for ch in part if ch.isdigit())
        out.append(int(digits) if digits else 0)
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def is_newer(remote, local):
    return parse_version(remote) > parse_version(local)


class UpdateError(Exception):
    def __init__(self, code, detail=""):
        super().__init__(code + (": " + detail if detail else ""))
        self.code = code
        self.detail = detail


def _val(f):
    if not isinstance(f, dict):
        return None
    for k in ("stringValue", "booleanValue", "doubleValue"):
        if k in f:
            return f[k]
    if "integerValue" in f:
        return int(f["integerValue"])
    return None


class Updater:
    """İş parçacığında çalışır; sonuçları callback ile değil, durum alanlarıyla verir (arayüz QTimer ile okur)."""

    def __init__(self, sync_cfg=None, current_version="0", channel=CHANNEL, app_dir=APP_DIR):
        self.sync_cfg = sync_cfg or (lambda: {})
        self.current = current_version
        self.channel = channel
        self.app_dir = app_dir
        self.state = "idle"   # idle | checking | none | available | downloading | installed | error
        self.info = {}        # yayındaki sürüm bilgisi
        self.error = ""
        self.progress = (0, 0)   # (indirilen bayt, toplam bayt)
        self.speed = 0.0         # bayt/saniye
        self.seq = 0          # her biten denetimde artar (arayüz yeni sonucu buradan anlar)
        self._busy = False
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ uç noktalar (GitHub)
    def _open(self, url, timeout=60):
        sep = "&" if "?" in url else "?"
        req = urllib.request.Request(url + sep + "t=" + str(int(time.time())),
                                     headers={"Accept-Encoding": "identity", "Cache-Control": "no-cache",
                                              "User-Agent": "BereketDefter/" + str(self.current)})
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise UpdateError("HTTP", str(e.code))
        except (urllib.error.URLError, OSError, ValueError) as e:
            raise UpdateError("NETWORK", str(getattr(e, "reason", e)))

    # ------------------------------------------------------------------ denetle
    def fetch_info(self):
        r = self._open(f"{GITHUB_RAW}/guncelleme/{self.channel}.json")
        if r is None:
            return None
        try:
            with r:
                return json.loads(r.read() or b"{}")
        except (OSError, ValueError) as e:
            raise UpdateError("NETWORK", str(e))

    def check(self, quiet=False):
        """quiet: arka plan denetimi; ekrandaki durumu 'denetleniyor'a çevirmez, hata olursa bulunan sürümü silmez."""
        with self._lock:
            if self._busy or self.state in ("downloading", "installed"):
                return self.state
            self._busy = True
            if not quiet:
                self.state, self.error = "checking", ""
        try:
            info = self.fetch_info()
            if self.state in ("downloading", "installed"):
                return self.state
            if info and info.get("surum") and info.get("dosya") and is_newer(info["surum"], self.current):
                self.info, self.state, self.error = info, "available", ""
            else:
                self.info, self.state, self.error = info or {}, "none", ""
        except UpdateError as e:
            if not (quiet and self.state == "available"):
                self.state, self.error = "error", e.code
        finally:
            self._busy = False
            self.seq += 1
        return self.state

    def check_async(self, quiet=False):
        if self._busy or self.state in ("downloading", "installed"):
            return
        threading.Thread(target=self.check, args=(quiet,), name="guncelleme", daemon=True).start()

    # ------------------------------------------------------------------ indir + kur
    def download(self, info):
        """Paketi GitHub'dan akış hâlinde indirir; progress = (indirilen, toplam bayt), speed = bayt/sn."""
        total = int(info.get("boyut") or 0)
        self.speed, self.progress = 0.0, (0, total)
        r = self._open(f"{GITHUB_RAW}/guncelleme/{info['dosya']}", timeout=120)
        if r is None:
            raise UpdateError("BAD_PACKAGE", "dosya yok")
        buf, done, t0 = io.BytesIO(), 0, time.monotonic()
        try:
            with r:
                total = total or int(r.headers.get("Content-Length") or 0)
                while True:
                    b = r.read(65536)
                    if not b:
                        break
                    buf.write(b)
                    done += len(b)
                    self.speed = done / max(time.monotonic() - t0, 0.05)
                    self.progress = (done, max(total, done))
        except (OSError, ValueError) as e:
            raise UpdateError("NETWORK", str(e))
        self.progress = (done, done)
        data = buf.getvalue()
        if hashlib.sha256(data).hexdigest() != str(info.get("sha256") or "").lower():
            raise UpdateError("BAD_PACKAGE", "sha256")
        return data

    def install_bytes(self, data):
        """ZIP içindeki dosyaları app klasörüne yazar. Önce tamamı yan klasöre açılır, sonra tek tek değiştirilir."""
        parent = os.path.dirname(self.app_dir)
        stage = os.path.join(parent, "app_guncelleme")
        backup = os.path.join(parent, "app_onceki")
        shutil.rmtree(stage, ignore_errors=True)
        try:
            z = zipfile.ZipFile(io.BytesIO(data))
        except zipfile.BadZipFile:
            raise UpdateError("BAD_PACKAGE", "zip")
        names = [n for n in z.namelist() if not n.endswith("/")]
        if "main.py" not in names:
            raise UpdateError("BAD_PACKAGE", "main.py yok")
        for n in names:
            parts = n.replace("\\", "/").split("/")
            if n.startswith("/") or ".." in parts or ":" in n or parts[0] in PROTECTED:
                raise UpdateError("BAD_PACKAGE", n)
        try:
            os.makedirs(stage)
            z.extractall(stage)
            # yedek: bir önceki sürümün app klasörü (sorun olursa elle geri alınabilir)
            shutil.rmtree(backup, ignore_errors=True)
            shutil.copytree(self.app_dir, backup, ignore=shutil.ignore_patterns("__pycache__"))
            for n in names:
                src = os.path.join(stage, *n.split("/"))
                dst = os.path.join(self.app_dir, *n.split("/"))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                os.replace(src, dst)
        except OSError as e:
            raise UpdateError("WRITE", str(e))
        finally:
            shutil.rmtree(stage, ignore_errors=True)

    def install(self, info=None):
        info = info or self.info
        with self._lock:
            if self.state == "downloading":
                return
            self.state, self.error = "downloading", ""
        try:
            if getattr(sys, "frozen", False):
                raise UpdateError("FROZEN")
            data = self.download(info)
            self.install_bytes(data)
            self.state = "installed"
        except UpdateError as e:
            self.state, self.error = "error", e.code + (": " + e.detail if e.detail else "")

    def install_async(self):
        threading.Thread(target=self.install, name="guncelleme-kur", daemon=True).start()


def restart_program():
    """Aynı Python ile main.py'yi yeniden açar (Veriler yolu ortam değişkeniyle aynen geçer)."""
    env = dict(os.environ)
    env["AV_YENIDEN_BASLAT"] = "1"
    args = [sys.executable, os.path.join(APP_DIR, "main.py")] + sys.argv[1:]
    kw = {"cwd": os.getcwd(), "env": env, "close_fds": True}
    if sys.platform == "win32":
        kw["creationflags"] = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    else:
        kw["start_new_session"] = True
    subprocess.Popen(args, **kw)
