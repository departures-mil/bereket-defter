"""Bereket Defter masaüstü: veri kuralları (arşiv / çakışma yedeği / veri klasörü) + ortak çekirdek kabuğu duman testi (offscreen Qt)."""
import json
import os
import re
import subprocess
import sys

import pytest

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture()
def veri(tmp_path, monkeypatch):
    monkeypatch.setenv("AV_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("APPDATA", str(tmp_path / "appdata"))
    import db as dbm
    d = dbm.DB(str(tmp_path / "veriler.db"))
    yield d
    d.con.close()


def _kisi_kayit_belge(d, tmp_path):
    pid = d.add_person("Ahmet", "0555")
    tid = d.add_tx(pid, "2026-11-24 10:00:00", "VERDIM", "USD", 25.5, "deneme")
    src = tmp_path / "fis.jpg"
    src.write_bytes(b"\xff\xd8\xff resim")
    d.add_photo(tid, str(src))
    d.add_reminder(pid, "TAHSIL", "USD", 25.5, "2026-12-01 09:00", "hatırlat")
    return pid, tid


def test_yerel_silme_arsivlenir_ve_geri_alinir(veri, tmp_path):
    d = veri
    pid, tid = _kisi_kayit_belge(d, tmp_path)
    uid = d.person(pid)["uid"]
    foto = d.photos(tid)[0]
    yol = d.photo_path(foto)
    assert os.path.isfile(yol)
    d.delete_person(pid)
    assert d.person(pid) is None
    assert not os.path.exists(yol)                                   # canlı yerden kalktı …
    assert os.path.isfile(os.path.join(d.photo_dir, "arsiv", foto["file"]))   # … ama silinmedi
    a = d.archived()
    assert len(a) == 1 and a[0]["tur"] == "persons" and a[0]["kaynak"] == "yerel"
    assert d.restore(a[0]["id"])
    p = d.con.execute("SELECT * FROM persons WHERE uid=?", (uid,)).fetchone()
    assert p is not None and p["dirty"] == 1                         # aynı kimlik, yeniden gönderilecek
    t = d.con.execute("SELECT * FROM transactions WHERE person_id=?", (p["id"],)).fetchall()
    assert len(t) == 1 and t[0]["amount"] == 25.5
    ph = d.photos(t[0]["id"])
    assert len(ph) == 1 and os.path.isfile(d.photo_path(ph[0]))
    assert len(d.reminders(p["id"])) == 1
    assert d.con.execute("SELECT COUNT(*) FROM tombstones WHERE uid=?", (uid,)).fetchone()[0] == 0
    assert d.archived() == []


def test_uzak_silme_kalici_silmez_arsivler(veri, tmp_path):
    import sync
    d = veri
    pid, tid = _kisi_kayit_belge(d, tmp_path)
    d.con.execute("UPDATE persons SET dirty=0")
    d.con.execute("UPDATE transactions SET dirty=0")
    d.con.commit()
    eng = sync.SyncEngine(d.dir, d.path, autostart=False)
    eng._db = d
    tuid = d.tx(tid)["uid"]
    r = eng._apply(d.con, "tx", tuid, sync.Doc({"id": {"stringValue": tuid}, "m": {"integerValue": str(10 ** 15)},
                                                  "del": {"booleanValue": True}}))
    d.con.commit()
    assert r == "changed"
    assert d.tx(tid) is None
    a = d.archived()
    assert a and a[0]["kaynak"] == "uzak" and a[0]["tur"] == "tx"
    snap = json.loads(a[0]["veri"])
    assert snap["tx"][0]["description"] == "deneme" and len(snap["tx"][0]["photos"]) == 1
    assert d.restore(a[0]["id"])
    assert len(d.transactions(pid)) == 1


def test_cakismada_eski_hal_yedeklenir(veri, tmp_path):
    import sync
    d = veri
    pid = d.add_person("Ayşe", "1")
    uid = d.person(pid)["uid"]
    m = d.person(pid)["m"]
    eng = sync.SyncEngine(d.dir, d.path, autostart=False)
    eng._db = d
    f = {"id": {"stringValue": uid}, "m": {"integerValue": str(m + 5)}, "del": {"booleanValue": False},
         "name": {"stringValue": "Ayşe Yılmaz"}, "phone": {"stringValue": "2"}}
    assert eng._apply(d.con, "persons", uid, sync.Doc(f)) == "changed"
    d.con.commit()
    assert d.person(pid)["name"] == "Ayşe Yılmaz"                      # yeni olan kaldı
    c = d.conflicts()
    assert len(c) == 1 and json.loads(c[0]["veri"])["name"] == "Ayşe"  # eski hal yedekte


def test_veri_klasoru_degismez(tmp_path, monkeypatch):
    import db as dbm
    monkeypatch.delenv("AV_DATA_DIR", raising=False)
    monkeypatch.setenv("APPDATA", str(tmp_path / "ad"))
    monkeypatch.setattr(sys, "platform", "win32")
    eski = tmp_path / "Tasinabilir" / "Veriler"
    eski.mkdir(parents=True)
    (eski / "veriler.db").write_bytes(b"")
    assert dbm.data_dir() == os.path.join(str(tmp_path / "ad"), "AlacakVerecek")
    assert dbm.remember_data_dir(str(eski))
    assert dbm.data_dir() == str(eski)
    monkeypatch.setenv("AV_DATA_DIR", str(tmp_path / "x"))
    assert dbm.data_dir() == str(tmp_path / "x")


def test_surum_tutarli():
    r = subprocess.run([sys.executable, os.path.join(KOK, "araclar", "surum_yaz.py"), "--kontrol"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    import surum
    assert re.fullmatch(r"\d+\.\d+\.\d+", surum.APP_VERSION)
    from notlar import NOTES
    assert list(NOTES)[0] == surum.APP_VERSION
    assert all(NOTES[surum.APP_VERSION].get(l) for l in ("tr", "en", "ar"))


def test_cekirdek_kopyasi_kayitli():
    v = open(os.path.join(KOK, "cekirdek", "VERSION"), encoding="utf-8").read()
    assert re.search(r"\b[0-9a-f]{40}\b", v)
    assert os.path.isfile(os.path.join(KOK, "masaustu", "fccore", "updater.py"))
    assert os.path.isfile(os.path.join(KOK, "mobil", "cekirdek", "fc-core.js"))


def test_eski_surum_karsilastirmasi_yeni_surumu_gorur():
    """Kurulu 1.20 (masaüstü guncelle.py / telefon update.js aynı kural) "1.21.0"ı yeni görmeli."""
    def parca(v):
        out = [int("".join(c for c in p if c.isdigit()) or 0) for p in str(v).lstrip("vV").split(".")]
        while out and out[-1] == 0:
            out.pop()
        return tuple(out)
    import surum
    assert parca(surum.APP_VERSION) > parca("1.20")


def test_kabuk_duman(tmp_path, monkeypatch):
    """Gerçek pencere (offscreen): üst çubuk sırası, ayarlar sırası (İletişim EN SON), dil + şema değişimi, Wi‑Fi sunucusu."""
    monkeypatch.setenv("AV_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("APPDATA", str(tmp_path / "appdata"))
    kod = r'''
import os, sys, json
sys.argv = ["x"]
import main, fccore
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QPushButton
sonuc = {}
orig = main.build_app
def kontrol(win, shell):
    a = QApplication.instance()
    tb = shell.topbar
    sonuc["ust"] = [b.property("fcWin") or b.text() for b in tb.actions.findChildren(QPushButton) if b.isVisibleTo(win)]
    sonuc["sync"] = hasattr(tb, "sync_btn") and hasattr(tb, "lan_btn") and hasattr(tb, "upd_btn")
    sonuc["tam"] = win.isFullScreen()
    shell.show_page("ayarlar")
    g = shell.grid
    sonuc["kartlar"] = [w.property("fcKey") or w.objectName() for w in g._items] if hasattr(g, "_items") else []
    sonuc["iletisim_son"] = g.contact is not None
    fccore.i18n.set("ar"); fccore.style.set_scheme("klasik"); fccore.style.set_theme("light")
    sonuc["rtl"] = a.isRightToLeft()
    sonuc["defter"] = shell.defter is not None and shell.defter.isVisible() is not None
    sonuc["lan"] = shell.db.sync_engine.lan_server.running or bool(shell.db.sync_engine.lan_server.error)
    json.dump(sonuc, open(os.environ["SONUC"], "w"))
    win.quitting = True
    a.quit()
def wrap(*x, **k):
    r = orig(*x, **k)
    QTimer.singleShot(1500, lambda: kontrol(*r))
    return r
main.build_app = wrap
fccore.storage.use(os.environ["AV_DATA_DIR"], app="bereket-defter")
fccore.storage.set("onboarding.done", True)
sys.exit(main.main())
'''
    env = dict(os.environ, SONUC=str(tmp_path / "s.json"), QT_QPA_PLATFORM="offscreen", BEREKET_TEST="1")
    r = subprocess.run([sys.executable, "-c", kod], cwd=os.path.join(KOK, "masaustu"), env=env, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
    s = json.load(open(tmp_path / "s.json"))
    assert s["sync"] and s["tam"] and s["rtl"] and s["iletisim_son"] and s["lan"]
    assert s["ust"][-4:] == ["minimize", "half", "fullscreen", "close"], s["ust"]
