"""ESKİ KANAL KÖPRÜSÜ (1.20 ve öncesi taşınabilir masaüstü → 1.21.0 kurulumlu sürüm).

Eski program raw guncelleme/masaustu.json'dan bu paketi indirip app\\ klasörüne açar (yalnız program dosyaları; Veriler ve runtime
değişmez). Program 1.20 olarak çalışmaya devam eder; açılışta bu pencere "Yeni kurulum gerekli" der:
  "İndir ve kur" → GitHub Releases latest.json → win-setup (kurulum exe'si) indirilir (yüzde · MB · kalan · hız), SHA-256 doğrulanır,
  veri klasörü işareti bırakılır (%APPDATA%\\AlacakVerecek\\veri-konumu.txt → yeni sürüm aynı kayıtları açar), kurulum başlatılır,
  bu program kapanır. "Daha sonra" → eski program olduğu gibi çalışır (pencere sonraki açılışta yine gelir).
Yalnız standart kütüphane + PySide6 (eski taşınabilir runtime'da ne varsa).
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request

REPO = "departures-mil/bereket-defter"
MANIFEST = f"https://github.com/{REPO}/releases/latest/download/latest.json"
SAYFA = f"https://github.com/{REPO}/releases/latest"
POINTER = "veri-konumu.txt"

M = {
    "tr": {"baslik": "Yeni kurulum gerekli",
           "p1": "Bereket Defter {v} yeni bir kurulum programıyla gelir: yeni görünüm (renk şemaları, koyu/açık tema, yazı boyutu), tek tuşla "
                 "güncelleme (yalnızca değişen kısımlar iner) ve kayıtlar için arşiv. Bir kez kurun; sonraki güncellemeler kendiliğinden gelir.",
           "p2": "✓ Kayıtlarınız korunur: kişiler, kayıtlar, belgeler, hatırlatıcılar ve eşitleme bilgileri aynı yerde kalır; yeni sürüm "
                 "onları kendiliğinden açar.",
           "p3": "\"İndir ve kur\" kurulum dosyasını indirir, bu programı kapatır ve kurulumu başlatır. Masaüstüne yeni \"Bereket Defter\" "
                 "kısayolu eklenir; eski kısayolu sonra silebilirsiniz.",
           "kur": "İndir ve kur", "sonra": "Daha sonra", "sayfa": "Sürümler sayfası", "iniyor": "Kurulum dosyası indiriliyor",
           "kalan": "kalan", "hata": "Kurulum dosyası indirilemedi ({e}). Sürümler sayfasından indirebilirsiniz.",
           "dogrula": "Doğrulanıyor…", "basliyor": "Kurulum başlatılıyor…"},
    "en": {"baslik": "New installer required",
           "p1": "Bereket Defter {v} comes with a new installer: a new look (colour schemes, dark/light theme, font size), one-click updates "
                 "(only the changed parts are downloaded) and an archive for records. Install it once; later updates arrive automatically.",
           "p2": "✓ Your records are kept: people, records, documents, reminders and sync details stay where they are and the new version "
                 "opens them automatically.",
           "p3": "\"Download and install\" downloads the installer, closes this program and starts the installation. A new \"Bereket Defter\" "
                 "desktop shortcut is added; you may delete the old one later.",
           "kur": "Download and install", "sonra": "Later", "sayfa": "Releases page", "iniyor": "Downloading the installer",
           "kalan": "left", "hata": "The installer could not be downloaded ({e}). You can download it from the releases page.",
           "dogrula": "Verifying…", "basliyor": "Starting the installer…"},
    "ar": {"baslik": "يلزم مثبّت جديد",
           "p1": "يأتي Bereket Defter {v} بمثبّت جديد: مظهر جديد (أنظمة ألوان، سمة داكنة/فاتحة، حجم الخط)، وتحديث بضغطة واحدة (تُنزَّل "
                 "الأجزاء المتغيرة فقط)، وأرشيف للسجلات. ثبّته مرة واحدة؛ وستصل التحديثات التالية تلقائياً.",
           "p2": "✓ سجلاتك محفوظة: الأشخاص والسجلات والمستندات والتذكيرات وبيانات المزامنة تبقى في مكانها ويفتحها الإصدار الجديد تلقائياً.",
           "p3": "زر «تنزيل وتثبيت» ينزّل ملف التثبيت ويغلق هذا البرنامج ويبدأ التثبيت. يُضاف اختصار جديد باسم «Bereket Defter» على سطح "
                 "المكتب، ويمكنك حذف الاختصار القديم لاحقاً.",
           "kur": "تنزيل وتثبيت", "sonra": "لاحقاً", "sayfa": "صفحة الإصدارات", "iniyor": "جارٍ تنزيل ملف التثبيت",
           "kalan": "متبقٍ", "hata": "تعذّر تنزيل ملف التثبيت ({e}). يمكنك تنزيله من صفحة الإصدارات.",
           "dogrula": "جارٍ التحقق…", "basliyor": "جارٍ بدء التثبيت…"},
}


def dil():
    try:
        import i18n
        l = i18n.lang()
        return l if l in M else "tr"
    except Exception:
        return "tr"


def veri_klasoru():
    try:
        import db
        return db.data_dir()
    except Exception:
        return os.environ.get("AV_DATA_DIR") or ""


def isaret_birak(d):
    """Eski kurulumun veri klasörü varsayılan değilse yeni kurulum aynı klasörü açsın (db.data_dir okur)."""
    if not d:
        return
    base = os.path.join(os.environ.get("APPDATA") or os.path.expanduser("~"), "AlacakVerecek")
    if os.path.normcase(os.path.abspath(d)) == os.path.normcase(os.path.abspath(base)):
        return
    os.makedirs(base, exist_ok=True)
    tmp = os.path.join(base, POINTER + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(os.path.abspath(d))
    os.replace(tmp, os.path.join(base, POINTER))


def _ac(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "BereketDefter-kopru", "Accept-Encoding": "identity"})
    return urllib.request.urlopen(req, timeout=timeout)


def manifest():
    with _ac(MANIFEST, 30) as r:
        m = json.loads(r.read().decode("utf-8"))
    a = (m.get("assets") or {}).get("win-setup") or {}
    if not a.get("file") or len(str(a.get("sha256") or "")) != 64:
        raise RuntimeError("NO_SETUP")
    url = f"https://github.com/{REPO}/releases/download/v{m['version']}/{a['file']}"
    return m["version"], url, int(a.get("size") or 0), str(a["sha256"]).lower(), a["file"]


def indir(url, size, sha, hedef, ilerleme):
    h, done, t0 = hashlib.sha256(), 0, time.monotonic()
    with _ac(url, 120) as r, open(hedef + ".part", "wb") as f:
        total = size or int(r.headers.get("Content-Length") or 0)
        while True:
            b = r.read(262144)
            if not b:
                break
            f.write(b)
            h.update(b)
            done += len(b)
            ilerleme(done, total, done / max(time.monotonic() - t0, 0.05))
    if h.hexdigest() != sha or (size and done != size):
        os.remove(hedef + ".part")
        raise RuntimeError("BAD_HASH")
    os.replace(hedef + ".part", hedef)


def goster(parent=None, surum="1.21.0"):
    from PySide6.QtCore import Qt, QTimer, QUrl
    from PySide6.QtGui import QDesktopServices
    from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel, QProgressBar, QPushButton, QVBoxLayout)
    T = M[dil()]
    d = QDialog(parent)
    d.setWindowTitle(T["baslik"])
    d.setMinimumWidth(620)
    if dil() == "ar":
        d.setLayoutDirection(Qt.RightToLeft)
    v = QVBoxLayout(d)
    h = QLabel(T["baslik"])
    h.setStyleSheet("font-size:20px;font-weight:700;color:#06513f;")
    v.addWidget(h)
    for k in ("p1", "p2", "p3"):
        l = QLabel(T[k].format(v=surum))
        l.setWordWrap(True)
        if k == "p2":
            l.setStyleSheet("background:#e3f6ee;color:#06513f;padding:10px;border-radius:10px;font-weight:600;")
        v.addWidget(l)
    bar = QProgressBar()
    bar.setRange(0, 1000)
    bar.hide()
    durum = QLabel()
    durum.setWordWrap(True)
    v.addWidget(bar)
    v.addWidget(durum)
    row = QHBoxLayout()
    b_sayfa = QPushButton(T["sayfa"])
    b_sonra = QPushButton(T["sonra"])
    b_kur = QPushButton(T["kur"])
    b_kur.setDefault(True)
    row.addWidget(b_sayfa)
    row.addStretch(1)
    row.addWidget(b_sonra)
    row.addWidget(b_kur)
    v.addLayout(row)
    b_sayfa.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(SAYFA)))
    b_sonra.clicked.connect(d.reject)
    st = {"p": None, "bitti": None, "hata": None}

    def ilerleme(done, total, bps):
        st["p"] = (done, total, bps)

    def is_parcacigi():
        try:
            ver, url, size, sha, ad = manifest()
            hedef = os.path.join(tempfile.gettempdir(), ad)
            indir(url, size, sha, hedef, ilerleme)
            st["bitti"] = hedef
        except Exception as e:  # ağ / doğrulama
            st["hata"] = str(e) or e.__class__.__name__

    def tik():
        p = st["p"]
        if p:
            done, total, bps = p
            mb = lambda x: f"{x / 1048576:.1f}".replace(".", "," if dil() == "tr" else ".")
            if total:
                bar.setValue(int(done * 1000 / total))
                durum.setText(f"{T['iniyor']} · %{done * 100 // total} · {mb(done)} / {mb(total)} MB · {T['kalan']} "
                              f"{mb(max(total - done, 0))} MB · {mb(bps)} MB/sn")
        if st["hata"]:
            timer.stop()
            durum.setText(T["hata"].format(e=st["hata"]))
            b_kur.setEnabled(True)
            b_sonra.setEnabled(True)
        elif st["bitti"]:
            timer.stop()
            durum.setText(T["basliyor"])
            try:
                isaret_birak(veri_klasoru())
            except OSError:
                pass
            try:
                flags = 0x00000008 | 0x00000200 if sys.platform == "win32" else 0
                subprocess.Popen([st["bitti"]], close_fds=True, creationflags=flags) if sys.platform == "win32" else \
                    subprocess.Popen([st["bitti"]], close_fds=True, start_new_session=True)
            except OSError as e:
                durum.setText(T["hata"].format(e=e))
                b_kur.setEnabled(True)
                b_sonra.setEnabled(True)
                return
            d.accept()
            app = QApplication.instance()
            for w in app.topLevelWidgets():
                setattr(w, "restarting", True)   # eski programın "çıkmak istiyor musunuz?" sorusu sorulmasın
            QTimer.singleShot(300, app.quit)

    timer = QTimer(d)
    timer.setInterval(200)
    timer.timeout.connect(tik)

    def kur():
        b_kur.setEnabled(False)
        b_sonra.setEnabled(False)
        bar.show()
        bar.setValue(0)
        durum.setText(T["iniyor"] + "…")
        st.update(p=None, bitti=None, hata=None)
        threading.Thread(target=is_parcacigi, daemon=True).start()
        timer.start()
    b_kur.clicked.connect(kur)
    d.exec()
