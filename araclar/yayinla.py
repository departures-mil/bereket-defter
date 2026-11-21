"""Bereket Defter - GitHub güncelleme yayınlayıcı.

Kullanım (depo kökünden):
  python3 araclar/yayinla.py masaustu "<notlar>"
  python3 araclar/yayinla.py mobil    "<notlar>" [--minNative 14] [--apk dosya.apk --apkKod 15]
Sürüm, kaynaktaki APP_VERSION'dan okunur. Paket guncelleme/<kanal>-<kod>.zip olarak yazılır,
bildirge guncelleme/<kanal>.json güncellenir. Sonra: git add -A && git commit && git push
"""
import datetime, hashlib, io, json, os, re, sys, zipfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUN = os.path.join(KOK, "guncelleme")
SKIP_DIRS = {"__pycache__", "_tools"}


def zip_dir(folder):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(folder):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for f in sorted(files):
                if f.endswith(".pyc"):
                    continue
                p = os.path.join(root, f)
                zi = zipfile.ZipInfo(os.path.relpath(p, folder).replace(os.sep, "/"), (2026, 1, 1, 0, 0, 0))
                zi.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(zi, open(p, "rb").read())
    return buf.getvalue()


def surum(kanal):
    if kanal == "masaustu":
        s = open(os.path.join(KOK, "masaustu", "main.py"), encoding="utf-8").read()
        return re.search(r'^APP_VERSION = "([^"]+)"', s, re.M).group(1)
    s = open(os.path.join(KOK, "mobil", "js", "core.js"), encoding="utf-8").read()
    return re.search(r'const APP_VERSION = "([^"]+)"', s).group(1)


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("masaustu", "mobil"):
        raise SystemExit(__doc__)
    kanal, notlar = sys.argv[1], sys.argv[2]
    ver = surum(kanal)
    kod = ver.replace(".", "_")
    data = zip_dir(os.path.join(KOK, kanal))
    os.makedirs(GUN, exist_ok=True)
    dosya = f"{kanal}-{kod}.zip"
    open(os.path.join(GUN, dosya), "wb").write(data)
    yol = os.path.join(GUN, kanal + ".json")
    eski = json.load(open(yol, encoding="utf-8")) if os.path.exists(yol) else {}
    info = {"surum": ver, "kod": kod, "dosya": dosya, "sha256": hashlib.sha256(data).hexdigest(),
            "boyut": len(data), "notlar": notlar, "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
    if kanal == "mobil":
        info["minNative"] = int(arg("--minNative", eski.get("minNative", 14)))
        apk = arg("--apk")
        if apk:
            b = open(apk, "rb").read()
            ad = f"BereketDefter-{arg('--apkKod', kod)}.apk"
            open(os.path.join(GUN, ad), "wb").write(b)
            info.update({"apkKod": arg("--apkKod", kod), "apkDosya": ad, "apkBoyut": len(b),
                         "apkSha256": hashlib.sha256(b).hexdigest()})
        else:
            for k in ("apkKod", "apkDosya", "apkBoyut", "apkSha256"):
                if k in eski:
                    info[k] = eski[k]
    # eski paketleri temizle (bildirgede olmayan aynı kanal zip'leri)
    for f in os.listdir(GUN):
        if f.startswith(kanal + "-") and f.endswith(".zip") and f != dosya:
            os.remove(os.path.join(GUN, f))
    json.dump(info, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("HAZIR", kanal, ver, len(data), "bayt ->", dosya)


if __name__ == "__main__":
    main()
