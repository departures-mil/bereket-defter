"""Sürüm notları ("neler yeni" penceresi + GitHub sürüm notları). En yeni sürüm EN ÜSTTE.
araclar/surum_yaz.py ilk kaydı release-notes.json'a yazar (CI latest.json notları)."""
NOTES = {
    "1.22.0": {
        "tr": "Güvenlik: PIN kilidi (açılışta ve boşta kalınca), tutarları gizle düğmesi (👁), her gün otomatik yedek ve önizlemeli «eksikleri geri getir» (hiçbir kaydı silmez, üzerine yazmaz)\n"
              "Yeni Raporlar sayfası: genel durum ve dolar karşılığı (elle kur), yaşlandırma, en büyük bakiyeler, aylık hareket grafiği, vadesi geçenler; CSV dışa / içe aktarma\n"
              "Kişiye mesaj / mutabakat: bakiye bildirimi, kibar ödeme hatırlatması, hesap kapandı (Türkçe, İngilizce, Arapça; WhatsApp · Telegram · kopyala)\n"
              "Taksit planı (her taksit için hatırlatıcı) ve Bakara 282'ye uygun borç senedi (kâtip ve iki şahit; PDF / yazdır)\n"
              "Hızlı kayıt: «Ahmet'e 500 TL verdim» yazın, kayıt hazırlanır (internet gerekmez)\n"
              "Kişilere etiket (aile, iş…) ve etiket süzgeci; vadesi geçenler ⏰ ile işaretli; silinen kayıt için «Geri al»; klavye kısayolları (masaüstü)",
        "en": "Security: PIN lock (at start and when idle), a hide-amounts button (👁), a daily automatic backup and a «recover missing items» option with preview (never deletes or overwrites a record)\n"
              "New Reports page: overall position and USD equivalent (manual rates), aging, largest balances, monthly activity chart, overdue items; CSV export / import\n"
              "Message / reconcile with a person: balance notice, polite payment reminder, account settled (Turkish, English, Arabic; WhatsApp · Telegram · copy)\n"
              "Instalment plan (a reminder for each instalment) and a promissory note following al-Baqarah 2:282 (scribe and two witnesses; PDF / print)\n"
              "Quick entry: type «gave Ahmet 500 TL» and the record is prepared (no internet needed)\n"
              "Tags for people (family, work…) with a tag filter; overdue people marked with ⏰; «Undo» after deleting; keyboard shortcuts (desktop)",
        "ar": "الأمان: قفل برمز PIN (عند الفتح وعند عدم الاستخدام)، وزر لإخفاء المبالغ (👁)، ونسخة احتياطية تلقائية يومية، وخيار «استرجاع الناقص» مع معاينة (لا يحذف أي سجل ولا يكتب فوقه)\n"
              "صفحة تقارير جديدة: الوضع العام وما يعادله بالدولار (سعر صرف يدوي)، أعمار الأرصدة، أكبر الأرصدة، رسم الحركة الشهرية، المتأخرات؛ تصدير / استيراد CSV\n"
              "رسالة / مطابقة حساب مع الشخص: إشعار الرصيد، تذكير لطيف بالسداد، إغلاق الحساب (بالتركية والإنجليزية والعربية؛ WhatsApp · Telegram · نسخ)\n"
              "خطة أقساط (تذكير لكل قسط) وسند دين وفق آية الدين (البقرة: 282) بكاتب وشاهدين؛ PDF / طباعة\n"
              "إدخال سريع: اكتب «أعطيت أحمد 500 ليرة تركية» فيُجهَّز السجل (دون إنترنت)\n"
              "وسوم للأشخاص (عائلة، عمل…) مع تصفية حسب الوسم؛ تمييز المتأخرين بـ⏰؛ «تراجع» بعد الحذف؛ اختصارات لوحة المفاتيح (الحاسوب)",
    },
    "1.21.4": {
        "tr": "Güncelleme sırasında \"Programdan çıkmak istiyor musunuz?\" sorusu artık çıkmaz; güncelleme kendiliğinden tamamlanır.",
        "en": "The \"Do you want to quit?\" question no longer appears during an update; the update completes by itself.",
        "ar": "لم يعد سؤال «هل تريد الخروج من البرنامج؟» يظهر أثناء التحديث؛ يكتمل التحديث تلقائياً.",
    },
    "1.21.3": {
        "tr": "Eski sürümlerden bu sürüme geçiş bir kez tam kurulumla yapılır (eski güncelleyicideki siyah pencere sorunu yaşanmaz). Sonraki güncellemeler yine arka planda, kendiliğinden. Kayıtlar korunur.",
        "en": "Moving from older versions to this one is done once with a full install (avoids the black-window problem of the old updater). Later updates again run by themselves in the background. Records are kept.",
        "ar": "يتم الانتقال من الإصدارات القديمة إلى هذا الإصدار مرة واحدة بتثبيت كامل (تجنباً لمشكلة النوافذ السوداء في المحدِّث القديم). التحديثات اللاحقة تتم تلقائياً في الخلفية. تبقى السجلات محفوظة.",
    },
    "1.21.2": {
        "tr": "Güncellemeler artık tamamen kendiliğinden: yeni sürüm arka planda sessizce indirilir, program kapanınca pencere açmadan kurulur; bir sonraki açılışta yeni sürüm gelir. Hemen kurmak için Güncelle → «Şimdi kur ve yeniden aç». Kurulum gereken güncellemeler de sessiz yapılır. Kayıtlara dokunulmaz.",
        "en": "Updates are now fully automatic: the new version downloads quietly in the background and installs without any window when the program closes; the next start opens the new version. To install right away: Update → «Install now and reopen». Updates that need the installer also run silently. Records are not touched.",
        "ar": "أصبحت التحديثات تلقائية بالكامل: يُنزَّل الإصدار الجديد بهدوء في الخلفية ويُثبَّت دون أي نافذة عند إغلاق البرنامج، ويُفتح الإصدار الجديد في المرة التالية. للتثبيت فوراً: تحديث ← «ثبّت الآن وأعد الفتح». التحديثات التي تحتاج إلى برنامج التثبيت تتم بصمت أيضاً. لا تُمَسّ السجلات.",
    },
    "1.21.1": {
        "tr": "Defter ekranındaki hadisler İngilizce ve Arapça (asıl metniyle) gösterilir\n"
              "Sürüm rozeti tam sürümü gösterir (v1.21.1)\n"
              "Arapça: kalan süre \"د / ث\" ile; Asistan Agent kartında metin kesilmiyor\n"
              "Sol alttaki ✦ düğmesinin simgesi yeniden görünüyor",
        "en": "The hadiths on the ledger screen are shown in English and Arabic (original text)\n"
              "The version badge shows the full version (v1.21.1)\n"
              "Arabic: remaining time uses \"د / ث\"; text in the Assistant Agent card is no longer cut off\n"
              "The ✦ button at the bottom left shows its icon again",
        "ar": "تُعرض الأحاديث في شاشة الدفتر بالإنجليزية وبالعربية (بنصّها الأصلي)\n"
              "تعرض شارة الإصدار رقم الإصدار كاملاً (v1.21.1)\n"
              "العربية: الوقت المتبقي بـ«د / ث»؛ ولم يعد النص في بطاقة الوكيل المساعد مقطوعاً\n"
              "عاد رمز الزر ✦ في أسفل اليسار إلى الظهور",
    },
    "1.21.0": {
        "tr": "Yeni görünüm (Falcon) ve renk şeması seçici; eski yeşil görünüm \"Klasik\" olarak seçilebilir, koyu/açık tema, yazı boyutu\n"
              "Sağ üstte Eşitle · Wi‑Fi · Güncelle · tema · dil | Küçült · Orta · Tam ekran · Kapat\n"
              "Tek tuşla güncelleme: yalnızca değişen kısımlar iner (yüzde, MB, kalan, hız); bilgisayarda kurulum programı\n"
              "Hiçbir kayıt kalıcı silinmez: başka cihazda silinenler Ayarlar → Arşiv'e gider, çakışmada eski hal yedeklenir\n"
              "İlk açılış rehberi (kendi Firebase'iniz), otomatik hata raporu, Admin ile iletişim Ayarlar'ın en sonunda",
        "en": "New look (Falcon) with a colour scheme picker; the old green look is available as \"Classic\", dark/light theme, font size\n"
              "Top right: Sync · Wi‑Fi · Update · theme · language | Minimize · Half · Full screen · Close\n"
              "One-click updates: only the changed parts are downloaded (percent, MB, remaining, speed); an installer on the computer\n"
              "No record is ever deleted for good: records deleted on another device go to Settings → Archive, conflicts keep a backup\n"
              "First-run guide (your own Firebase), automatic error reports, Contact the admin at the end of Settings",
        "ar": "مظهر جديد (Falcon) مع اختيار نظام الألوان؛ المظهر الأخضر القديم متاح باسم «الكلاسيكي»، وسمة داكنة/فاتحة وحجم الخط\n"
              "أعلى اليمين: مزامنة · Wi‑Fi · تحديث · السمة · اللغة | تصغير · نصف · ملء الشاشة · إغلاق\n"
              "تحديث بضغطة واحدة: تُنزَّل الأجزاء المتغيرة فقط (النسبة، الميغابايت، المتبقي، السرعة)؛ ومثبّت على الحاسوب\n"
              "لا يُحذف أي سجل نهائياً: ما يُحذف على جهاز آخر ينتقل إلى الإعدادات ← الأرشيف، وعند التعارض تُحفظ نسخة احتياطية\n"
              "دليل التشغيل الأول (Firebase الخاص بك)، وتقارير الأخطاء التلقائية، والتواصل مع المسؤول في آخر الإعدادات",
    },
}
