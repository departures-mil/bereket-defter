"""v1.22 ekleri — arayüzsüz mantık (testlenebilir):
güvenlik ayarları + PIN, günlük otomatik yedek, yedek özeti ve "eksikleri geri getir" (hiçbir şeyi silmez, üzerine yazmaz),
raporlar (özet, kur karşılığı, yaşlandırma, en büyük bakiyeler, aylık hareket, gecikenler), CSV dışa / içe aktarma,
hızlı kayıt ayrıştırıcı (internetsiz, tr/en/ar), hazır mesajlar (bakiye + mutabakat, kibar hatırlatma, hesap kapandı),
borç senedi (Bakara 282: yazan ve iki şahit) HTML'i. Telefon tarafındaki karşılığı: mobil/js/ekler.js (aynı kurallar)."""
import csv
import hashlib
import io
import json
import os
import re
import secrets
import shutil
import sqlite3
import tempfile
import zipfile
from datetime import datetime, timedelta

CURRENCIES = ("USD", "TRY", "SYP")
SYMBOLS = {"USD": "$", "TRY": "₺", "SYP": "£S"}
AYAR_DOSYA = "guvenlik.json"          # yalnız bu cihaz (eşitlenmez)
YEDEK_KLASOR = "Yedekler"
VARSAYILAN = {"pin": None, "kilit_dk": 5, "gizle": False, "oto_yedek": True, "yedek_sakla": 10,
              "kurlar": {"TRY": 0.0, "SYP": 0.0}, "ben": ""}


# ---------------------------------------------------------------- ayarlar
def ayar_yolu(veri_dir):
    return os.path.join(veri_dir, AYAR_DOSYA)


def ayar_oku(veri_dir):
    a = json.loads(json.dumps(VARSAYILAN))
    try:
        with open(ayar_yolu(veri_dir), encoding="utf-8") as f:
            d = json.load(f)
        if isinstance(d, dict):
            a.update({k: v for k, v in d.items() if k in VARSAYILAN})
    except (OSError, ValueError):
        pass
    if not isinstance(a.get("kurlar"), dict):
        a["kurlar"] = dict(VARSAYILAN["kurlar"])
    return a


def ayar_yaz(veri_dir, a):
    os.makedirs(veri_dir, exist_ok=True)
    tmp = ayar_yolu(veri_dir) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({k: a.get(k, VARSAYILAN[k]) for k in VARSAYILAN}, f, ensure_ascii=False, indent=1)
    os.replace(tmp, ayar_yolu(veri_dir))


# ---------------------------------------------------------------- PIN (PBKDF2-SHA256; telefonla aynı biçim değil, cihaza özel)
PIN_TUR = 120000


def pin_gecerli(pin):
    return bool(re.fullmatch(r"\d{4,8}", pin or ""))


def pin_kaydi(pin):
    tuz = secrets.token_hex(16)
    return {"tuz": tuz, "tur": PIN_TUR, "ozet": hashlib.pbkdf2_hmac("sha256", pin.encode(), bytes.fromhex(tuz), PIN_TUR).hex()}


def pin_dogru(kayit, pin):
    if not kayit or not pin:
        return False
    try:
        o = hashlib.pbkdf2_hmac("sha256", pin.encode(), bytes.fromhex(kayit["tuz"]), int(kayit.get("tur") or PIN_TUR)).hex()
    except (KeyError, ValueError, TypeError):
        return False
    return secrets.compare_digest(o, kayit.get("ozet", ""))


# ---------------------------------------------------------------- otomatik yedek
def yedek_klasoru(veri_dir):
    d = os.path.join(veri_dir, YEDEK_KLASOR)
    os.makedirs(d, exist_ok=True)
    return d


def oto_yedek(db, sakla=10, bugun=None):
    """Günde bir kez veriler + belgelerin ZIP yedeği (Yedekler/otomatik_YYYY-MM-DD.zip); en yeni `sakla` tanesi kalır.
    Döner: oluşturulan dosyanın yolu ya da None (bugün zaten alınmış)."""
    bugun = bugun or datetime.now().strftime("%Y-%m-%d")
    d = yedek_klasoru(db.dir)
    yol = os.path.join(d, f"otomatik_{bugun}.zip")
    if os.path.isfile(yol):
        return None
    gecici = yol + ".tmp"
    db.backup(gecici)
    os.replace(gecici, yol)
    eski = sorted(f for f in os.listdir(d) if re.fullmatch(r"otomatik_\d{4}-\d\d-\d\d\.zip", f))
    for f in eski[:-max(int(sakla or 1), 1)]:
        try:
            os.remove(os.path.join(d, f))
        except OSError:
            pass
    return yol


def yedekler(veri_dir):
    """[(yol, ad, boyut, değiştirilme zamanı)] en yeni üstte."""
    d = yedek_klasoru(veri_dir)
    out = []
    for f in os.listdir(d):
        if f.lower().endswith(".zip"):
            p = os.path.join(d, f)
            out.append((p, f, os.path.getsize(p), datetime.fromtimestamp(os.path.getmtime(p))))
    return sorted(out, key=lambda x: x[3], reverse=True)


def _yedek_ac(zip_path, klasor):
    with zipfile.ZipFile(zip_path) as z:
        if "veriler.db" not in z.namelist():
            raise ValueError("format")
        z.extract("veriler.db", klasor)
    con = sqlite3.connect(os.path.join(klasor, "veriler.db"))
    con.row_factory = sqlite3.Row
    return con


