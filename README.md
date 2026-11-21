# Bereket Alacak-Verecek Defteri

Windows masaüstü programı (Python + PySide6, taşınabilir) ve Android telefon uygulaması. Kayıtlar cihazlar arasında
kullanıcının Firebase hesabı üzerinden eşitlenir; **kayıtlar bu depoda bulunmaz**.

- `masaustu/` — masaüstü programın kaynağı (kurulu programda `app\` klasörü).
- `mobil/` — telefon uygulamasının web paketi (Android kabuğu içinde çalışır).
- `guncelleme/` — güncelleme paketleri ve bildirgeleri. Programlar yeni sürümü buradan indirir
  (`https://raw.githubusercontent.com/departures-mil/bereket-defter/main/guncelleme/<kanal>.json`), sha256 ile doğrular.
- `araclar/yayinla.py` — yeni sürüm yayınlama aracı.

## Yeni sürüm
1. Sürümü iki tarafta aynı artır: `masaustu/main.py` (`APP_VERSION`) ve `mobil/js/core.js` (`APP_VERSION`).
2. `python3 araclar/yayinla.py masaustu "notlar"` ve `python3 araclar/yayinla.py mobil "notlar"`
3. `git add -A && git commit -m "Bereket X.Y" && git push`
