"""Masaüstü ekran görüntüleri (offscreen Qt): python3 araclar/ekran.py <klasör>
tr-falcon-dark, ar-falcon-light, tr-klasik (Defter + Ayarlar sayfaları; örnek kayıtlarla, gerçek veriye dokunmaz)."""
import json
import os
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KOD = r'''
import os, sys, json
sys.argv = ["x"]
import main, fccore
from db import DB
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
d = DB()
if not d.persons():
    p1 = d.add_person("Ahmet Yılmaz", "+90 555 111 22 33"); d.set_channel(p1, "wa", True); d.set_channel(p1, "call", True)
    p2 = d.add_person("محمد الأحمد", "+963 944 000 000"); d.set_channel(p2, "tg", True)
    p3 = d.add_person("Ayşe Demir", "")
    d.add_tx(p1, "2026-11-20 10:15:00", "VERDIM", "USD", 250, "Kira avansı")
    d.add_tx(p1, "2026-11-22 16:40:00", "ALDIM", "USD", 100, "Kısmi ödeme")
    d.add_tx(p2, "2026-11-21 12:00:00", "VERDIM", "SYP", 1500000, "Malzeme")
    d.add_tx(p3, "2026-11-23 09:30:00", "ALDIM", "TRY", 4500, "Borç ödemesi")
    d.add_reminder(p1, "TAHSIL", "USD", 150, "2026-11-24 09:00", "Kalan ödeme")
    t = d.add_tx(p3, "2026-11-24 11:00:00", "VERDIM", "TRY", 800, "Silinen deneme"); d.delete_tx(t)
fccore.storage.use(d.dir, app="bereket-defter")
o = json.loads(os.environ["EKRAN"])
for k, v in o["st"].items():
    fccore.storage.set(k, v)
orig = main.build_app
def wrap(*x, **k):
    win, shell = orig(*x, **k)
    def shot(i=0):
        win.showNormal(); win.resize(1440, 900)
        def g():
            if i < len(o["pages"]):
                shell.show_page(o["pages"][i])
                QTimer.singleShot(500, lambda: (win.grab().save(o["out"] + "-" + o["pages"][i] + ".png"), shot(i + 1)))
            else:
                win.quitting = True; QApplication.instance().quit()
        QTimer.singleShot(400, g)
    QTimer.singleShot(2500, shot)
    return win, shell
main.build_app = wrap
sys.exit(main.main())
'''


def main():
    out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "ekran")
    os.makedirs(out, exist_ok=True)
    for ad, st in (("tr-falcon-dark", {"lang": "tr", "scheme": "falcon", "theme": "dark"}),
                   ("ar-falcon-light", {"lang": "ar", "scheme": "falcon", "theme": "light"}),
                   ("tr-klasik", {"lang": "tr", "scheme": "klasik", "theme": "light"})):
        st.update({"onboarding.done": True, "whatsnew.seen": "9.9.9"})
        veri = tempfile.mkdtemp()
        env = dict(os.environ, AV_DATA_DIR=veri, QT_QPA_PLATFORM="offscreen",
                   EKRAN=json.dumps({"st": st, "out": os.path.join(out, "masaustu-" + ad), "pages": ["defter", "ayarlar"]}))
        r = subprocess.run([sys.executable, "-c", KOD], cwd=os.path.join(KOK, "masaustu"), env=env, capture_output=True, text=True, timeout=120)
        print(ad, "ok" if r.returncode == 0 else r.stderr[-800:])


if __name__ == "__main__":
    main()