def _uids(con, tablo):
    try:
        return {r[0] for r in con.execute(f"SELECT uid FROM {tablo} WHERE uid IS NOT NULL AND uid<>''")}
    except sqlite3.Error:
        return set()


def yedek_ozet(db, zip_path):
    """Yedekte kaç kişi / kayıt / hatırlatıcı / belge var ve bunlardan kaçı şu an bu cihazda YOK."""
    with tempfile.TemporaryDirectory() as tmp:
        b = _yedek_ac(zip_path, tmp)
        try:
            out = {}
            for anahtar, tablo in (("kisi", "persons"), ("kayit", "transactions"), ("hatirlatici", "reminders"), ("belge", "photos")):
                yuid = _uids(b, tablo)
                out[anahtar] = len(yuid)
                out[anahtar + "_eksik"] = len(yuid - _uids(db.con, tablo))
            return out
        finally:
            b.close()


def yedekten_eksikleri_getir(db, zip_path):
    """Yedekte olup bu cihazda olmayan kişi, kayıt, hatırlatıcı ve belgeleri geri koyar (aynı kimlik, yeniden eşitlenir).
    Var olan hiçbir kayda dokunmaz, hiçbir şeyi silmez. Döner: {kisi, kayit, hatirlatici, belge} eklenen sayılar."""
    import db as dbm
    say = {"kisi": 0, "kayit": 0, "hatirlatici": 0, "belge": 0}
    con = db.con
    m = dbm.now_ms()

    def kolonlar(tablo):
        return [r[1] for r in con.execute(f"PRAGMA table_info({tablo})")]

    def ekle(tablo, satir, **ust):
        k = [c for c in kolonlar(tablo) if c != "id" and c in satir.keys()]
        v = {c: satir[c] for c in k}
        v.update(ust)
        v.update({"m": m, "dirty": 1})
        cols = list(v)
        cur = con.execute(f"INSERT INTO {tablo}({','.join(cols)}) VALUES({','.join('?' * len(cols))})", [v[c] for c in cols])
        return cur.lastrowid

    def mezar_kaldir(col, uid):
        con.execute("DELETE FROM tombstones WHERE col=? AND uid=?", (col, uid))

    with tempfile.TemporaryDirectory() as tmp:
        b = _yedek_ac(zip_path, tmp)
        try:
            pid_of = {r["uid"]: r["id"] for r in con.execute("SELECT id, uid FROM persons")}
            for p in b.execute("SELECT * FROM persons"):
                if p["uid"] and p["uid"] not in pid_of:
                    pid_of[p["uid"]] = ekle("persons", p)
                    mezar_kaldir("persons", p["uid"])
                    say["kisi"] += 1
            bpid = {r["id"]: r["uid"] for r in b.execute("SELECT id, uid FROM persons")}
            tid_of = {r["uid"]: r["id"] for r in con.execute("SELECT id, uid FROM transactions")}
            for t in b.execute("SELECT * FROM transactions"):
                puid = bpid.get(t["person_id"])
                if t["uid"] and t["uid"] not in tid_of and puid in pid_of:
                    tid_of[t["uid"]] = ekle("transactions", t, person_id=pid_of[puid])
                    mezar_kaldir("tx", t["uid"])
                    say["kayit"] += 1
            var = _uids(con, "reminders")
            for r in b.execute("SELECT * FROM reminders"):
                puid = bpid.get(r["person_id"])
                if r["uid"] and r["uid"] not in var and puid in pid_of:
                    ekle("reminders", r, person_id=pid_of[puid])
                    mezar_kaldir("rem", r["uid"])
                    say["hatirlatici"] += 1
            btid = {r["id"]: r["uid"] for r in b.execute("SELECT id, uid FROM transactions")}
            var = _uids(con, "photos")
            with zipfile.ZipFile(zip_path) as z:
                adlar = set(z.namelist())
                for f in b.execute("SELECT * FROM photos"):
                    tuid = btid.get(f["tx_id"])
                    if not f["uid"] or f["uid"] in var or tuid not in tid_of:
                        continue
                    ad = "fotograflar/" + f["file"]
                    hedef = os.path.join(db.photo_dir, f["file"])
                    if not os.path.exists(hedef):
                        if ad not in adlar:
                            continue
                        os.makedirs(os.path.dirname(hedef), exist_ok=True)
                        with z.open(ad) as kaynak, open(hedef, "wb") as cikti:
                            shutil.copyfileobj(kaynak, cikti)
                    ekle("photos", f, tx_id=tid_of[tuid], blobs_up=0)
                    mezar_kaldir("docs", f["uid"])
                    say["belge"] += 1
        finally:
            b.close()
    con.commit()
    if any(say.values()):
        db._changed()
    return say


# ---------------------------------------------------------------- raporlar
def _gun(ts):
    try:
        return datetime.strptime((ts or "")[:10], "%Y-%m-%d")
    except ValueError:
        return None


def usd_karsiligi(tutar, cur, kurlar):
    """kurlar: {"TRY": 1 USD kaç TL, "SYP": 1 USD kaç £S}. Kur yoksa None."""
    if cur == "USD":
        return tutar
    k = float((kurlar or {}).get(cur) or 0)
    return tutar / k if k > 0 else None


