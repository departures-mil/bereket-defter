"""Telefon çevirilerini üretir: mobil/js/ekler.js (+ ui.js / forms.js'teki v1.22 metinleri) içindeki t("…") / tf("…") anahtarlarını
masaüstü i18n.T'den (masaustu/ekler_ceviri.py dahil) alıp mobil/js/i18n_ekler.js'e yazar. Eksik çeviri varsa hata verir.
Kullanım: python3 araclar/ceviri_mobil.py"""
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "masaustu"))
import i18n  # noqa: E402
import ekler_ceviri  # noqa: E402,F401

DOSYALAR = ["mobil/js/ekler.js", "mobil/js/ui.js", "mobil/js/forms.js"]
DIZI = re.compile(r'\[\s*(?:-?\d+|"[^"]*")\s*,\s*"((?:[^"\\]|\\.)+)"\s*\]')   # [k, "Türkçe"] seçenek dizileri (ekler.js)


def anahtarlar():
    out = []
    for f in DOSYALAR:
        s = open(os.path.join(KOK, f), encoding="utf-8").read()
        for m in re.finditer(r'\bt[f]?\(\s*"((?:[^"\\]|\\.)*)"', s):
            out.append(json.loads('"' + m.group(1) + '"'))
        if f.endswith("ekler.js"):
            out += [json.loads('"' + m.group(1) + '"') for m in DIZI.finditer(s)]
    return list(dict.fromkeys(out))


def main():
    mevcut = set()
    for f in ("mobil/js/i18n_desktop.js", "mobil/js/i18n_mobile.js"):
        s = open(os.path.join(KOK, f), encoding="utf-8").read()
        mevcut |= {json.loads('"' + m.group(1) + '"') for m in re.finditer(r'^"((?:[^"\\]|\\.)*)":', s, re.M)}
    sozluk, eksik = {}, []
    for k in anahtarlar():
        if k in i18n.T:
            if k not in mevcut or k in ekler_ceviri_anahtarlari():
                sozluk[k] = list(i18n.T[k])
        elif k not in mevcut and re.search(r"[a-zçğıöşü]{3}", k, re.I) and not re.fullmatch(r"[A-Za-z ]+", k):
            eksik.append(k)
    if eksik:
        print("ÇEVİRİSİ EKSİK:", *eksik, sep="\n  ")
        sys.exit(1)
    yol = os.path.join(KOK, "mobil/js/i18n_ekler.js")
    with open(yol, "w", encoding="utf-8") as f:
        f.write("/* OTOMATİK ÜRETİLDİ (araclar/ceviri_mobil.py) — kaynak: masaustu/ekler_ceviri.py. v1.22 eklerinin çevirileri [en, ar]. */\n")
        f.write("'use strict';\nwindow.I18N_MOBILE = Object.assign(window.I18N_MOBILE || {}, ")
        f.write(json.dumps(sozluk, ensure_ascii=False, indent=0))
        f.write(");\n")
    print(f"{len(sozluk)} çeviri yazıldı → mobil/js/i18n_ekler.js")


def ekler_ceviri_anahtarlari():
    s = open(os.path.join(KOK, "masaustu/ekler_ceviri.py"), encoding="utf-8").read()
    return {m for m in re.findall(r'^\s{4}"((?:[^"\\]|\\.)*)"', s, re.M)}


if __name__ == "__main__":
    main()
