"""Eski kanal köprüsü: 1.20 taşınabilir kurulumu raw masaustu.json → bu paket → "Yeni kurulum gerekli" → kurulum exe'si."""
import hashlib
import http.server
import io
import os
import subprocess
import sys
import threading
import zipfile

import pytest

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "araclar"))


def _git_var():
    try:
        subprocess.run(["git", "-C", KOK, "cat-file", "-e", "69e624f^{commit}"], check=True, capture_output=True)
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _git_var(), reason="1.20 commit'i yok (sığ klon)")
def test_kopru_paketi_eski_programda_acilir(tmp_path):
    import kopru
    data = kopru.masaustu_paketi("1.21.0")
    app = tmp_path / "app"
    zipfile.ZipFile(io.BytesIO(data)).extractall(app)
    # eski güncelleyici (1.20 guncelle.py) paketi kabul eder ve sürümü daha yeni görür
    sys.path.insert(0, str(app))
    try:
        import guncelle
        assert guncelle.is_newer("1.21.0", "1.20")
        assert "main.py" in zipfile.ZipFile(io.BytesIO(data)).namelist()
    finally:
        sys.path.remove(str(app))
    kod = r'''
import os, sys
sys.argv = ["x"]
import kurulum_kopru, main
from PySide6.QtWidgets import QApplication
def goster(w, v):
    open(os.environ["SONUC"], "w").write(v)
    w.restarting = True   # eski programın çıkış sorusu (kurulum_kopru da aynısını yapar)
    QApplication.instance().quit()
kurulum_kopru.goster = goster
main.main()
'''
    env = dict(os.environ, AV_DATA_DIR=str(tmp_path / "Veriler"), QT_QPA_PLATFORM="offscreen", SONUC=str(tmp_path / "s"),
               APPDATA=str(tmp_path / "ad"))
    r = subprocess.run([sys.executable, "-c", kod], cwd=str(app), env=env, capture_output=True, text=True, timeout=120)
    assert (tmp_path / "s").exists(), r.stdout + r.stderr
    assert (tmp_path / "s").read_text() == "1.21.0"


def test_kurulum_indirme_ve_veri_isareti(tmp_path, monkeypatch):
    sys.path.insert(0, os.path.join(KOK, "kopru"))
    import kurulum_kopru as k
    body = b"MZ kurulum" * 1000
    (tmp_path / "srv").mkdir()
    (tmp_path / "srv" / "s.exe").write_bytes(body)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(tmp_path / "srv"), **kw)

        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}/s.exe"
    seen = []
    hedef = str(tmp_path / "out.exe")
    k.indir(url, len(body), hashlib.sha256(body).hexdigest(), hedef, lambda d, t, b: seen.append((d, t)))
    assert open(hedef, "rb").read() == body and seen[-1] == (len(body), len(body))
    with pytest.raises(RuntimeError):
        k.indir(url, len(body), "0" * 64, str(tmp_path / "bad.exe"), lambda *a: None)
    assert not os.path.exists(str(tmp_path / "bad.exe"))
    srv.shutdown()
    monkeypatch.setenv("APPDATA", str(tmp_path / "ad"))
    k.isaret_birak(str(tmp_path / "Tasinabilir" / "Veriler"))
    assert open(tmp_path / "ad" / "AlacakVerecek" / "veri-konumu.txt", encoding="utf-8").read().endswith("Veriler")