def rapor(db, kurlar=None, bugun=None, ay_sayisi=12):
    """Bütün raporların verisi (masaüstü Raporlar sayfası ve testler)."""
    bugun = bugun or datetime.now()
    con = db.con
    kisi = {r["id"]: r["name"] for r in con.execute("SELECT id, name FROM persons")}
    # kişi × para birimi: bakiye ve son hareket
    bak, son = {}, {}
    aylik = {c: {} for c in CURRENCIES}
    for t in con.execute("SELECT person_id, ts, direction, currency, amount FROM transactions"):
        if t["person_id"] not in kisi or t["currency"] not in CURRENCIES:
            continue
        k = (t["person_id"], t["currency"])
        bak[k] = bak.get(k, 0.0) + (1 if t["direction"] == "VERDIM" else -1) * float(t["amount"] or 0)
        if (t["ts"] or "") > son.get(k, ""):
            son[k] = t["ts"] or ""
        ay = (t["ts"] or "")[:7]
        a = aylik[t["currency"]].setdefault(ay, [0.0, 0.0])
        a[0 if t["direction"] == "VERDIM" else 1] += float(t["amount"] or 0)
    ozet = {c: {"alacak": 0.0, "verecek": 0.0, "net": 0.0, "kisi_alacak": 0, "kisi_verecek": 0} for c in CURRENCIES}
    kovalar = ("0-30", "31-90", "91-180", "180+")
    yas = {c: {"alacak": {k: 0.0 for k in kovalar}, "verecek": {k: 0.0 for k in kovalar}} for c in CURRENCIES}
    satirlar = []
    for (pid, c), b in bak.items():
        if abs(b) < 0.005:
            continue
        o = ozet[c]
        if b > 0:
            o["alacak"] += b
            o["kisi_alacak"] += 1
        else:
            o["verecek"] += -b
            o["kisi_verecek"] += 1
        g = _gun(son.get((pid, c)))
        gun = (bugun - g).days if g else 0
        kova = kovalar[0] if gun <= 30 else kovalar[1] if gun <= 90 else kovalar[2] if gun <= 180 else kovalar[3]
        yas[c]["alacak" if b > 0 else "verecek"][kova] += abs(b)
        satirlar.append({"pid": pid, "ad": kisi[pid], "cur": c, "bakiye": b, "gun": gun, "son": son.get((pid, c), ""),
                         "usd": usd_karsiligi(b, c, kurlar)})
    for c in CURRENCIES:
        ozet[c]["net"] = ozet[c]["alacak"] - ozet[c]["verecek"]

    def sirala(liste):
        return sorted(liste, key=lambda s: -abs(s["usd"]) if s["usd"] is not None else -abs(s["bakiye"]) / 1e9)
    en_alacak = sirala([s for s in satirlar if s["bakiye"] > 0])[:10]
    en_verecek = sirala([s for s in satirlar if s["bakiye"] < 0])[:10]
    toplam_usd, eksik_kur = 0.0, []
    for c in CURRENCIES:
        u = usd_karsiligi(ozet[c]["net"], c, kurlar)
        if u is None:
            if abs(ozet[c]["net"]) >= 0.005:
                eksik_kur.append(c)
        else:
            toplam_usd += u
    aylar = []
    y, m = bugun.year, bugun.month
    for _i in range(ay_sayisi):
        aylar.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    aylar.reverse()
    hareket = {c: [(ay, *aylik[c].get(ay, [0.0, 0.0])) for ay in aylar] for c in CURRENCIES}
    simdi = bugun.strftime("%Y-%m-%d %H:%M")
    geciken = [dict(r) for r in con.execute(
        "SELECT r.*, p.name person_name FROM reminders r JOIN persons p ON p.id=r.person_id WHERE r.done=0 AND r.due<=? "
        "ORDER BY r.due", (simdi,))]
    return {"ozet": ozet, "yas": yas, "kovalar": kovalar, "en_alacak": en_alacak, "en_verecek": en_verecek,
            "toplam_usd": toplam_usd, "eksik_kur": eksik_kur, "hareket": hareket, "geciken": geciken,
            "kisi_sayisi": len(kisi), "kayit_sayisi": con.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]}


def gecikmis_kisiler(db, simdi=None):
    simdi = simdi or datetime.now().strftime("%Y-%m-%d %H:%M")
    return {r[0] for r in db.con.execute("SELECT DISTINCT person_id FROM reminders WHERE done=0 AND due<=?", (simdi,))}


# ---------------------------------------------------------------- CSV
CSV_BASLIK = {"tr": ["Tarih", "Kişi", "İşlem", "Birim", "Tutar", "Açıklama"],
              "en": ["Date", "Person", "Type", "Currency", "Amount", "Description"],
              "ar": ["التاريخ", "الشخص", "العملية", "العملة", "المبلغ", "البيان"]}
ISLEM_AD = {"tr": {"VERDIM": "Verdim", "ALDIM": "Aldım"}, "en": {"VERDIM": "Gave", "ALDIM": "Received"},
            "ar": {"VERDIM": "أعطيت", "ALDIM": "استلمت"}}


def _sayi_yaz(x, dil):
    s = f"{x:.2f}"
    return s.replace(".", ",") if dil == "tr" else s


def csv_disa(db, dil="tr"):
    """Kayıtlar CSV (Excel için UTF-8 BOM, ';' ayraç). Döner: metin."""
    out = io.StringIO()
    w = csv.writer(out, delimiter=";", lineterminator="\r\n")
    w.writerow(CSV_BASLIK.get(dil, CSV_BASLIK["tr"]))
    for t in db.transactions():
        w.writerow([(t["ts"] or "")[:16], t["person_name"], ISLEM_AD.get(dil, ISLEM_AD["tr"])[t["direction"]], t["currency"],
                    _sayi_yaz(float(t["amount"]), dil), t["description"] or ""])
    return "﻿" + out.getvalue()


