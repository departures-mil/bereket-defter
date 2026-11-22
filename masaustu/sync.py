"""Bulut eşitleme (telefon <-> bilgisayar), Firebase REST API ile — yalnızca standart kütüphane.

Sözleşme: alacak-verecek-mobil/ESITLEME_SPEC.md (bölüm 1-6). Ağ işleri tek bir arka plan iş parçacığında
(kendi SQLite bağlantısıyla) yapılır; arayüz `events` kuyruğunu okur (QTimer ile), hiçbir zaman beklemez.
Ayarlar ve oturum <veri klasörü>/esitleme.json dosyasında tutulur (şifre asla kaydedilmez).
"""
import base64
import collections
import http.client
import json
import math
import mimetypes
import os
import queue
import re
import socket
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

import db as dbm

COLS = ("persons", "tx", "docs", "rem", "hist")
TABLE = {"persons": "persons", "tx": "transactions", "docs": "photos", "rem": "reminders", "hist": "history"}
CHUNK = dbm.CHUNK          # 700000 bayt
BLOB_BATCH = 8             # bir :commit isteğinde en fazla blob yazımı
ROW_BATCH = 200            # bir :commit isteğinde en fazla satır yazımı
PAGE = 300                 # runQuery sayfa boyu
EPOCH = "1970-01-01T00:00:00Z"
PERSON_STR = ("name", "phone", "note", "phone2", "wa_phone", "tg_user", "sg_phone", "email", "address")
PERSON_BOOL = ("ch_wa", "ch_tg", "ch_sg", "ch_call")
RULES = """rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{uid}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
    match /guncelleme/{document=**} {
      allow read: if true;
    }
  }
}
"""
AUTH_CODES = ("EMAIL_EXISTS", "EMAIL_NOT_FOUND", "INVALID_PASSWORD", "INVALID_LOGIN_CREDENTIALS", "WEAK_PASSWORD",
              "INVALID_EMAIL", "OPERATION_NOT_ALLOWED", "CONFIGURATION_NOT_FOUND", "API_KEY_INVALID",
              "TOO_MANY_ATTEMPTS_TRY_LATER", "USER_DISABLED", "MISSING_PASSWORD", "MISSING_EMAIL")
SESSION_CODES = ("TOKEN_EXPIRED", "INVALID_REFRESH_TOKEN", "USER_NOT_FOUND", "USER_DISABLED", "INVALID_ID_TOKEN",
                 "MISSING_REFRESH_TOKEN")
SAFE_ID = re.compile(r"^[A-Za-z0-9_-]{1,80}$")
SAFE_EXT = re.compile(r"^\.[a-z0-9]{1,10}$")
TS_RE = re.compile(r"^\d{4}-\d\d-\d\d \d\d:\d\d")


def norm_ts(s):
    """Tarih metnini masaüstü biçimine getirir ("YYYY-MM-DD HH:MM[:SS]"); olmuyorsa None."""
    s = (s or "").strip().replace("T", " ")[:19]
    if re.match(r"^\d{4}-\d\d-\d\d$", s):
        s += " 00:00"
    return s if TS_RE.match(s) else None


class SyncError(Exception):
    """code: EMAIL_EXISTS, ..., NETWORK, PERMISSION_DENIED, DB_NOT_FOUND, SESSION_EXPIRED, NOT_CONFIGURED,
    NOT_SIGNED_IN, SERVER, INTERNAL (arayüz bunları Türkçe metne çevirir)."""

    def __init__(self, code, detail=""):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail


# ---------------------------------------------------------------- Firestore değer kodlama
def enc(v):
    if isinstance(v, bool):
        return {"booleanValue": v}
    if isinstance(v, int):
        return {"integerValue": str(v)}
    if isinstance(v, float):
        return {"doubleValue": v}
    if isinstance(v, (bytes, bytearray)):
        return {"bytesValue": base64.b64encode(bytes(v)).decode("ascii")}
    return {"stringValue": "" if v is None else str(v)}


def dec(v):
    if not isinstance(v, dict):
        return None
    if "stringValue" in v:
        return v["stringValue"]
    if "integerValue" in v:
        try:
            return int(v["integerValue"])
        except (TypeError, ValueError):
            return 0
    if "doubleValue" in v:
        try:
            return float(v["doubleValue"])
        except (TypeError, ValueError):
            return 0.0
    if "booleanValue" in v:
        return bool(v["booleanValue"])
    if "timestampValue" in v:
        return v["timestampValue"]
    if "bytesValue" in v:
        return base64.b64decode(v["bytesValue"])
    if "referenceValue" in v:
        return v["referenceValue"]
    return None


class Doc:
    """Gelen bir Firestore belgesinin alanlarına güvenli erişim (eksik alan => boş / 0 / false)."""

    def __init__(self, fields):
        self.f = {k: dec(v) for k, v in (fields or {}).items()}

    def s(self, k):
        v = self.f.get(k)
        if v is None or isinstance(v, (bytes, bool)):
            return ""
        if isinstance(v, float) and v.is_integer():
            v = int(v)
        return str(v)

    def num(self, k):
        v = self.f.get(k)
        try:
            v = float(v) if v not in (None, "") and not isinstance(v, bool) else 0.0
        except (TypeError, ValueError):
            return 0.0
        return v if math.isfinite(v) else 0.0

    def int(self, k):
        return int(self.num(k))

    def b(self, k):
        v = self.f.get(k)
        return bool(v) if isinstance(v, (bool, int, float)) else str(v).lower() == "true" if v else False


