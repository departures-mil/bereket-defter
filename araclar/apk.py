"""Bereket Defter Android APK'sını depodaki apktool ağacından üretir (Android SDK gerekmez).

Kullanım (depo kökünden):  python3 araclar/apk.py <bereket.jks> <şifre> <çıktı.apk>
- android/ = yayındaki APK'nın apktool ağacı (smali). Java kaynağı yoktur; değişiklikler smali üzerinde yapılır.
- android/assets/www her derlemede mobil/ klasöründen yenilenir (telefon arayüzü).
- Sürüm: android/apktool.yml versionCode / versionName (nativeCode = versionCode; mobil.json minNative ile eşleşir).
- İmza anahtarı (bereket.jks, alias bereket) depoda DEĞİL: C:\\Claude Programlarım\\_Anahtarlar\\Bereket
Araçlar (apktool, apksig) ilk çalıştırmada ~/.cache/og-apk/ altına indirilir.
"""
import os, shutil, struct, subprocess, sys, tempfile, urllib.request, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.expanduser("~/.cache/og-apk")
TOOLS = {
    "apktool.jar": "https://github.com/iBotPeaches/Apktool/releases/download/v2.12.1/apktool_2.12.1.jar",
    "apksig.jar": "https://dl.google.com/android/maven2/com/android/tools/build/apksig/8.7.3/apksig-8.7.3.jar",
}


def tool(name):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        urllib.request.urlretrieve(TOOLS[name], p + ".part")
        os.rename(p + ".part", p)
    return p


def run(*cmd):
    r = subprocess.run(list(cmd), capture_output=True, text=True)
    out = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if "JAVA_" not in l)
    if r.returncode:
        raise SystemExit("HATA: " + " ".join(cmd[:3]) + "\n" + out)
    return out


def align(src, dst, n=4):
    zin = zipfile.ZipFile(src)
    with zipfile.ZipFile(dst, "w") as zout:
        for i in zin.infolist():
            data = zin.read(i.filename)
            zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
            zi.compress_type, zi.external_attr = i.compress_type, i.external_attr
            if i.compress_type == zipfile.ZIP_STORED:
                off = zout.fp.tell() + 30 + len(i.filename.encode("utf-8"))
                pad = (-(off + 6)) % n
                zi.extra = struct.pack("<HHH", 0xD935, 2 + pad, n) + b"\0" * pad
            zout.writestr(zi, data, compress_type=i.compress_type)


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    ks, pw, out = sys.argv[1:]
    apktool, apksig = tool("apktool.jar"), tool("apksig.jar")
    www = os.path.join(ROOT, "android", "assets", "www")
    shutil.rmtree(www, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, "mobil"), www)
    with tempfile.TemporaryDirectory() as t:
        unsigned, aligned = os.path.join(t, "u.apk"), os.path.join(t, "a.apk")
        run("java", "-jar", apktool, "b", "-f", os.path.join(ROOT, "android"), "-o", unsigned)
        align(unsigned, aligned)
        run("javac", "-nowarn", "-cp", apksig, "-d", t, os.path.join(ROOT, "araclar", "apk", "Imzala.java"))
        print(run("java", "-cp", apksig + os.pathsep + t, "Imzala", ks, pw, "bereket", aligned, os.path.abspath(out)).strip())
    print("APK:", out, f"({os.path.getsize(out) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
