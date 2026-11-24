# Bereket Alacak-Verecek Defteri

Windows masaüstü programı (Python + PySide6, taşınabilir) ve Android telefon uygulaması. Kayıtlar cihazlar arasında
kullanıcının Firebase hesabı üzerinden eşitlenir; **kayıtlar bu depoda bulunmaz**.

- `masaustu/` — masaüstü programın kaynağı (kurulu programda `app\` klasörü).
- `mobil/` — telefon uygulamasının web paketi (Android kabuğu içinde çalışır).
- `android/` — telefon uygulamasının (APK) apktool ağacı (smali; Java kaynağı yok). APK: `python3 araclar/apk.py <bereket.jks> <şifre> <çıktı.apk>`
  (imza anahtarı depoda değil: `C:\Claude Programlarım\_Anahtarlar\Bereket`). Sürüm `android/apktool.yml` (versionCode = nativeCode).
- Wi‑Fi (internetsiz) eşitleme (1.14 / APK 1.8): masaüstü `masaustu/lan.py` (port 47341, eşleme kodu), telefon `mobil/js/lan.js`.
  Bulut eşitlemesiyle aynı biçim ve aynı birleştirme kuralı; Wi‑Fi'dan gelen değişiklikler buluta da gönderilir.
- `guncelleme/` — güncelleme paketleri ve bildirgeleri. Programlar yeni sürümü buradan indirir
  (`https://raw.githubusercontent.com/departures-mil/bereket-defter/main/guncelleme/<kanal>.json`), sha256 ile doğrular.
- `araclar/yayinla.py` — yeni sürüm yayınlama aracı.

## Yeni sürüm
1. Sürümü iki tarafta aynı artır: `masaustu/main.py` (`APP_VERSION`) ve `mobil/js/core.js` (`APP_VERSION`).
2. `python3 araclar/yayinla.py masaustu "notlar"` ve `python3 araclar/yayinla.py mobil "notlar"`
   APK değiştiyse: `python3 araclar/yayinla.py mobil "notlar" --minNative <kod> --apk <dosya.apk> --apkKod <kod>` (telefon tek tuşla kurar)
3. `git add -A && git commit -m "Bereket X.Y" && git push`

## Asistan Agent (telefon 1.19, masaüstü 1.20 — `masaustu/fc_agent.py` = ortak-cekirdek/python/fc_agent.py)
✦ Asistan Agent eklendi: `fc-agent.js` (= ortak-cekirdek/web/dist/fc-agent.js) + `agent-baslat.js` arayüz klasöründe. Bütün programlardaki
çalışmayı sayılarla izler, öneri verir (bildirim + ✦ panel), Ayarlar'da admin iletişim kartının önünde. Sonraki sürüm yayınlanınca kullanıcılara gider.
