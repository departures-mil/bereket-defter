"""ESKİ KANAL KÖPRÜSÜ — release'ten SONRA çalıştırılır (imza gerekmez: eski kanal yalnız SHA-256 denetler).

Kullanım (depo kökünden, main'de):  python3 araclar/kopru.py [--apk dosya.apk]
1) GitHub Releases latest.json okunur (win-setup ve android kanalları var olmalı).
2) Masaüstü: 1.20'nin program dosyaları (git: ESKI_REF:masaustu) + kopru/kurulum_kopru.py; main.py'de APP_VERSION = yeni sürüm ve
   açılışta "Yeni kurulum gerekli" penceresi. → guncelleme/masaustu-<kod>.zip + masaustu.json (eski guncelle.py bunu "daha yeni" görür).
3) Telefon: release'teki android APK'sı indirilir (ya da --apk), SHA-256 latest.json ile, imza sertifikası kurulu APK'larınkiyle
   (guncelleme/BereketDefter-16.apk) karşılaştırılır → guncelleme/BereketDefter-<kod>.apk + mobil.json (minNative = yeni versionCode:
   eski update.js APK'yı indirip installApk ile kurar; yeni APK artık GitHub Releases'tan güncellenir).
Sonra: git add -A && git commit && git push (main).
"""
import datetime
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import urllib.request
import zipfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUN = os.path.join(KOK, "guncelleme")
REPO = "departures-mil/bereket-defter"
ESKI_REF = "69e624f"          # Bereket 1.20 (masaüstü 1.20 + Asistan Agent) — eski taşınabilir kurulumun program dosyaları
ESKI_APK = "BereketDefter-16.apk"


def git(*a):
    return subprocess.run(["git", "-C", KOK] + list(a), capture_output=True, check=True).stdout


def al(url):
    req = urllib.request.Request(url, headers={"User-Agent": "BereketDefter-kopru"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def zip_yap(dosyalar):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for ad in sorted(dosyalar):
            zi = zipfile.ZipInfo(ad, (2026, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, dosyalar[ad])
    return buf.getvalue()


def masaustu_paketi(surum):
    names = [n for n in git("ls-tree", "-r", "--name-only", ESKI_REF, "masaustu").decode().split("\n") if n]
    files = {n[len("masaustu/"):]: git("show", f"{ESKI_REF}:{n}") for n in names}
    main = files["main.py"].decode("utf-8")
    main, n1 = re.subn(r'^APP_VERSION = "[^"]+"', f'APP_VERSION = "{surum}"', main, flags=re.M)
    hook = ('        w.showFullScreen()\n'
            '        if first:  # 1.21 köprüsü: "Yeni kurulum gerekli" (kurulum_kopru.py)\n'
            '            QTimer.singleShot(1800, lambda w=w: __import__("kurulum_kopru").goster(w, APP_VERSION))\n')
    main, n2 = re.subn(r'^        w\.showFullScreen\(\)\n', hook, main, count=1, flags=re.M)
    assert n1 == 1 and n2 == 1, "1.20 main.py beklenen biçimde değil"
    files["main.py"] = main.encode("utf-8")
    with open(os.path.join(KOK, "kopru", "kurulum_kopru.py"), "rb") as f:
        files["kurulum_kopru.py"] = f.read()
    return zip_yap(files)


def sertifika(apk):
    out = subprocess.run([sys.executable, os.path.join(KOK, "araclar", "apk.py"), "--sertifika", apk], capture_output=True, text=True)
    return out.stdout.strip().splitlines()[-1] if out.returncode == 0 else ""


def main():
    man = json.loads(al(f"https://github.com/{REPO}/releases/latest/download/latest.json"))
    surum = man["version"]
    kod = surum.replace(".", "_")
    a = man["assets"]
    assert "win-setup" in a and "win-app" in a, "release'te win-setup / win-app yok"
    notlar = (man.get("notes") or {}).get("tr") or ""
    tarih = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # --- masaüstü
    data = masaustu_paketi(surum)
    dosya = f"masaustu-{kod}.zip"
    for f in os.listdir(GUN):
        if f.startswith("masaustu-") and f.endswith(".zip"):
            os.remove(os.path.join(GUN, f))
    open(os.path.join(GUN, dosya), "wb").write(data)
    json.dump({"surum": surum, "kod": kod, "dosya": dosya, "sha256": hashlib.sha256(data).hexdigest(), "boyut": len(data),
               "notlar": "Bereket Defter " + surum + " yeni kurulum programıyla geliyor. Güncellemeden sonra açılan pencerede "
                         "\"İndir ve kur\"a basın; kayıtlarınız olduğu gibi kalır.\n\n" + notlar, "tarih": tarih},
              open(os.path.join(GUN, "masaustu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("masaüstü köprüsü:", dosya, len(data), "bayt")
    # --- telefon
    if "android" not in a:
        print("UYARI: release'te android kanalı yok; telefon köprüsü yapılmadı")
        return
    an = a["android"]
    if "--apk" in sys.argv:
        apk = open(sys.argv[sys.argv.index("--apk") + 1], "rb").read()
    else:
        apk = al(f"https://github.com/{REPO}/releases/download/v{surum}/{an['file']}")
    assert hashlib.sha256(apk).hexdigest() == an["sha256"], "APK SHA-256 latest.json ile tutmuyor"
    yml = open(os.path.join(KOK, "android", "apktool.yml"), encoding="utf-8").read()
    vcode = int(re.search(r"versionCode: (\d+)", yml).group(1))
    ad = f"BereketDefter-{vcode}.apk"
    yol = os.path.join(GUN, ad)
    open(yol, "wb").write(apk)
    eski = sertifika(os.path.join(GUN, ESKI_APK))
    yeni = sertifika(yol)
    if not eski or eski != yeni:
        os.remove(yol)
        raise SystemExit(f"İMZA FARKLI: kurulu APK {eski} ≠ yeni {yeni} — telefonlar güncellemeyi kuramaz; köprü yayınlanmadı")
    mj = os.path.join(GUN, "mobil.json")
    m = json.load(open(mj, encoding="utf-8"))
    m.update({"surum": surum, "kod": kod, "tarih": tarih, "minNative": vcode, "apkKod": str(vcode), "apkDosya": ad,
              "apkBoyut": len(apk), "apkSha256": hashlib.sha256(apk).hexdigest(),
              "notlar": "Bereket Defter " + surum + ": uygulamanın yeni sürümü (APK). Kayıtlarınız olduğu gibi kalır.\n\n" + notlar})
    json.dump(m, open(mj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("telefon köprüsü:", ad, len(apk), "bayt, imza aynı:", yeni[:16])


if __name__ == "__main__":
    main()