def _auth_code(payload):
    err = (payload or {}).get("error") or {}
    if isinstance(err, str):  # securetoken bazen {"error": "invalid_grant"} döndürür
        return "INVALID_REFRESH_TOKEN" if "grant" in err else err.upper(), err
    msg = str(err.get("message") or "")
    text = json.dumps(payload)
    if "API key not valid" in msg or "API_KEY_INVALID" in text:
        return "API_KEY_INVALID", msg
    code = re.split(r"[\s:]", msg.strip(), 1)[0] if msg else "SERVER"
    return code or "SERVER", msg


def _db_missing(payload):
    """404'ün nedeni veritabanının hiç oluşturulmamış olması mı (tek bir belgenin yokluğu değil)?"""
    text = json.dumps(payload or {}).lower()
    return "database" in text and "does not exist" in text


def _fs_error(status, payload):
    err = (payload or {}).get("error") or {}
    msg = str(err.get("message") or "") if isinstance(err, dict) else str(err)
    text = json.dumps(payload)
    st = str(err.get("status") or "") if isinstance(err, dict) else ""
    if "API key not valid" in msg or "API_KEY_INVALID" in text:
        return SyncError("API_KEY_INVALID", msg)
    if _db_missing(payload) or status == 404 or st == "NOT_FOUND":
        return SyncError("DB_NOT_FOUND", msg)
    if status == 403 or st == "PERMISSION_DENIED":
        if "has not been used" in msg or "is disabled" in msg or "SERVICE_DISABLED" in text:
            return SyncError("DB_NOT_FOUND", msg)
        return SyncError("PERMISSION_DENIED", msg)
    if status == 401:
        return SyncError("SESSION_EXPIRED", msg)
    if status == 429:
        return SyncError("TOO_MANY_ATTEMPTS_TRY_LATER", msg)
    return SyncError("SERVER", f"HTTP {status} {msg}".strip())


