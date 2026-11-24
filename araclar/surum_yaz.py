"""Sürümü tek yerden yazar (semver X.Y.Z; etiket vX.Y.Z).

Kullanım (depo kökünden):  python3 araclar/surum_yaz.py 1.22.0
Önce masaustu/notlar.py içinde NOTES'un EN ÜSTÜNE yeni sürümün notunu (tr/en/ar) ekleyin. Bu araç şunları yazar:
  masaustu/surum.py (APP_VERSION) · mobil/js/core.js (APP_VERSION) · mobil/js/notlar.js (neler yeni, telefon)
  android/apktool.yml (versionName = sürüm, versionCode bir artar) · release-notes.json (GitHub sürüm notları / latest.json)
--kontrol: hiçbir şey yazmaz, tutarsızlık varsa 1 ile çıkar (CI testi).
"""
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "masaustu"))


def oku(p):
    with open(os.path.join(KOK, p), encoding="utf-8") as f:
        return f.read()


def yaz(p, s):
    tmp = os.path.join(KOK, p + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    os.replace(tmp, os.path.join(KOK, p))


def notlar():
    import importlib
    import notlar as n
    importlib.reload(n)
    return n.NOTES


def hedefler(v):
    notes = notlar()
    if v not in notes:
        raise SystemExit(f"masaustu/notlar.py içinde {v} notu yok (EN ÜSTE ekleyin)")
    out = {}
    out["masaustu/surum.py"] = re.sub(r'APP_VERSION = "[^"]*"', f'APP_VERSION = "{v}"', oku("masaustu/surum.py"))
    out["mobil/js/core.js"] = re.sub(r'const APP_VERSION = "[^"]*";', f'const APP_VERSION = "{v}";', oku("mobil/js/core.js"))
    out["mobil/js/notlar.js"] = ("/* OTOMATİK: araclar/surum_yaz.py ← masaustu/notlar.py (\"neler yeni\" penceresi). Elle düzenlemeyin. */\n"
                                 "window.BEREKET_NOTES = " + json.dumps(notes, ensure_ascii=False, indent=1) + ";\n")
    yml = oku("android/apktool.yml")
    eski = re.search(r"versionName: (\S+)", yml).group(1).strip("'\"")
    kod = int(re.search(r"versionCode: (\d+)", yml).group(1))
    if eski != v:
        kod += 1
    yml = re.sub(r"versionCode: \d+", f"versionCode: {kod}", yml)
    yml = re.sub(r"versionName: \S+", f"versionName: {v}", yml)
    out["android/apktool.yml"] = yml
    out["release-notes.json"] = json.dumps(notes[v], ensure_ascii=False, indent=1) + "\n"
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--kontrol" in sys.argv:
        v = re.search(r'APP_VERSION = "([^"]+)"', oku("masaustu/surum.py")).group(1)
        bad = [p for p, s in hedefler(v).items() if not os.path.exists(os.path.join(KOK, p)) or oku(p) != s]
        if bad:
            print("TUTARSIZ:", ", ".join(bad), "→ python3 araclar/surum_yaz.py", v)
            sys.exit(1)
        print("sürüm tutarlı:", v)
        return
    if len(args) != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", args[0]):
        raise SystemExit(__doc__)
    for p, s in hedefler(args[0]).items():
        yaz(p, s)
    print("sürüm", args[0], "yazıldı")


if __name__ == "__main__":
    main()
