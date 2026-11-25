# Bereket Defter

PySide6 masaüstü (`masaustu/`, kurulumlu) + Android apktool/smali kabuğu (`android/`) içinde WebView arayüzü (`mobil/`). Türkçe.
Ortak çekirdek (v1.21.0'dan beri): masaüstü `masaustu/fccore` (Python/Qt), telefon `mobil/cekirdek` (web); hangi commit: `cekirdek/VERSION`.
Çekirdek kopyasını burada değiştirme (departures-mil/ortak-cekirdek'ten yeniden kopyala); yerel ek `android/java/.../FcGuncelle.java`.

## Kurallar (kullanıcı)
- Kullanıcı "BAŞLA" demeden yeni iş başlatma. Yazışma dili Türkçe. Arayüz tr/en/ar (Arapça RTL).
- Sürüm semver X.Y.Z, etiket `vX.Y.Z`. Önce `masaustu/notlar.py` en üstüne not, sonra `python3 araclar/surum_yaz.py X.Y.Z`.
- Güncelleme yalnız GitHub Releases + latest.json + FCD1 yama (CI: `.github/workflows/release.yml` → ortak reusable-release).
  Yayın main'de workflow_dispatch: `gh api -X POST repos/departures-mil/bereket-defter/actions/workflows/release.yml/dispatches -f ref=main`.
- Android: aynı paket adı (`com.bereket.alacakverecek`) ve aynı anahtar (secret'lar ANDROID_KEYSTORE_B64/PASS/[KEY_PASS]/[KEY_ALIAS]);
  CI yeni APK'nın sertifikasını `guncelleme/BereketDefter-16.apk` ile karşılaştırır. Java eki değişince `bash araclar/java_smali.sh`.
- Veri klasörü / paket adı / productName DEĞİŞMEZ. Hiçbir kayıt kalıcı silinmez (arşiv + çakışma yedeği; `db.py`, `store.js`).
- Ayarlar'da "Admin ile iletişim" EN SONDA (çekirdek). Bulut: kullanıcının kendi Firebase'i; AI yok (`usage: {firebase:true, ai:false}`).
- ESKİ KANAL: ≤1.20 kurulumlar raw `guncelleme/masaustu.json` + `mobil.json` okur (yalnız SHA-256, imza yok). Release'ten SONRA
  `python3 araclar/kopru.py` → masaüstü "Yeni kurulum gerekli" paketi + telefon APK (minNative) → commit + push main.
- Kullanıcıya APK/exe dosyası gönderme; güncelleme uygulamanın içinden insin.
- v1.22 ekleri: masaüstü `ekler*.py`, telefon `mobil/js/ekler.js`. Yeni çeviri eklerken `masaustu/ekler_ceviri.py`'ye yazıp
  `python3 araclar/ceviri_mobil.py` çalıştırın (eksik çeviri varsa hata verir). PIN / kur / otomatik yedek ayarları cihaza özeldir
  (masaüstü `guvenlik.json`, telefon localStorage `bereket_guvenlik`), eşitlenmez. Kişi `tags` alanı eşitlenir (ESITLEME: persons.tags).