def csv_bakiyeler(db, dil="tr"):
    out = io.StringIO()
    w = csv.writer(out, delimiter=";", lineterminator="\r\n")
    bas = {"tr": ["Kişi", "Birim", "Verilen", "Alınan", "Bakiye"], "en": ["Person", "Currency", "Given", "Received", "Balance"],
           "ar": ["الشخص", "العملة", "المُعطى", "المأخوذ", "الرصيد"]}
    w.writerow(bas.get(dil, bas["tr"]))
    for p in db.persons():
        bal = db.balances(p["id"])
        for c in CURRENCIES:
            v, a, b = bal[c]
            if v or a:
                w.writerow([p["name"], c, _sayi_yaz(v, dil), _sayi_yaz(a, dil), _sayi_yaz(b, dil)])
    return "﻿" + out.getvalue()


def sayi_oku(s):
    """'1.234,56' / '1,234.56' / '12,5' / '12.5' → float (geçersiz: None)."""
    s = re.sub(r"[\s'$₺£S]", "", str(s or "")).replace("٫", ".").replace("٬", ",")
    s = s.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789"))
    if not s:
        return None
    neg = s.startswith("-")
    s = s.lstrip("+-")
    lc, ld = s.rfind(","), s.rfind(".")
    if lc >= 0 and ld >= 0:
        dec = "," if lc > ld else "."
        s = s.replace("." if dec == "," else ",", "").replace(dec, ".")
    elif lc >= 0 or ld >= 0:
        sep = "," if lc >= 0 else "."
        parts = s.split(sep)
        if len(parts) > 2 or (len(parts[1]) == 3 and len(parts[0]) <= 3 and parts[0] not in ("", "0")):
            s = "".join(parts)           # 1.234.567 / 1.500 → grup ayırıcı
        else:
            s = parts[0] + "." + parts[1]
    if not re.fullmatch(r"\d*\.?\d*", s) or s in ("", "."):
        return None
    v = float(s)
    return -v if neg else v


_ESLES = {"tarih": ("tarih", "date", "التاريخ", "zaman", "time"), "kisi": ("kişi", "kisi", "person", "name", "ad", "الشخص", "الاسم"),
          "islem": ("işlem", "islem", "type", "direction", "العملية", "yön"),
          "birim": ("birim", "currency", "para birimi", "العملة", "cur"), "tutar": ("tutar", "amount", "miktar", "المبلغ"),
          "aciklama": ("açıklama", "aciklama", "description", "note", "not", "البيان", "ملاحظة")}
_VERDIM = ("verdim", "verilen", "çıktı", "cikti", "given", "gave", "out", "lent", "paid", "أعطيت", "دفعت", "صادر", "verdım")
_ALDIM = ("aldım", "aldim", "alınan", "alinan", "girdi", "received", "got", "in", "أخذت", "استلمت", "وارد", "قبضت")
_BIRIM = {"USD": ("usd", "$", "dolar", "dollar", "دولار"), "TRY": ("try", "tl", "₺", "türk lirası", "turkish lira", "ليرة تركية"),
          "SYP": ("syp", "£s", "suriye lirası", "syrian pound", "ليرة سورية", "ل.س")}


def _birim(s):
    s = (s or "").strip().lower()
    for c, ad in _BIRIM.items():
        if s in ad or s.upper() == c:
            return c
    return None


def _tarih(s):
    s = (s or "").strip()
    for f in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%d.%m.%Y %H:%M", "%d.%m.%Y", "%d/%m/%Y %H:%M", "%d/%m/%Y",
              "%Y/%m/%d %H:%M", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, f).strftime("%Y-%m-%d %H:%M")
        except ValueError:
            pass
    return None


def csv_cozumle(metin, db=None):
    """CSV metnini kayıtlara çevirir. Döner: {"satirlar": [{ts, ad, direction, currency, amount, description, yinelenen}],
    "hatalar": [(satır no, neden)], "yeni_kisiler": set}. Hiçbir şey yazmaz."""
    metin = metin.lstrip("﻿")
    ilk = metin.splitlines()[0] if metin.strip() else ""
    ayrac = ";" if ilk.count(";") >= max(ilk.count(","), ilk.count("\t")) and ";" in ilk else ("\t" if "\t" in ilk else ",")
    r = list(csv.reader(io.StringIO(metin), delimiter=ayrac))
    out = {"satirlar": [], "hatalar": [], "yeni_kisiler": set()}
    if not r:
        return out
    bas = [x.strip().lower() for x in r[0]]
    idx = {}
    for k, adlar in _ESLES.items():
        for i, b in enumerate(bas):
            if b in adlar:
                idx[k] = i
                break
    veri = r[1:] if len(idx) >= 3 else r
    if len(idx) < 3:
        idx = {"tarih": 0, "kisi": 1, "islem": 2, "birim": 3, "tutar": 4, "aciklama": 5}
    mevcut = {}
    var_olan = set()
    if db is not None:
        mevcut = {p["name"].strip().lower(): p["id"] for p in db.persons()}
        for t in db.transactions():
            var_olan.add((t["person_name"].strip().lower(), (t["ts"] or "")[:16], t["direction"], t["currency"], round(float(t["amount"]), 2)))
    for no, satir in enumerate(veri, start=2 if veri is not r else 1):
        if not any(x.strip() for x in satir):
            continue

        def al(k):
            i = idx.get(k)
            return satir[i].strip() if i is not None and i < len(satir) else ""
        ts = _tarih(al("tarih"))
        ad = al("kisi")
        tutar = sayi_oku(al("tutar"))
        cur = _birim(al("birim"))
        isl = al("islem").lower()
        if isl in _VERDIM or isl.upper() == "VERDIM":
            yon = "VERDIM"
        elif isl in _ALDIM or isl.upper() == "ALDIM":
            yon = "ALDIM"
        elif tutar is not None and tutar < 0:
            yon = "ALDIM"
        elif tutar is not None and not isl:
            yon = "VERDIM"
        else:
            yon = None
        neden = None
        if not ts:
            neden = "tarih"
        elif not ad:
            neden = "kisi"
        elif tutar is None or abs(tutar) < 0.005:
            neden = "tutar"
        elif not cur:
            neden = "birim"
        elif not yon:
            neden = "islem"
        if neden:
            out["hatalar"].append((no, neden))
            continue
        tutar = round(abs(tutar), 2)
        anahtar = (ad.lower(), ts, yon, cur, tutar)
        yin = anahtar in var_olan
        var_olan.add(anahtar)
        if ad.lower() not in mevcut:
            out["yeni_kisiler"].add(ad)
        out["satirlar"].append({"ts": ts, "ad": ad, "direction": yon, "currency": cur, "amount": tutar,
                                "description": al("aciklama"), "yinelenen": yin})
    return out


