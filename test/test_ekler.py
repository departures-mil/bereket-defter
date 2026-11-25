"""v1.22 ekleri: PIN, otomatik yedek, yedekten eksikleri geri getirme (silmez / üzerine yazmaz), raporlar, CSV, hızlı kayıt,
mesajlar, senet, taksitler, etiketlerin eşitlemeye girmesi."""
import os
from datetime import datetime

import pytest


@pytest.fixture()
def veri(tmp_path, monkeypatch):
    monkeypatch.setenv("AV_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("APPDATA", str(tmp_path / "appdata"))
    import db as dbm
    d = dbm.DB(str(tmp_path / "veriler.db"))
    yield d
    d.con.close()


def test_pin_ve_ayarlar(tmp_path):
    import ekler_cekirdek as E
    k = E.pin_kaydi("4321")
    assert E.pin_dogru(k, "4321") and not E.pin_dogru(k, "1234") and not E.pin_dogru(None, "4321")
    assert E.pin_gecerli("1234") and E.pin_gecerli("12345678") and not E.pin_gecerli("12a4") and not E.pin_gecerli("123")
    a = E.ayar_oku(str(tmp_path))
    assert a["oto_yedek"] is True and a["pin"] is None
    a["pin"] = k
    a["kurlar"] = {"TRY": 34.5, "SYP": 13000}
    E.ayar_yaz(str(tmp_path), a)
    b = E.ayar_oku(str(tmp_path))
    assert E.pin_dogru(b["pin"], "4321") and b["kurlar"]["TRY"] == 34.5


def test_oto_yedek_gunde_bir_ve_eski_silinir(veri):
    import ekler_cekirdek as E
    veri.add_person("A")
    for g in range(1, 6):
        assert E.oto_yedek(veri, sakla=3, bugun=f"2026-11-0{g}")
    assert E.oto_yedek(veri, sakla=3, bugun="2026-11-05") is None      # aynı gün ikinci kez alınmaz
    adlar = sorted(f for f in os.listdir(E.yedek_klasoru(veri.dir)) if f.startswith("otomatik_"))
    assert adlar == ["otomatik_2026-11-03.zip", "otomatik_2026-11-04.zip", "otomatik_2026-11-05.zip"]


def test_yedekten_eksikleri_getir_silmez_uzerine_yazmaz(veri, tmp_path):
    import ekler_cekirdek as E
    p = veri.add_person("Ahmet")
    t = veri.add_tx(p, "2026-11-01 10:00:00", "VERDIM", "USD", 100, "eski")
    src = tmp_path / "fis.jpg"
    src.write_bytes(b"\xff\xd8 resim")
    veri.add_photo(t, str(src))
    veri.add_reminder(p, "TAHSIL", "USD", 100, "2026-12-01 09:00", "")
    yol = str(tmp_path / "y.zip")
    veri.backup(yol)
    # yedekten sonra: kayıt silindi, kişi değişti, yeni kayıt eklendi
    veri.delete_tx(t)
    veri.update_person(p, "Ahmet Yeni", "", "")
    t2 = veri.add_tx(p, "2026-11-02 10:00:00", "ALDIM", "USD", 30, "yeni")
    o = E.yedek_ozet(veri, yol)
    assert o["kisi"] == 1 and o["kisi_eksik"] == 0 and o["kayit_eksik"] == 1 and o["belge_eksik"] == 1
    s = E.yedekten_eksikleri_getir(veri, yol)
    assert s == {"kisi": 0, "kayit": 1, "hatirlatici": 0, "belge": 1}
    assert veri.person(p)["name"] == "Ahmet Yeni"                       # var olana dokunulmadı
    assert veri.tx(t2) is not None                                      # yeni kayıt duruyor
    tx = veri.transactions(p)
    assert sorted(r["description"] for r in tx) == ["eski", "yeni"]
    eski = [r for r in tx if r["description"] == "eski"][0]
    assert eski["dirty"] == 1 and len(veri.photos(eski["id"])) == 1 and os.path.isfile(veri.photo_path(veri.photos(eski["id"])[0]))
    assert veri.con.execute("SELECT COUNT(*) FROM tombstones WHERE uid=?", (eski["uid"],)).fetchone()[0] == 0
    assert E.yedekten_eksikleri_getir(veri, yol) == {"kisi": 0, "kayit": 0, "hatirlatici": 0, "belge": 0}


def test_rapor(veri):
    import ekler_cekirdek as E
    a = veri.add_person("Ali")
    b = veri.add_person("Veli")
    veri.add_tx(a, "2026-01-10 10:00:00", "VERDIM", "USD", 500, "")
    veri.add_tx(a, "2026-11-20 10:00:00", "ALDIM", "USD", 100, "")
    veri.add_tx(b, "2026-11-01 10:00:00", "ALDIM", "TRY", 3450, "")
    veri.add_reminder(a, "TAHSIL", "USD", 400, "2026-11-01 09:00", "")
    r = E.rapor(veri, {"TRY": 34.5}, bugun=datetime(2026, 11, 25))
    assert r["ozet"]["USD"]["alacak"] == 400 and r["ozet"]["TRY"]["verecek"] == 3450
    assert r["toplam_usd"] == pytest.approx(400 - 100) and r["eksik_kur"] == []
    assert r["yas"]["USD"]["alacak"]["0-30"] == 400                     # son hareket 20.11 → 5 gün
    assert r["en_alacak"][0]["ad"] == "Ali" and r["en_verecek"][0]["ad"] == "Veli"
    assert len(r["hareket"]["USD"]) == 12 and r["hareket"]["USD"][-1] == ("2026-11", 0.0, 100.0)
    assert len(r["geciken"]) == 1 and E.gecikmis_kisiler(veri, "2026-11-25 00:00") == {a}


def test_csv_gidis_donus(veri, tmp_path):
    import ekler_cekirdek as E
    a = veri.add_person("Ali")
    veri.add_tx(a, "2026-11-01 10:00:00", "VERDIM", "USD", 1234.5, "kira; avans")
    metin = E.csv_disa(veri, "tr")
    assert metin.startswith("﻿") and "1234,50" in metin
    coz = E.csv_cozumle(metin, veri)
    assert len(coz["satirlar"]) == 1 and coz["satirlar"][0]["yinelenen"]   # aynı kayıt ikinci kez eklenmez
    yeni = "Date,Person,Type,Currency,Amount,Description\n2026-11-03,Can,Received,TRY,\"1,500.00\",x\n05.11.2026,Ali,gave,$,20,\n" \
           "bozuk,Ali,gave,USD,1,\n"
    coz = E.csv_cozumle(yeni, veri)
    assert [s["amount"] for s in coz["satirlar"]] == [1500.0, 20.0] and coz["yeni_kisiler"] == {"Can"}
    assert coz["hatalar"] == [(4, "tarih")]
    assert E.csv_ice_al(veri, coz) == (2, 1)
    assert veri.balances(a)["USD"][2] == pytest.approx(1254.5)


@pytest.mark.parametrize("metin,beklenen", [
    ("Ahmet'e 500 TL verdim", ("Ahmet Yılmaz", "VERDIM", "TRY", 500)),
    ("Ali'den 1.500 dolar aldım kira için", ("Ali", "ALDIM", "USD", 1500)),
    ("Ali bana 300 lira ödedi", ("Ali", "ALDIM", "TRY", 300)),
    ("received 200$ from Ali", ("Ali", "ALDIM", "USD", 200)),
    ("gave John 20 usd for lunch", ("John", "VERDIM", "USD", 20)),
    ("أعطيت محمد 100 دولار", ("محمد", "VERDIM", "USD", 100)),
    ("استلمت من خالد 5000 ليرة سورية", ("خالد", "ALDIM", "SYP", 5000)),
    ("Ahmet 2 bin TL verdi", ("Ahmet Yılmaz", "ALDIM", "TRY", 2000)),
])
def test_hizli_kayit(metin, beklenen):
    import ekler_cekirdek as E
    s = E.hizli_ayristir(metin, [(1, "Ahmet Yılmaz"), (2, "Ali"), (3, "محمد")])
    assert (s["ad"], s["direction"], s["currency"], s["amount"]) == beklenen


def test_mesaj_senet_taksit():
    import ekler_cekirdek as E
    m = E.mesaj_metni("bakiye", "tr", "Ali", {"USD": 150, "TRY": -50, "SYP": 0}, "Deniz", "25.11.2026")
    assert "Bana olan borcunuz: 150,00 $" in m and "Size olan borcum: 50,00 ₺" in m and "Onaylıyorum" in m and m.endswith("Deniz")
    assert "bekleme" in E.mesaj_metni("hatirlat", "tr", "Ali", {"USD": 10})
    assert "Confirmed" in E.mesaj_metni("hatirlat", "en", "Ali", {"USD": -10})       # borç yoksa hatırlatma yerine bakiye
    assert "أُغلق" in E.mesaj_metni("kapandi", "ar", "علي", {})
    h = E.senet_html({"borclu": "Ali <b>", "alacakli": "Veli", "tutar": 1500, "cur": "USD", "vade": "01.01.2027", "sahit1": "Can"}, "tr")
    assert "BORÇ SENEDİ" in h and "1.500,00 $" in h and "Ali &lt;b&gt;" in h and "Bakara" in h
    assert 'dir="rtl"' in E.senet_html({}, "ar")
    p = E.taksitler(1000, 3, datetime(2026, 1, 31, 10, 0))
    assert p == [("2026-01-31 10:00", 333.33), ("2026-02-28 10:00", 333.33), ("2026-03-31 10:00", 333.34)]
    assert [x[0][:10] for x in E.taksitler(100, 2, datetime(2026, 1, 1), "hafta")] == ["2026-01-01", "2026-01-08"]


def test_etiketler_eslenir(veri):
    import sync
    p = veri.add_person("Ali", extra={"tags": "aile, iş"})
    assert veri.person(p)["tags"] == "aile, iş"
    assert [r["name"] for r in veri.persons("aile")] == ["Ali"]
    eng = sync.SyncEngine(veri.dir, veri.path, autostart=False)
    con = eng._con() if hasattr(eng, "_con") else veri.con
    yazilar = eng._row_writes(con)
    f = [w for w, t, *_ in yazilar if t == "persons"][0]["update"]["fields"]
    assert f["tags"] == {"stringValue": "aile, iş"}
