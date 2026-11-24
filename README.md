# Bereket Alacak-Verecek Defteri

Windows masaüstü programı (Python + PySide6, kurulumlu) ve Android telefon uygulaması. Kayıtlar cihazlar arasında
kullanıcının KENDİ Firebase hesabı üzerinden ve aynı ağda Wi‑Fi ile eşitlenir; **kayıtlar bu depoda bulunmaz**.
v1.21.0'dan beri ortak çekirdek kullanılır (`cekirdek/VERSION`): Falcon görünümü + şema seçici (eski görünüm "Klasik"), sağ üst
Eşitle · Wi‑Fi · Güncelle · tema · dil | Küçült · Orta · Tam ekran · Kapat, tek tuşla güncelleme (GitHub Releases + latest.json + FCD1 yama),
Admin ile iletişim (Ayarlar'ın EN SONU), çökme raporu, Kullanım Limitleri, ilk açılış rehberi (kendi Firebase'iniz), "neler yeni", yazı boyutu.

- `masaustu/` — masaüstü kaynağı. `main.py` (kabuk: `build_app`, defter sayfası `MainWindow`, ayarlar kartları), `db.py` (SQLite + arşiv),
  `sync.py` (Firebase REST), `lan.py` (Wi‑Fi sunucusu, port 47341), `fccore/` (ortak çekirdek, DEĞİŞTİRMEYİN), `fc_agent.py` (Asistan Agent),
  `surum.py` (sürüm), `notlar.py` (sürüm notları).
- `mobil/` — telefon arayüzü (WebView). `cekirdek/` = ortak çekirdek web (fc-core.js, css, yazı tipleri), `js/kabuk.js` = çekirdek yapıştırıcısı.
  `android/assets/www` bunun kopyasıdır (APK derlenirken yenilenir).
- `android/` — APK'nın apktool ağacı (smali). Java eki: `android/java/` (FcGuncelle: GitHub Releases'tan APK güncellemesi + ortak FcDelta)
  → `bash araclar/java_smali.sh` ile smali'ye çevrilir. Paket adı `com.bereket.alacakverecek`, imza anahtarı hep aynı (CI secret'ları).
- `paket/` — PyInstaller one-dir (`BereketDefter.spec`) ve NSIS kurulum (`kurulum.nsi`, kullanıcı başına: `%LOCALAPPDATA%\Programs\Bereket Defter\app`).
- `guncelleme/` — ESKİ kanal (≤1.20 kurulumlar raw `masaustu.json` / `mobil.json` okur). Yalnız köprü için: `araclar/kopru.py`.

## Veri (değişmez)
Masaüstü: `%APPDATA%\AlacakVerecek` (eski taşınabilir kurulumda `AV_DATA_DIR`; köprü `veri-konumu.txt` bırakır, yeni sürüm aynı klasörü açar).
Telefon: WebView IndexedDB `bereket_defter`. Hiçbir kayıt kalıcı silinmez: silinen (bu ya da başka cihazda) → Ayarlar → Arşiv (geri alınabilir),
çakışmada eski hal → çakışma yedeği. Belge dosyaları da arşivde kalır (`fotograflar/arsiv`).

## Yeni sürüm
1. `masaustu/notlar.py` → `NOTES`'un EN ÜSTÜNE yeni sürüm (tr/en/ar). 2. `python3 araclar/surum_yaz.py X.Y.Z`
   (masaüstü + telefon + apktool.yml versionName/versionCode + release-notes.json). 3. Dalda CI yeşil → main → yayın:
   `gh api -X POST repos/departures-mil/bereket-defter/actions/workflows/release.yml/dispatches -f ref=main`
   Kanallar: `win-app` (fcpack zip), `win-setup` (NSIS), `android` (APK). Yamalar CI'da üretilir.

## Test
`python -m pytest -q test` (veri kuralları, sürüm, köprü, offscreen Qt kabuk) · `node test/mobil.test.js` (Chromium) ·
ekran görüntüleri: `python3 araclar/ekran.py <klasör>`, `node araclar/ekran_mobil.js <klasör>`.