def csv_ice_al(db, cozum):
    """csv_cozumle sonucunu yazar (yinelenenler atlanır). Döner: (eklenen kayıt, eklenen kişi)."""
    kisiler = {p["name"].strip().lower(): p["id"] for p in db.persons()}
    n = yeni = 0
    for s in cozum["satirlar"]:
        if s["yinelenen"]:
            continue
        k = s["ad"].strip().lower()
        if k not in kisiler:
            kisiler[k] = db.add_person(s["ad"].strip())
            yeni += 1
        db.add_tx(kisiler[k], s["ts"] + ":00" if len(s["ts"]) == 16 else s["ts"], s["direction"], s["currency"], s["amount"],
                  s["description"])
        n += 1
    return n, yeni


# ---------------------------------------------------------------- hızlı kayıt (internetsiz ayrıştırıcı)
_CUR_KELIME = [
    ("SYP", r"(suriye\s*lira\w*|syrian\s*pounds?|ل\.?\s?س|ليرة\s*سورية|ليرات\s*سورية|\bsyp\b|£s)"),
    ("TRY", r"(türk\s*lira\w*|turkish\s*lira\w*|ليرة\s*تركية|ليرات\s*تركية|\btl\b|\btry\b|₺|\blira\w*)"),
    ("USD", r"(dolar\w*|dollars?|دولار\w*|\busd\b|\$)"),
    ("SYP", r"(ليرة|ليرات)"),
]
_VER_KALIP = [r"\bpaid me\b", r"\bgave me\b", r"\breturned\b", r"\bfrom\b.*\b(received|got)\b",
              r"أعطاني", r"دفع لي", r"ردّ لي", r"رد لي", r"سدد"]
_YON_KALIP = [
    ("ALDIM", r"\b(received|got|collected|borrowed|took)\b"), ("ALDIM", r"(أخذت|استلمت|قبضت|استلفت|استدنت|اقترضت)"),
    ("ALDIM", r"(aldım|aldim|tahsil ettim|geri aldım|ödedi|ödemiş|verdi\b|getirdi|borç aldım)"),
    ("VERDIM", r"(verdim|ödedim|odedim|borç verdim|gönderdim|yolladım)"),
    ("VERDIM", r"\b(gave|lent|paid|sent|loaned)\b"), ("VERDIM", r"(أعطيت|دفعت|أقرضت|أرسلت|سلّمت|سلمت)"),
]
_TR_EKLER = ("'ye", "'ya", "'e", "'a", "'ten", "'tan", "'den", "'dan", "'nin", "'nın", "'nun", "'nün", "'in", "'ın", "'un", "'ün",
             "’e", "’a", "’ye", "’ya", "’den", "’dan", "’ten", "’tan")


def _kucuk(s):
    return (s or "").replace("I", "ı").replace("İ", "i").lower()