# ---------------------------------------------------------------- motor
class SyncEngine:
    def __init__(self, data_dir=None, db_path=None, autostart=True):
        self.dir = data_dir or dbm.data_dir()
        self.db_path = db_path or os.path.join(self.dir, "veriler.db")
        self.cfg_path = os.path.join(self.dir, "esitleme.json")
        self.events = queue.Queue()     # arayüze giden sonuçlar (dict)
        self.log = collections.deque(maxlen=300)
        self._q = queue.Queue()
        self._lock = threading.RLock()
        self._sync_queued = False
        self.busy = False
        self.last = None                # son "done" olayı
        self.id_token, self.token_exp = "", 0.0
        self._db = None
        self.cfg = self._load()
        self._thread = threading.Thread(target=self._run, name="esitleme", daemon=True)
        if autostart:
            self._thread.start()

    # --- ayarlar
    DEFAULT = {"apiKey": "", "projectId": "", "emulator": "", "email": "", "uid": "", "refreshToken": "",
               "binding": "", "cursors": {}, "lastSync": ""}

    def _load(self):
        cfg = dict(self.DEFAULT)
        try:
            with open(self.cfg_path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                cfg.update({k: v for k, v in data.items() if k in self.DEFAULT})
        except (OSError, ValueError):
            pass
        if not isinstance(cfg.get("cursors"), dict):
            cfg["cursors"] = {}
        return cfg

    def _save(self):
        with self._lock:
            data = json.dumps(self.cfg, ensure_ascii=False, indent=1)
            tmp = self.cfg_path + ".tmp"
            try:
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(data)
                os.replace(tmp, self.cfg_path)
            except OSError as e:
                self._log("esitleme.json yazılamadı: %s" % e)

    def signed_in(self):
        c = self.cfg
        return bool(c.get("refreshToken") and c.get("uid") and c.get("apiKey") and c.get("projectId"))

    def _log(self, text):
        self.log.append(f"{datetime.now():%H:%M:%S} {text}")

    # --- Wi‑Fi eşitleme (lan.py): istek motorun iş parçacığında, bulut eşitlemesiyle sırayla yürür
    def lan_call(self, kind, body, timeout=180):
        box = {"done": threading.Event(), "res": None}
        self._q.put(("lan", {"kind": kind, "body": body, "box": box}))
        if not box["done"].wait(timeout):
            return None
        return box["res"]

    # --- istekler (arayüz iş parçacığından çağrılır, hemen döner)
    def request(self, op, **kw):
        """op: 'sync' | 'signin' | 'signup' | 'signout'."""
        if op == "sync":
            with self._lock:
                if self._sync_queued:
                    return
                self._sync_queued = True
        self._q.put((op, kw))

    def stop(self):
        self._q.put((None, {}))

    def _emit(self, ev):
        self.events.put(ev)

    def _run(self):
        while True:
            op, kw = self._q.get()
            if op is None:
                break
            if op == "sync":
                with self._lock:
                    self._sync_queued = False
            self.busy = True
            self._emit({"type": "busy", "op": op})
            ev = self.run_op(op, **kw)
            self.busy = False
            self._emit(ev)

    def run_op(self, op, **kw):
        """İşlemi bu iş parçacığında yürütür ve sonucu (olay) döndürür; testlerde doğrudan çağrılabilir."""
        if op == "lan":
            box = kw.get("box") or {}
            ev = {"type": "done", "op": "lan", "ok": False, "code": "", "detail": "", "changed": False}
            try:
                res = self._op_lan(kw.get("kind"), kw.get("body") or {})
                ev.update(ok=True, changed=bool(res.get("_got")))
            except Exception as e:
                res = {"error": f"{type(e).__name__}: {e}"}
                self._log("Wi‑Fi eşitleme hatası: " + traceback.format_exc())
            box["res"] = res
            if box.get("done"):
                box["done"].set()
            ev["time"] = datetime.now().strftime("%H:%M")
            return ev
        ev = {"type": "done", "op": op, "ok": False, "code": "", "detail": "", "changed": False}
        try:
            res = getattr(self, "_op_" + op)(**kw) or {}
            ev.update(res)
            ev["ok"] = True
        except SyncError as e:
            ev.update(code=e.code, detail=e.detail)
            self._log(f"{op} hata {e.code}: {e.detail}")
        except Exception as e:  # beklenmeyen hata: programı düşürmesin
            ev.update(code="INTERNAL", detail=f"{type(e).__name__}: {e}")
            self._log(traceback.format_exc())
        ev["time"] = datetime.now().strftime("%H:%M")
        if op == "sync" and ev["ok"]:
            self.cfg["lastSync"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._save()
        self.last = ev
        return ev

    # --- uç noktalar
    def _emu(self):
        e = (self.cfg.get("emulator") or "").strip()
        e = re.sub(r"^https?://", "", e).rstrip("/")
        return e.split(":")[0] if e.count(":") == 1 else e

    def _auth_url(self, method):
        e = self._emu()
        base = f"http://{e}:9099/identitytoolkit.googleapis.com/v1" if e else "https://identitytoolkit.googleapis.com/v1"
        return f"{base}/accounts:{method}?key={urllib.parse.quote(self.cfg['apiKey'])}"

    def _token_url(self):
        e = self._emu()
        base = f"http://{e}:9099/securetoken.googleapis.com/v1/token" if e else \
            "https://securetoken.googleapis.com/v1/token"
        return f"{base}?key={urllib.parse.quote(self.cfg['apiKey'])}"

    def _fs_base(self):
        e = self._emu()
        pid = urllib.parse.quote(self.cfg["projectId"], safe="")
        root = f"http://{e}:8080/v1" if e else "https://firestore.googleapis.com/v1"
        return f"{root}/projects/{pid}/databases/(default)/documents"

    def _doc_name(self, col, did):
        return (f"projects/{self.cfg['projectId']}/databases/(default)/documents/users/{self.cfg['uid']}"
                f"/{col}/{did}")

    # --- HTTP
    def _http(self, method, url, body=None, headers=None, form=False, timeout=60):
        hdrs = dict(headers or {})
        data = None
        if body is not None:
            if form:
                data = urllib.parse.urlencode(body).encode()
                hdrs["Content-Type"] = "application/x-www-form-urlencoded"
            else:
                data = json.dumps(body).encode()
                hdrs["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        # emülatör (yerel) için vekil sunucu (proxy) kullanılmaz
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if self._emu() else \
            urllib.request.build_opener()
        try:
            with opener.open(req, timeout=timeout) as r:
                raw = r.read()
                return r.status, (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as e:
            try:
                raw = e.read()
                payload = json.loads(raw) if raw else {}
            except (ValueError, OSError):
                payload = {"error": {"message": f"HTTP {e.code}"}}
            if isinstance(payload, list) and payload:
                payload = payload[0]
            return e.code, payload if isinstance(payload, dict) else {}
        except (urllib.error.URLError, OSError, socket.timeout, http.client.HTTPException, ValueError) as e:
            raise SyncError("NETWORK", str(getattr(e, "reason", e)))

    # --- oturum
    def _check_config(self):
        if not (self.cfg.get("apiKey") and self.cfg.get("projectId")):
            raise SyncError("NOT_CONFIGURED")

    def _sign(self, method, email, password):
        self._check_config()
        if not email or not password:
            raise SyncError("MISSING_PASSWORD" if email else "MISSING_EMAIL")
        st, p = self._http("POST", self._auth_url(method),
                           {"email": email, "password": password, "returnSecureToken": True}, timeout=30)
        if st != 200:
            raise SyncError(*_auth_code(p))
        self.id_token = p["idToken"]
        self.token_exp = time.time() + int(p.get("expiresIn") or 3600)
        with self._lock:
            self.cfg.update(email=email, uid=p["localId"], refreshToken=p["refreshToken"])
        self._save()
        self._log(f"giriş: {email} uid={p['localId']}")
        return {"email": email, "uid": p["localId"]}

    def _configure(self, api_key=None, project_id=None, emulator=None):
        with self._lock:
            new = {"apiKey": (api_key or "").strip() if api_key is not None else self.cfg["apiKey"],
                   "projectId": (project_id or "").strip() if project_id is not None else self.cfg["projectId"],
                   "emulator": (emulator or "").strip() if emulator is not None else self.cfg["emulator"]}
            if any(new[k] != self.cfg.get(k) for k in new):
                self.cfg.update(new, refreshToken="")
                self.id_token, self.token_exp = "", 0.0
        self._save()

    def _op_signin(self, email="", password="", api_key=None, project_id=None, emulator=None):
        self._configure(api_key, project_id, emulator)
        res = self._sign("signInWithPassword", (email or "").strip(), password or "")
        self.request("sync")
        return res

    def _op_signup(self, email="", password="", api_key=None, project_id=None, emulator=None):
        self._configure(api_key, project_id, emulator)
        res = self._sign("signUp", (email or "").strip(), password or "")
        self.request("sync")
        return res

    def _op_signout(self):
        with self._lock:
            self.cfg["refreshToken"] = ""
            self.id_token, self.token_exp = "", 0.0
        self._save()
        return {}

    def _ensure_token(self, force=False):
        if not force and self.id_token and time.time() < self.token_exp - 300:
            return
        if not self.signed_in():
            raise SyncError("NOT_SIGNED_IN")
        st, p = self._http("POST", self._token_url(),
                           {"grant_type": "refresh_token", "refresh_token": self.cfg["refreshToken"]},
                           form=True, timeout=30)
        if st != 200:
            code, msg = _auth_code(p)
            if code in SESSION_CODES:
                with self._lock:
                    self.cfg["refreshToken"] = ""
                self._save()
                raise SyncError("SESSION_EXPIRED", msg)
            raise SyncError(code, msg)
        self.id_token = p["id_token"]
        self.token_exp = time.time() + int(p.get("expires_in") or 3600)
        if p.get("refresh_token") and p["refresh_token"] != self.cfg["refreshToken"]:
            with self._lock:
                self.cfg["refreshToken"] = p["refresh_token"]
            self._save()

    def _fs(self, method, path, body=None, timeout=90, missing_ok=False):
        for attempt in (0, 1):
            self._ensure_token(force=attempt == 1)
            st, p = self._http(method, self._fs_base() + path, body, timeout=timeout,
                               headers={"Authorization": "Bearer " + self.id_token})
            if st == 401 and attempt == 0:
                continue
            if 200 <= st < 300:
                return p
            if st == 404 and missing_ok and not _db_missing(p):
                return None
            raise _fs_error(st, p)

    def _commit(self, writes):
        if writes:
            self._fs("POST", ":commit", {"writes": writes})

    def _write(self, col, did, fields):
        return {"update": {"name": self._doc_name(col, did), "fields": {k: enc(v) for k, v in fields.items()}},
                "updateTransforms": [{"fieldPath": "sm", "setToServerValue": "REQUEST_TIME"}]}

    # --- eşitleme
    @property
    def db(self):
        if self._db is None:  # bu iş parçacığına ait bağlantı
            self._db = dbm.DB(self.db_path)
        return self._db

    def _bind(self, con):
        """Başka bir hesaba/projeye geçildiyse imleçleri sıfırla ve her şeyi yeniden gönder."""
        key = f"{self.cfg['projectId']}|{self._emu()}|{self.cfg['uid']}"
        if self.cfg.get("binding") == key:
            return
        for t in TABLE.values():
            con.execute(f"UPDATE {t} SET dirty=1")
        con.execute("UPDATE photos SET blobs_up=0")
        con.commit()
        with self._lock:
            self.cfg.update(binding=key, cursors={})
        self._save()
        self._log("yeni hesap/proje bağlantısı: " + key)

    def _op_sync(self):
        self._check_config()
        if not self.signed_in():
            raise SyncError("NOT_SIGNED_IN")
        self._ensure_token()
        con = self.db.con
        self._bind(con)
        # Not: önce çekme, sonra gönderme. Spec §4 önce gönderip sonra çekmeyi anlatır; ama o sırayla, çevrimdışı
        # yapılmış ESKİ bir değişiklik sunucudaki daha YENİ sürümün üzerine yazılır ve §4.4'teki "yeni m kazanır"
        # kuralı bozulur. Önce çekince birleştirme kuralı yerelde uygulanır, sonra yalnızca kazanan satırlar gider.
        changed, pulled = self._pull(con)
        pushed = self._push(con)
        got = self._download(con)
        self._log(f"eşitleme: gönderilen {pushed}, değişen {pulled}, indirilen belge {got}")
        return {"pushed": pushed, "pulled": pulled, "downloaded": got, "changed": bool(pulled or got),
                "pending": self.db.pending_changes()}

    # push ------------------------------------------------------------
    def _doc_meta(self, con, ph):
        """Yerel belge satırının boyut / parça / mime bilgisini dosyadan tamamlar."""
        path = self.db.photo_path(ph)
        size = os.path.getsize(path) if os.path.isfile(path) else 0
        ext = os.path.splitext(ph["file"])[1].lower()
        mime = ph["mime"] or mimetypes.guess_type("x" + ext)[0] or ""
        chunks = dbm.file_chunks(size)
        con.execute("UPDATE photos SET size=?, chunks=?, mime=? WHERE id=?", (size, chunks, mime, ph["id"]))
        return path, size, chunks

    def _upload_blobs(self, con):
        rows = con.execute("SELECT * FROM photos WHERE dirty=1 AND blobs_up=0").fetchall()
        n = 0
        for ph in rows:
            path, size, chunks = self._doc_meta(con, ph)
            con.commit()
            writes = []
            try:
                f = open(path, "rb") if chunks else None
            except OSError as e:
                self._log(f"belge okunamadı {path}: {e}")
                f, chunks = None, 0
                con.execute("UPDATE photos SET size=0, chunks=0 WHERE id=?", (ph["id"],))
            try:
                for i in range(chunks):
                    data = f.read(CHUNK)
                    writes.append(self._write("blobs", f"{ph['uid']}_{i}",
                                              {"doc": ph["uid"], "i": i, "d": data, "m": int(ph["m"] or 0)}))
                    if len(writes) >= BLOB_BATCH:
                        self._commit(writes)
                        n += len(writes)
                        writes = []
                self._commit(writes)
                n += len(writes)
            finally:
                if f:
                    f.close()
            con.execute("UPDATE photos SET blobs_up=1 WHERE id=?", (ph["id"],))
            con.commit()
        return n

    def _hist_old(self, con, h):
        text = h["old_values"] or ""
        try:
            if isinstance(json.loads(text), dict):
                return text
        except ValueError:
            pass
        o = dbm.parse_old(text)  # v1.0-1.1 kaydı: repr(dict) -> sözleşmedeki JSON
        p = con.execute("SELECT uid, name FROM persons WHERE id=?", (o.get("person_id"),)).fetchone()
        return json.dumps({"ts": o.get("ts", ""), "direction": o.get("direction", ""),
                           "currency": o.get("currency", ""), "amount": float(o.get("amount") or 0),
                           "description": o.get("description") or "", "person": p["uid"] if p else "",
                           "person_name": p["name"] if p else ""}, ensure_ascii=False)

    def _row_writes(self, con):
        out = []  # (write, tablo, yerel id, m)
        for p in con.execute("SELECT * FROM persons WHERE dirty=1"):
            f = {"id": p["uid"], "m": int(p["m"] or 0), "del": False}
            f.update({k: p[k] or "" for k in PERSON_STR})
            f.update({k: bool(p[k]) for k in PERSON_BOOL})
            f["created_at"] = p["created_at"] or ""
            out.append((self._write("persons", p["uid"], f), "persons", p["id"], p["m"]))
        for t in con.execute("SELECT t.*, p.uid puid FROM transactions t JOIN persons p ON p.id=t.person_id "
                             "WHERE t.dirty=1"):
            f = {"id": t["uid"], "m": int(t["m"] or 0), "del": False, "person": t["puid"], "ts": t["ts"],
                 "direction": t["direction"], "currency": t["currency"], "amount": float(t["amount"]),
                 "description": t["description"] or "", "created_at": t["created_at"] or "",
                 "updated_at": t["updated_at"] or ""}
            out.append((self._write("tx", t["uid"], f), "transactions", t["id"], t["m"]))
        for d in con.execute("SELECT f.*, t.uid tuid FROM photos f JOIN transactions t ON t.id=f.tx_id "
                             "WHERE f.dirty=1 AND f.blobs_up=1"):
            ext = os.path.splitext(d["file"])[1].lower()
            f = {"id": d["uid"], "m": int(d["m"] or 0), "del": False, "tx": d["tuid"],
                 "name": d["original_name"] or os.path.basename(d["file"]), "ext": ext, "mime": d["mime"] or "",
                 "size": max(int(d["size"] or 0), 0), "chunks": int(d["chunks"] or 0),
                 "added_at": d["added_at"] or ""}
            out.append((self._write("docs", d["uid"], f), "photos", d["id"], d["m"]))
        for r in con.execute("SELECT r.*, p.uid puid FROM reminders r JOIN persons p ON p.id=r.person_id "
                             "WHERE r.dirty=1"):
            f = {"id": r["uid"], "m": int(r["m"] or 0), "del": False, "person": r["puid"], "kind": r["kind"],
                 "currency": r["currency"], "amount": float(r["amount"] or 0), "due": r["due"] or "",
                 "note": r["note"] or "", "done": bool(r["done"]), "created_at": r["created_at"] or ""}
            out.append((self._write("rem", r["uid"], f), "reminders", r["id"], r["m"]))
        for h in con.execute("SELECT * FROM history WHERE dirty=1").fetchall():
            f = {"id": h["uid"], "m": int(h["m"] or 0), "del": False, "tx": h["tx_uid"] or "",
                 "action": h["action"], "at": h["at"] or "", "old": self._hist_old(con, h)}
            out.append((self._write("hist", h["uid"], f), "history", h["id"], h["m"]))
        for tb in con.execute("SELECT * FROM tombstones WHERE dirty=1"):
            out.append((self._write(tb["col"], tb["uid"], {"id": tb["uid"], "m": int(tb["m"]), "del": True}),
                        "tombstones", (tb["col"], tb["uid"]), tb["m"]))
        return out

    def _push(self, con):
        self._upload_blobs(con)
        rows = self._row_writes(con)
        for i in range(0, len(rows), ROW_BATCH):
            part = rows[i:i + ROW_BATCH]
            self._commit([w for w, *_r in part])
            for _w, table, key, m in part:
                if table == "tombstones":
                    con.execute("UPDATE tombstones SET dirty=0 WHERE col=? AND uid=? AND m=?", (key[0], key[1], m))
                else:  # bu arada yeniden değiştiyse kirli kalır
                    con.execute(f"UPDATE {table} SET dirty=0 WHERE id=? AND m=?", (key, m))
            con.commit()
        # silinen belgelerin blob parçalarını da sil (en iyi çaba)
        dels = []
        for tb in con.execute("SELECT * FROM tombstones WHERE col='docs' AND chunks>0").fetchall():
            dels += [({"delete": self._doc_name("blobs", f"{tb['uid']}_{i}")}) for i in range(tb["chunks"])]
            dels.append(tb["uid"])
        batch, uids = [], []
        for x in dels + [None]:
            if isinstance(x, dict):
                batch.append(x)
            elif x is not None:
                uids.append(x)
            if batch and (len(batch) >= ROW_BATCH or x is None):
                try:
                    self._commit(batch)
                    for u in uids:
                        con.execute("UPDATE tombstones SET chunks=0 WHERE col='docs' AND uid=?", (u,))
                    con.commit()
                except SyncError as e:
                    self._log(f"blob silinemedi: {e}")
                batch, uids = [], []
        return len(rows)

    # pull ------------------------------------------------------------
    def _pull(self, con):
        changed = 0
        aside = []
        for col in COLS:
            cur = self.cfg["cursors"].get(col) or {}
            last_sm, last_name = cur.get("lastSm") or EPOCH, cur.get("lastName") or ""
            start = None
            while True:
                q = {"from": [{"collectionId": col}],
                     "where": {"fieldFilter": {"field": {"fieldPath": "sm"}, "op": "GREATER_THAN_OR_EQUAL",
                                               "value": {"timestampValue": last_sm}}},
                     "orderBy": [{"field": {"fieldPath": "sm"}, "direction": "ASCENDING"},
                                 {"field": {"fieldPath": "__name__"}, "direction": "ASCENDING"}],
                     "limit": PAGE}
                if start:
                    q["startAt"] = {"before": False, "values": [{"timestampValue": start[0]},
                                                                {"referenceValue": start[1]}]}
                resp = self._fs("POST", f"/users/{self.cfg['uid']}:runQuery", {"structuredQuery": q}) or []
                docs = [e["document"] for e in resp if isinstance(e, dict) and e.get("document")]
                for d in docs:
                    did = d["name"].rsplit("/", 1)[-1]
                    r = self._apply(con, col, did, Doc(d.get("fields")))
                    if r == "changed":
                        changed += 1
                    elif r == "orphan":
                        aside.append((col, did, Doc(d.get("fields"))))
                    sm = (d.get("fields", {}).get("sm") or {}).get("timestampValue")
                    if sm:
                        last_sm, last_name = sm, d["name"]
                con.commit()
                with self._lock:
                    self.cfg["cursors"][col] = {"lastSm": last_sm, "lastName": last_name}
                self._save()
                if len(docs) < PAGE:
                    break
                start = (last_sm, last_name)
        # üst kaydı (kişi / kayıt) henüz olmayanları sonda bir kez daha dene
        for col, did, doc in aside:
            r = self._apply(con, col, did, doc)
            if r == "changed":
                changed += 1
            elif r == "orphan":
                self._log(f"atlandı ({col}/{did}): bağlı olduğu kişi/kayıt bulunamadı")
        con.commit()
        return changed > 0, changed

    def _delete_local(self, con, table, rid):
        db = self.db
        if table == "persons":
            for t in con.execute("SELECT id FROM transactions WHERE person_id=?", (rid,)).fetchall():
                self._delete_files(con, t["id"])
        elif table == "transactions":
            self._delete_files(con, rid)
        elif table == "photos":
            ph = con.execute("SELECT * FROM photos WHERE id=?", (rid,)).fetchone()
            if ph:
                db._remove_file(ph)
        con.execute(f"DELETE FROM {table} WHERE id=?", (rid,))

    def _delete_files(self, con, tid):
        for ph in con.execute("SELECT * FROM photos WHERE tx_id=?", (tid,)).fetchall():
            self.db._remove_file(ph)
        self.db._remove_photo_files(tid)

    def _apply(self, con, col, did, d):
        """Birleştirme kuralı (spec §4.4). Dönen: 'changed' | 'same' | 'kept' | 'orphan' | 'bad'."""
        table = TABLE[col]
        rm = d.int("m")
        local = con.execute(f"SELECT id, m, dirty FROM {table} WHERE uid=?", (did,)).fetchone()
        tomb = con.execute("SELECT m, dirty FROM tombstones WHERE col=? AND uid=?", (col, did)).fetchone()
        if local and local["dirty"] and (local["m"] or 0) > rm:
            return "kept"
        if not local and tomb and tomb["dirty"] and tomb["m"] > rm:
            return "kept"
        if d.b("del"):
            if tomb and tomb["dirty"]:
                con.execute("UPDATE tombstones SET dirty=0 WHERE col=? AND uid=?", (col, did))
            if local:
                self._delete_local(con, table, local["id"])
                return "changed"
            return "same"
        if local and not local["dirty"] and (local["m"] or 0) == rm:
            return "same"
        try:
            r = getattr(self, "_up_" + col)(con, did, d, rm, local["id"] if local else None)
        except Exception as e:  # sqlite kısıtı vb.: bu belgeyi atla
            self._log(f"uygulanamadı ({col}/{did}): {e}")
            return "bad"
        if r == "changed" and tomb:
            con.execute("DELETE FROM tombstones WHERE col=? AND uid=?", (col, did))
        return r

    @staticmethod
    def _upsert(con, table, lid, did, rm, vals):
        if lid is not None:
            sets = ",".join(f"{k}=?" for k in vals)
            con.execute(f"UPDATE {table} SET {sets},m=?,dirty=0 WHERE id=?", (*vals.values(), rm, lid))
        else:
            ks = ",".join(vals)
            qs = ",".join("?" * len(vals))
            con.execute(f"INSERT INTO {table}({ks},uid,m,dirty) VALUES({qs},?,?,0)", (*vals.values(), did, rm))
        return "changed"

    @staticmethod
    def _pid(con, uid):
        r = con.execute("SELECT id FROM persons WHERE uid=?", (uid,)).fetchone() if uid else None
        return r["id"] if r else None

    @staticmethod
    def _tid(con, uid):
        r = con.execute("SELECT id FROM transactions WHERE uid=?", (uid,)).fetchone() if uid else None
        return r["id"] if r else None

    def _up_persons(self, con, did, d, rm, lid):
        vals = {k: d.s(k) for k in PERSON_STR}
        vals.update({k: int(d.b(k)) for k in PERSON_BOOL})
        vals["created_at"] = d.s("created_at") or dbm.now()
        return self._upsert(con, "persons", lid, did, rm, vals)

    def _up_tx(self, con, did, d, rm, lid):
        pid = self._pid(con, d.s("person"))
        if pid is None:
            return "orphan"
        if d.s("direction") not in dbm.DIRECTIONS or d.s("currency") not in dbm.CURRENCIES or d.num("amount") <= 0:
            self._log(f"geçersiz kayıt atlandı tx/{did}")
            return "bad"
        ts = norm_ts(d.s("ts"))
        if ts is None:
            self._log(f"tarih biçimi geçersiz, atlandı tx/{did}: {d.s('ts')!r}")
            return "bad"
        vals = {"person_id": pid, "ts": ts, "direction": d.s("direction"),
                "currency": d.s("currency"), "amount": d.num("amount"), "description": d.s("description"),
                "created_at": d.s("created_at") or dbm.now(), "updated_at": d.s("updated_at") or None}
        return self._upsert(con, "transactions", lid, did, rm, vals)

    def _up_docs(self, con, did, d, rm, lid):
        tid = self._tid(con, d.s("tx"))
        if tid is None:
            return "orphan"
        ext = d.s("ext").lower()
        if not SAFE_EXT.match(ext):
            ext = os.path.splitext(d.s("name"))[1].lower()
            ext = ext if SAFE_EXT.match(ext) else ""
        vals = {"tx_id": tid, "original_name": d.s("name"), "added_at": d.s("added_at") or dbm.now(),
                "mime": d.s("mime"), "size": d.int("size"), "chunks": d.int("chunks"), "blobs_up": 1}
        if lid is None:  # gelen belgeler fotograflar/sync/<docid><ext> olarak saklanır
            safe = did if SAFE_ID.match(did) else dbm.new_uid()
            vals["file"] = os.path.join("sync", safe + ext)
        return self._upsert(con, "photos", lid, did, rm, vals)

    def _up_rem(self, con, did, d, rm, lid):
        pid = self._pid(con, d.s("person"))
        if pid is None:
            return "orphan"
        if d.s("kind") not in ("TAHSIL", "ODEME") or d.s("currency") not in dbm.CURRENCIES:
            self._log(f"geçersiz hatırlatıcı atlandı rem/{did}")
            return "bad"
        due = norm_ts(d.s("due"))
        if due is None:
            self._log(f"tarih biçimi geçersiz, atlandı rem/{did}: {d.s('due')!r}")
            return "bad"
        vals = {"person_id": pid, "kind": d.s("kind"), "currency": d.s("currency"),
                "amount": max(d.num("amount"), 0.0), "due": due, "note": d.s("note"),
                "done": int(d.b("done")), "created_at": d.s("created_at") or dbm.now()}
        return self._upsert(con, "reminders", lid, did, rm, vals)

    def _up_hist(self, con, did, d, rm, lid):
        vals = {"tx_id": self._tid(con, d.s("tx")) or 0, "tx_uid": d.s("tx"), "action": d.s("action"),
                "at": d.s("at") or dbm.now(), "old_values": d.s("old")}
        return self._upsert(con, "history", lid, did, rm, vals)

    # Wi‑Fi eşitleme -------------------------------------------------------
    def _all_fields(self, con):
        """Bütün satırlar (kirli olsun olmasın) ve silme işaretleri, Firestore alan biçiminde: {col: [fields]}."""
        out = {c: [] for c in COLS}

        def add(col, f):
            out[col].append({k: enc(v) for k, v in f.items()})
        for p in con.execute("SELECT * FROM persons"):
            f = {"id": p["uid"], "m": int(p["m"] or 0), "del": False}
            f.update({k: p[k] or "" for k in PERSON_STR})
            f.update({k: bool(p[k]) for k in PERSON_BOOL})
            f["created_at"] = p["created_at"] or ""
            add("persons", f)
        for t in con.execute("SELECT t.*, p.uid puid FROM transactions t JOIN persons p ON p.id=t.person_id"):
            add("tx", {"id": t["uid"], "m": int(t["m"] or 0), "del": False, "person": t["puid"], "ts": t["ts"],
                       "direction": t["direction"], "currency": t["currency"], "amount": float(t["amount"]),
                       "description": t["description"] or "", "created_at": t["created_at"] or "",
                       "updated_at": t["updated_at"] or ""})
        for d in con.execute("SELECT f.*, t.uid tuid FROM photos f JOIN transactions t ON t.id=f.tx_id").fetchall():
            path = self.db.photo_path(d)
            size = os.path.getsize(path) if os.path.isfile(path) else max(int(d["size"] or 0), 0)
            ext = os.path.splitext(d["file"])[1].lower()
            add("docs", {"id": d["uid"], "m": int(d["m"] or 0), "del": False, "tx": d["tuid"],
                         "name": d["original_name"] or os.path.basename(d["file"]), "ext": ext,
                         "mime": d["mime"] or mimetypes.guess_type("x" + ext)[0] or "", "size": size,
                         "chunks": dbm.file_chunks(size), "added_at": d["added_at"] or ""})
        for r in con.execute("SELECT r.*, p.uid puid FROM reminders r JOIN persons p ON p.id=r.person_id"):
            add("rem", {"id": r["uid"], "m": int(r["m"] or 0), "del": False, "person": r["puid"], "kind": r["kind"],
                        "currency": r["currency"], "amount": float(r["amount"] or 0), "due": r["due"] or "",
                        "note": r["note"] or "", "done": bool(r["done"]), "created_at": r["created_at"] or ""})
        for h in con.execute("SELECT * FROM history").fetchall():
            add("hist", {"id": h["uid"], "m": int(h["m"] or 0), "del": False, "tx": h["tx_uid"] or "",
                         "action": h["action"], "at": h["at"] or "", "old": self._hist_old(con, h)})
        for tb in con.execute("SELECT * FROM tombstones"):
            if tb["col"] in out:
                add(tb["col"], {"id": tb["uid"], "m": int(tb["m"]), "del": True})
        return out

    def _op_lan(self, kind, body):
        con = self.db.con
        if kind == "sync":
            got = 0
            aside = []
            incoming = body.get("docs") or {}
            for col in COLS:  # ebeveynler önce (kişi → kayıt → belge/hatırlatıcı)
                for fields in incoming.get(col) or []:
                    if not isinstance(fields, dict):
                        continue
                    d = Doc(fields)
                    did = d.s("id")
                    if not did or not SAFE_ID.match(did) or self._lan_same(con, col, did, d):
                        continue
                    r = self._apply(con, col, did, d)
                    if r == "orphan":
                        aside.append((col, did, d))
                    elif r == "changed":
                        got += 1
                        self._lan_dirty(con, col, did, d)
            for col, did, d in aside:
                if self._apply(con, col, did, d) == "changed":
                    got += 1
                    self._lan_dirty(con, col, did, d)
            con.commit()
            have = set(x for x in (body.get("have") or []) if isinstance(x, str))
            need = []
            for ph in con.execute("SELECT * FROM photos").fetchall():
                if not os.path.isfile(self.db.photo_path(ph)) and ph["uid"] in have:
                    need.append(ph["uid"])
            docs = self._all_fields(con)
            sent = sum(len(v) for v in docs.values())
            if got:
                self._log(f"Wi‑Fi eşitleme ({body.get('device') or 'telefon'}): değişen {got}")
            return {"docs": docs, "need": need, "name": socket.gethostname(), "_got": got, "_sent": sent}
        if kind == "blob":
            uid = str(body.get("id") or "")
            ph = con.execute("SELECT * FROM photos WHERE uid=?", (uid,)).fetchone()
            path = self.db.photo_path(ph) if ph else ""
            if not ph or not os.path.isfile(path):
                return {"error": "missing"}
            with open(path, "rb") as f:
                return {"data": base64.b64encode(f.read()).decode("ascii")}
        if kind == "upload":
            uid = str(body.get("id") or "")
            ph = con.execute("SELECT * FROM photos WHERE uid=?", (uid,)).fetchone()
            if not ph:
                return {"error": "unknown"}
            data = base64.b64decode(body.get("data") or "")
            if ph["size"] and len(data) != int(ph["size"]):
                return {"error": "size"}
            path = self.db.photo_path(ph)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            tmp = path + ".part"
            with open(tmp, "wb") as f:
                f.write(data)
            os.replace(tmp, path)
            # dosya artık burada: internet gelince parçaları bu bilgisayar da buluta yükleyebilir
            con.execute("UPDATE photos SET blobs_up=0, dirty=1, size=? WHERE id=?", (len(data), ph["id"]))
            con.commit()
            return {"ok": True, "_got": 1}
        return {"error": "kind"}

    def _lan_same(self, con, col, did, d):
        """Aynı sürüm (aynı m, aynı silinme durumu) zaten burada: dokunma — kirli işareti (buluta gidecek) korunur."""
        rm, dele = d.int("m"), d.b("del")
        if dele:
            tb = con.execute("SELECT m FROM tombstones WHERE col=? AND uid=?", (col, did)).fetchone()
            return bool(tb and tb["m"] == rm)
        row = con.execute(f"SELECT m FROM {TABLE[col]} WHERE uid=?", (did,)).fetchone()
        return bool(row and (row["m"] or 0) == rm)

    def _lan_dirty(self, con, col, did, d):
        """Wi‑Fi'dan gelen değişiklik buluta da gitsin (kirli). Belge dosyası henüz yoksa parçalar sonra yüklenir."""
        if d.b("del"):
            con.execute("UPDATE tombstones SET dirty=1 WHERE col=? AND uid=?", (col, did))
            if not con.execute("SELECT 1 FROM tombstones WHERE col=? AND uid=?", (col, did)).fetchone():
                try:
                    con.execute("INSERT INTO tombstones(col, uid, m, dirty) VALUES(?,?,?,1)", (col, did, d.int("m")))
                except Exception:
                    pass
            return
        table = TABLE[col]
        if col == "docs":
            ph = con.execute("SELECT * FROM photos WHERE uid=?", (did,)).fetchone()
            if ph and not os.path.isfile(self.db.photo_path(ph)):
                return  # dosya gelince (upload) kirli yapılır
            con.execute("UPDATE photos SET dirty=1, blobs_up=0 WHERE uid=?", (did,))
            return
        con.execute(f"UPDATE {table} SET dirty=1 WHERE uid=?", (did,))

    # belgeler ----------------------------------------------------------
    def _download(self, con):
        got = 0
        for ph in con.execute("SELECT * FROM photos WHERE blobs_up=1").fetchall():
            path = self.db.photo_path(ph)
            if os.path.exists(path):
                continue
            parts = []
            for i in range(max(int(ph["chunks"] or 0), 0)):
                p = self._fs("GET", f"/users/{self.cfg['uid']}/blobs/{ph['uid']}_{i}", missing_ok=True,
                             timeout=120)
                data = Doc((p or {}).get("fields")).f.get("d") if p else None
                if not isinstance(data, bytes):
                    parts = None
                    self._log(f"belge parçası henüz yok: {ph['uid']}_{i}")
                    break
                parts.append(data)
            if parts is None:
                continue
            blob = b"".join(parts)
            if ph["size"] is not None and ph["size"] >= 0 and len(blob) != ph["size"]:
                self._log(f"belge boyutu tutmuyor: {ph['uid']} {len(blob)} != {ph['size']}")
                continue
            os.makedirs(os.path.dirname(path), exist_ok=True)
            tmp = path + ".part"
            with open(tmp, "wb") as f:
                f.write(blob)
            os.replace(tmp, path)
            got += 1
        return got