def hizli_ayristir(metin, kisiler=()):
    """'Ahmet'e 500 TL verdim', 'received 200$ from Ali', 'أعطيت محمد 100 دولار' → kayıt taslağı.
    Döner: {ad, kisi_id, direction, currency, amount, description} (bulunamayan alan None/"")."""
    s = (metin or "").strip()
    k = _kucuk(s.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")))
    sonuc = {"ad": "", "kisi_id": None, "direction": None, "currency": None, "amount": None, "description": ""}
    # tutar
    m = re.search(r"(?<![\w])(\d{1,3}(?:[.,\s]\d{3})+(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?)(\s*(bin|k|thousand|ألف|الف))?", k)
    if m:
        v = sayi_oku(m.group(1).replace(" ", ""))
        if v is not None and m.group(3):
            v *= 1000
        sonuc["amount"] = round(v, 2) if v else None
    # para birimi
    for c, kal in _CUR_KELIME:
        if re.search(kal, k):
            sonuc["currency"] = c
            break
    # yön (önce "bana ödedi / paid me" gibi ters kalıplar)
    if any(re.search(p, k) for p in _VER_KALIP):
        sonuc["direction"] = "ALDIM"
    else:
        for yon, kal in _YON_KALIP:
            if re.search(kal, k):
                sonuc["direction"] = yon
                break
    # kişi: kayıtlı adlar (en uzun eşleşme)
    en = None
    for kid, ad in kisiler:
        a = _kucuk(ad).strip()
        if a and re.search(r"(?<![\w])" + re.escape(a) + r"(?![\w])", k.replace("’", "'").split("'")[0] + " " + k) and \
                (en is None or len(a) > len(_kucuk(en[1]))):
            en = (kid, ad)
    if en is None:  # ilk ad (soyad olmadan) eşleşmesi
        for kid, ad in kisiler:
            ilk = _kucuk(ad).split()[0] if _kucuk(ad).split() else ""
            if len(ilk) >= 3 and re.search(r"(?<![\w])" + re.escape(ilk) + r"(?![\w])", k):
                en = (kid, ad)
                break
    if en:
        sonuc["kisi_id"], sonuc["ad"] = en
    else:
        mm = re.search(r"([A-ZÇĞİÖŞÜ][\wçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][\wçğıöşü]+)?)\s*['’](?:y?[ea]|[dt][ea]n|n?[ıiuü]n)\b", s)
        if not mm:
            mm = re.search(r"\b(?:to|from|gave|lent|paid|pay)\s+([A-Z][\w]+(?:\s+[A-Z][\w]+)?)", s)
        if not mm:
            mm = re.search(r"(?:^|\s)(?:من|إلى|الى|لـ)\s*([\u0600-\u06ff]{2,})", s) or \
                re.search(r"(?:أعطيت|دفعت|أقرضت|أرسلت|سلمت|سلّمت)\s+(?:ل)?([\u0600-\u06ff]{2,})", s) or \
                re.search(r"^([\u0600-\u06ff]{2,})\s+(?:أعطاني|دفع|رد|ردّ|سدد)", s)
            if mm and re.search(r"^(دولار|ليرة|ليرات|من|إلى)$", mm.group(1)):
                mm = None
        if mm:
            sonuc["ad"] = mm.group(1).strip()
    # açıklama: "... için" / "for ..." / "ثمن/مقابل ..."
    d = re.search(r"((?:[\wçğıöşü]+\s+){0,1}[\wçğıöşü]+)\s+için\b", s, re.I) or re.search(r"\bfor\s+([\w\s]{2,40})$", s, re.I) or \
        re.search(r"(?:ثمن|مقابل|لأجل|من أجل)\s+([\u0600-\u06ff\s]{2,40})", s)
    if d:
        kelimeler = [w for w in d.group(1).split() if not re.search(
            r"^(\d[\d.,]*|tl|usd|try|dolar\w*|lira\w*|verdim|aldım|aldim|ödedim|verdi|ödedi|aldı|borç|bin)$", _kucuk(w))]
        desc = " ".join(kelimeler)
        if sonuc["ad"]:
            desc = re.sub(re.escape(sonuc["ad"]) + r"\S*", "", desc, flags=re.I)
        sonuc["description"] = desc.strip(" ,.-")
    return sonuc


# ---------------------------------------------------------------- hazır mesajlar (bakiye + mutabakat, hatırlatma, hesap kapandı)
def _fmt(x, dil):
    s = f"{abs(x):,.2f}"
    if dil == "tr":
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def _tutar(x, c, dil):
    return f"{_fmt(x, dil)} {SYMBOLS[c]}" if dil != "ar" else f"⁦{_fmt(x, dil)} {SYMBOLS[c]}⁩"


MESAJ = {
    "tr": {"selam": "Merhaba {ad},", "selam_ad_yok": "Merhaba,",
           "bakiye_bas": "{tarih} itibarıyla kayıtlarıma göre aramızdaki hesap durumu şöyledir:",
           "sizin_borc": "• Bana olan borcunuz: {t}", "benim_borc": "• Size olan borcum: {t}",
           "mutabakat": "Kayıtlarınız bununla uyuşuyorsa \"Onaylıyorum\" yazmanız yeterlidir; bir farklılık varsa lütfen bildirin. Teşekkür ederim.",
           "hatirlat": "Umarım iyisinizdir. Kayıtlarıma göre {t} tutarındaki ödemeniz beklemededir. Uygun olduğunuz bir zamanda ödeyebilirseniz memnun olurum. "
                       "Bir aksilik varsa haber vermeniz yeterli; birlikte kolaylık sağlarız.",
           "kapandi": "{tarih} itibarıyla aramızdaki hesap kapanmıştır; kayıtlarıma göre karşılıklı borç kalmamıştır. Güzel muameleniz için teşekkür ederim, Allah bereket versin.",
           "acik_yok": "Kayıtlarıma göre aramızda açık bir hesap bulunmuyor.", "selamlar": "Selamlarımla.", "ve": " ve "},
    "en": {"selam": "Hello {ad},", "selam_ad_yok": "Hello,",
           "bakiye_bas": "According to my records, the balance between us as of {tarih} is as follows:",
           "sizin_borc": "• Amount you owe me: {t}", "benim_borc": "• Amount I owe you: {t}",
           "mutabakat": "If this matches your records, simply reply \"Confirmed\"; if there is any difference, please let me know. Thank you.",
           "hatirlat": "I hope you are well. According to my records, a payment of {t} is outstanding. I would appreciate it if you could settle it at your earliest convenience. "
                       "If there is any difficulty, just let me know and we will find an arrangement together.",
           "kapandi": "As of {tarih}, the account between us is settled; according to my records, neither of us owes the other anything. Thank you for the fair dealing; may God bless it.",
           "acik_yok": "According to my records, there is no open balance between us.", "selamlar": "Kind regards.", "ve": " and "},
    "ar": {"selam": "السلام عليكم {ad}،", "selam_ad_yok": "السلام عليكم،",
           "bakiye_bas": "وفقاً لسجلاتي، فإن الحساب بيننا حتى تاريخ {tarih} كما يلي:",
           "sizin_borc": "• المبلغ المستحق لي عليكم: {t}", "benim_borc": "• المبلغ المستحق لكم عليّ: {t}",
           "mutabakat": "إذا كان ذلك مطابقاً لسجلاتكم فيكفي أن تكتبوا «أوافق»، وإن كان هناك أي اختلاف فأرجو إعلامي. وشكراً لكم.",
           "hatirlat": "أرجو أن تكونوا بخير. وفقاً لسجلاتي، هناك دفعة مستحقة بمبلغ {t}. أكون شاكراً لو تفضلتم بسدادها في الوقت الذي يناسبكم. "
                       "وإن كان هناك أي ظرف فيكفي إعلامي، ونتفق معاً على ما ييسّر الأمر.",
           "kapandi": "اعتباراً من {tarih} أُغلق الحساب بيننا، ووفقاً لسجلاتي لم يبقَ لأيٍّ منا دين على الآخر. أشكركم على حسن المعاملة، بارك الله لكم.",
           "acik_yok": "وفقاً لسجلاتي، لا يوجد رصيد مفتوح بيننا.", "selamlar": "مع خالص التحيات.", "ve": " و"},
}


def mesaj_metni(tur, dil, ad, bakiyeler, ben="", tarih=None):
    """tur: 'bakiye' | 'hatirlat' | 'kapandi'. bakiyeler: {cur: bakiye} (>0: kişi bana borçlu)."""
    L = MESAJ.get(dil, MESAJ["tr"])
    tarih = tarih or datetime.now().strftime("%d.%m.%Y")
    acik = {c: b for c, b in (bakiyeler or {}).items() if abs(b) >= 0.005}
    satir = [L["selam"].format(ad=ad) if ad else L["selam_ad_yok"], ""]
    if tur == "hatirlat":
        borc = {c: b for c, b in acik.items() if b > 0}
        if borc:
            satir.append(L["hatirlat"].format(t=L["ve"].join(_tutar(b, c, dil) for c, b in borc.items())))
        else:
            tur = "bakiye"
    if tur == "kapandi" or (tur == "bakiye" and not acik):
        satir.append(L["kapandi"].format(tarih=tarih) if tur == "kapandi" else L["acik_yok"])
    elif tur == "bakiye":
        satir.append(L["bakiye_bas"].format(tarih=tarih))
        for c, b in acik.items():
            satir.append((L["sizin_borc"] if b > 0 else L["benim_borc"]).format(t=_tutar(b, c, dil)))
        satir += ["", L["mutabakat"]]
    satir += ["", L["selamlar"]]
    if ben:
        satir.append(ben)
    return "\n".join(satir)


# ---------------------------------------------------------------- borç senedi (Bakara 282)
SENET = {
    "tr": {"baslik": "BORÇ SENEDİ", "ayet_not": "“Ey iman edenler! Belirli bir vadeye kadar birbirinize borçlandığınız zaman onu yazın…” (Bakara, 2/282)",
           "metin": "Aşağıda imzası bulunan <b>{borclu}</b>, <b>{alacakli}</b> adlı kişiye <b>{tutar}</b>{yazi} borçlu olduğunu ve bu borcu "
                    "<b>{vade}</b> tarihinde{yer} eksiksiz ödeyeceğini kabul ve beyan eder.",
           "yazi": " (yazıyla: {y})", "yer": ", {y} yoluyla", "tarih": "Düzenlenme tarihi", "vade": "Vade", "tutar": "Tutar", "aciklama": "Açıklama",
           "borclu": "Borçlu", "alacakli": "Alacaklı", "katip": "Yazan (kâtip)", "sahit": "Şahit", "imza": "İmza", "ad": "Ad Soyad",
           "alt": "Bu senet iki nüsha düzenlenmiş, taraflarca okunup imzalanmıştır."},
    "en": {"baslik": "PROMISSORY NOTE (DEBT ACKNOWLEDGEMENT)",
           "ayet_not": "“O you who believe! When you contract a debt for a fixed term, write it down…” (al-Baqarah, 2:282)",
           "metin": "I, the undersigned <b>{borclu}</b>, acknowledge and declare that I owe <b>{alacakli}</b> the sum of <b>{tutar}</b>{yazi}, "
                    "and that I will repay this debt in full on <b>{vade}</b>{yer}.",
           "yazi": " (in words: {y})", "yer": ", by {y}", "tarih": "Date of issue", "vade": "Due date", "tutar": "Amount", "aciklama": "Description",
           "borclu": "Debtor", "alacakli": "Creditor", "katip": "Scribe (written by)", "sahit": "Witness", "imza": "Signature", "ad": "Full name",
           "alt": "This note has been drawn up in two copies, read and signed by the parties."},
    "ar": {"baslik": "سند دين",
           "ayet_not": "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا إِذَا تَدَايَنْتُمْ بِدَيْنٍ إِلَىٰ أَجَلٍ مُسَمًّى فَاكْتُبُوهُ﴾ (البقرة: 282)",
           "metin": "يقرّ الموقّع أدناه <b>{borclu}</b> بأن في ذمته للسيد/ة <b>{alacakli}</b> مبلغاً قدره <b>{tutar}</b>{yazi}، "
                    "ويتعهد بسداده كاملاً بتاريخ <b>{vade}</b>{yer}.",
           "yazi": " (كتابةً: {y})", "yer": "، عن طريق {y}", "tarih": "تاريخ التحرير", "vade": "تاريخ الاستحقاق", "tutar": "المبلغ", "aciklama": "البيان",
           "borclu": "المدين", "alacakli": "الدائن", "katip": "الكاتب", "sahit": "الشاهد", "imza": "التوقيع", "ad": "الاسم الكامل",
           "alt": "حُرّر هذا السند من نسختين، وقرأه الطرفان ووقّعا عليه."},
}


def senet_html(v, dil="tr"):
    """v: borclu, alacakli, tutar(float), cur, yazi, tarih, vade, yer, katip, sahit1, sahit2, aciklama → yazdırılabilir HTML."""
    import html as H
    L = SENET.get(dil, SENET["tr"])
    e = lambda x: H.escape(str(x or ""))  # noqa: E731
    tutar = _tutar(float(v.get("tutar") or 0), v.get("cur") or "USD", dil)
    metin = L["metin"].format(borclu=e(v.get("borclu")) or "…………", alacakli=e(v.get("alacakli")) or "…………", tutar=e(tutar),
                              yazi=L["yazi"].format(y=e(v["yazi"])) if v.get("yazi") else "",
                              vade=e(v.get("vade")) or "…………", yer=L["yer"].format(y=e(v["yer"])) if v.get("yer") else "")
    yon = "rtl" if dil == "ar" else "ltr"
    hiza = "right" if dil == "ar" else "left"

    def kutu(baslik, ad):
        return (f'<td width="33%" style="border:1px solid #333;padding:8px;vertical-align:top;height:90px">'
                f'<b>{e(baslik)}</b><br>{e(L["ad"])}: {e(ad)}<br><br>{e(L["imza"])}:</td>')
    tablo = (f'<table width="100%" cellspacing="0" cellpadding="6" style="border-collapse:collapse;margin-top:10px">'
             f'<tr><td style="border:1px solid #999"><b>{e(L["tutar"])}</b></td><td style="border:1px solid #999">{e(tutar)}</td>'
             f'<td style="border:1px solid #999"><b>{e(L["tarih"])}</b></td><td style="border:1px solid #999">{e(v.get("tarih"))}</td></tr>'
             f'<tr><td style="border:1px solid #999"><b>{e(L["vade"])}</b></td><td style="border:1px solid #999">{e(v.get("vade"))}</td>'
             f'<td style="border:1px solid #999"><b>{e(L["aciklama"])}</b></td><td style="border:1px solid #999">{e(v.get("aciklama"))}</td></tr></table>')
    imzalar = (f'<table width="100%" cellspacing="0" cellpadding="0" style="border-collapse:collapse;margin-top:22px">'
               f'<tr>{kutu(L["borclu"], v.get("borclu"))}{kutu(L["alacakli"], v.get("alacakli"))}{kutu(L["katip"], v.get("katip"))}</tr>'
               f'<tr>{kutu(L["sahit"] + " 1", v.get("sahit1"))}{kutu(L["sahit"] + " 2", v.get("sahit2"))}'
               f'<td width="33%" style="border:0"></td></tr></table>')
    return (f'<!DOCTYPE html><html dir="{yon}" lang="{dil}"><head><meta charset="utf-8"><title>{e(L["baslik"])}</title>'
            f'<style>body{{font-family:"Noto Sans Arabic","Segoe UI",Arial,sans-serif;color:#111;margin:28px;direction:{yon};text-align:{hiza}}}'
            f'h1{{text-align:center;letter-spacing:2px;font-size:22pt;margin:0 0 6px}}.ayet{{text-align:center;color:#06513f;font-size:11pt;margin-bottom:18px}}'
            f'.metin{{font-size:13pt;line-height:1.8;text-align:justify}}.alt{{color:#555;font-size:9.5pt;margin-top:16px;text-align:center}}</style></head>'
            f'<body><h1>{e(L["baslik"])}</h1><div class="ayet">{e(L["ayet_not"])}</div>'
            f'<p class="metin">{metin}</p>{tablo}{imzalar}<p class="alt">{e(L["alt"])}</p></body></html>')


# ---------------------------------------------------------------- taksit planı
def taksitler(toplam, adet, ilk, aralik="ay"):
    """[(vade 'YYYY-MM-DD HH:MM', tutar)] — kuruş farkı son taksitte. aralik: 'ay' | 'hafta' | '15'."""
    adet = max(int(adet), 1)
    pay = round(float(toplam) / adet, 2)
    out = []
    for i in range(adet):
        if aralik == "hafta":
            d = ilk + timedelta(days=7 * i)
        elif aralik == "15":
            d = ilk + timedelta(days=15 * i)
        else:
            y, m = divmod(ilk.month - 1 + i, 12)
            yil, ay = ilk.year + y, m + 1
            gun = min(ilk.day, [31, 29 if yil % 4 == 0 and (yil % 100 or yil % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][ay - 1])
            d = ilk.replace(year=yil, month=ay, day=gun)
        out.append((d.strftime("%Y-%m-%d %H:%M"), pay if i < adet - 1 else round(float(toplam) - pay * (adet - 1), 2)))
    return out
