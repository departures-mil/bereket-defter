"""Dil desteği: Türkçe (varsayılan), English, العربية (sağdan sola).

Anahtarlar Türkçe metinlerdir; _("Türkçe metin") seçili dildeki karşılığı döndürür.
"""
import json
import os

LANGS = {"tr": "Türkçe", "en": "English", "ar": "العربية"}
_lang = "tr"

# Türkçe: (English, العربية)
T = {
    # genel
    "Bereket Alacak-Verecek Defteri": ("Bereket Debt & Credit Ledger", "دفتر بركة للديون والمستحقات"),
    "Dolar ($)": ("Dollar ($)", "دولار ($)"),
    "Türk Lirası (₺)": ("Turkish Lira (₺)", "ليرة تركية (₺)"),
    "Suriye Lirası (£S)": ("Syrian Pound (£S)", "ليرة سورية (£S)"),
    "Pazartesi": ("Monday", "الاثنين"), "Salı": ("Tuesday", "الثلاثاء"), "Çarşamba": ("Wednesday", "الأربعاء"),
    "Perşembe": ("Thursday", "الخميس"), "Cuma": ("Friday", "الجمعة"), "Cumartesi": ("Saturday", "السبت"),
    "Pazar": ("Sunday", "الأحد"),
    # moral sözleri
    "Bereket, düzenli hesapla gelir.": ("Blessings come with well-kept accounts.", "البركة تأتي مع الحساب المنظم."),
    "Her kayıt, güvenin bir tuğlasıdır.": ("Every record is a brick of trust.", "كل قيد لبنة في بناء الثقة."),
    "Bugün attığın küçük adım, yarının büyük kazancıdır.": (
        "Today's small step is tomorrow's big gain.", "خطوتك الصغيرة اليوم هي ربحك الكبير غداً."),
    "Dürüst ticaret, kalıcı kazanç.": ("Honest trade, lasting profit.", "التجارة الصادقة ربح دائم."),
    "Hesabı temiz olanın alnı aktır.": ("Clean accounts, clear conscience.", "من كان حسابه نظيفاً كان ضميره مرتاحاً."),
    "Sabır ve emek, kazancın anahtarıdır.": ("Patience and effort are the keys to profit.",
                                             "الصبر والعمل مفتاحا الرزق."),
    "Damlaya damlaya göl olur.": ("Drop by drop, a lake is formed.", "قطرة فوق قطرة تصنع بحيرة."),
    "İyi hesap, dostluğu bozmaz; korur.": ("Good accounts protect friendships.", "الحساب الجيد يحفظ الصداقة."),
    "Kazancın en güzeli, alın teriyle olanıdır.": ("The best earnings are earned by hard work.",
                                                   "أطيب الكسب ما كان بعرق الجبين."),
    "Planlı çalışan, bereketi yakalar.": ("Those who plan, prosper.", "من خطط لعمله نال البركة."),
    # bakiye kutuları
    "Hesap kapalı": ("Settled", "الحساب مغلق"),
    "Alacak": ("Receivable", "لنا"),
    "Verecek": ("Payable", "علينا"),
    "Verilen": ("Given", "المُعطى"),
    "Alınan": ("Received", "المُستلم"),
    "Genel\nDurum": ("Overall\nStatus", "الوضع\nالعام"),
    # lisans
    "Lisans Etkinleştirme": ("License Activation", "تفعيل الترخيص"),
    "Bu bilgisayar için lisans gerekli.<br>Aşağıdaki <b>Makine Kodu</b>'nu satıcınıza gönderin; size bu "
    "bilgisayara özel bir <b>Serial Key</b> verilecektir.": (
        "A license is required for this computer.<br>Send the <b>Machine Code</b> below to your seller; you will "
        "receive a <b>Serial Key</b> for this computer only.",
        "هذا الحاسوب يحتاج إلى ترخيص.<br>أرسل <b>رمز الجهاز</b> أدناه إلى البائع، وستحصل على <b>مفتاح تسلسلي</b> "
        "خاص بهذا الحاسوب فقط."),
    "Kopyala": ("Copy", "نسخ"),
    "Makine Kodu:": ("Machine Code:", "رمز الجهاز:"),
    "Serial Key:": ("Serial Key:", "المفتاح التسلسلي:"),
    "Etkinleştir": ("Activate", "تفعيل"),
    "Çıkış": ("Exit", "خروج"),
    "Serial Key geçersiz veya bu bilgisayara ait değil.": (
        "The Serial Key is invalid or does not belong to this computer.",
        "المفتاح التسلسلي غير صالح أو لا يخص هذا الحاسوب."),
    "Lisans kaydedilemedi: {}": ("Could not save license: {}", "تعذر حفظ الترخيص: {}"),
    "Teşekkürler": ("Thank you", "شكراً"),
    "Lisans başarıyla etkinleştirildi. Hayırlı kazançlar!": (
        "License activated successfully. Wishing you prosperous business!", "تم تفعيل الترخيص بنجاح. رزقاً مباركاً!"),
    "Lisans No: {}": ("License No: {}", "رقم الترخيص: {}"),
    "Program lisans anahtarı olmadan derlenmiş. Satıcınıza başvurun.": (
        "This program was built without a license key. Contact your seller.",
        "تم بناء البرنامج بدون مفتاح ترخيص. يرجى مراجعة البائع."),
    "Hata": ("Error", "خطأ"),
    # kişiler
    "Kişi Düzenle": ("Edit Person", "تعديل الشخص"),
    "Yeni Kişi": ("New Person", "شخص جديد"),
    "➕ Yeni kişi ekle": ("➕ Add new person", "➕ إضافة شخص جديد"),
    "Yeni kişinin adı *": ("New person's name *", "اسم الشخص الجديد *"),
    "Ad Soyad *": ("Full name *", "الاسم الكامل *"),
    "Telefon": ("Phone", "الهاتف"),
    "Not": ("Note", "ملاحظة"),
    "Kaydet": ("Save", "حفظ"),
    "Vazgeç": ("Cancel", "إلغاء"),
    "Eksik": ("Missing", "نقص"),
    "Ad Soyad boş olamaz.": ("Full name cannot be empty.", "لا يمكن ترك الاسم فارغاً."),
    "Kişiler": ("People", "الأشخاص"),
    "🔍 Kişi ara…": ("🔍 Search people…", "🔍 بحث عن شخص…"),
    "+ Kişi Ekle": ("+ Add Person", "+ إضافة شخص"),
    "Düzenle": ("Edit", "تعديل"),
    "Sil": ("Delete", "حذف"),
    "★  Tüm kişiler": ("★  Everyone", "★  جميع الأشخاص"),
    "Tüm kişiler": ("Everyone", "جميع الأشخاص"),
    "Bütün kişilerin kayıtları": ("Records of all people", "سجلات جميع الأشخاص"),
    "'{}' silinsin mi?": ("Delete '{}'?", "هل تريد حذف '{}'؟"),
    "DİKKAT: Bu kişiye ait {} kayıt ve fotoğrafları da kalıcı olarak silinecek!": (
        "WARNING: {} records of this person and their photos will also be permanently deleted!",
        "تنبيه: سيتم أيضاً حذف {} قيداً لهذا الشخص مع صورها نهائياً!"),
    "Kişiyi sil": ("Delete person", "حذف الشخص"),
    "Kişi yok": ("No people", "لا يوجد أشخاص"),
    "Önce soldan bir kişi ekleyin.": ("Please add a person first.", "يرجى إضافة شخص أولاً."),
    "Önce bir kişi ekleyin.": ("Please add a person first.", "يرجى إضافة شخص أولاً."),
    # fotoğraflar
    "Yakınlaştır +": ("Zoom in +", "تكبير +"),
    "Uzaklaştır −": ("Zoom out −", "تصغير −"),
    "Sığdır": ("Fit", "ملاءمة"),
    "Harici programda aç": ("Open externally", "فتح ببرنامج خارجي"),
    "Fotoğraf açılamadı.": ("Could not open photo.", "تعذر فتح الصورة."),
    "Resimler (*.jpg *.jpeg *.png *.bmp *.webp *.heic *.gif);;Tüm dosyalar (*)": (
        "Images (*.jpg *.jpeg *.png *.bmp *.webp *.heic *.gif);;All files (*)",
        "صور (*.jpg *.jpeg *.png *.bmp *.webp *.heic *.gif);;كل الملفات (*)"),
    "Fotoğraf seç": ("Select photos", "اختيار صور"),
    "Fotoğraf": ("Photo", "صورة"),
    "{} kopyalanamadı: {}": ("Could not copy {}: {}", "تعذر نسخ {}: {}"),
    "<b>Fotoğraflar</b> (büyütmek için çift tıklayın)": (
        "<b>Photos</b> (double-click to enlarge)", "<b>الصور</b> (انقر مرتين للتكبير)"),
    "📷 Fotoğraf ekle": ("📷 Add photo", "📷 إضافة صورة"),
    "Seçili fotoğrafı kaldır": ("Remove selected photo", "إزالة الصورة المحددة"),
    "💵 Nakit dolar aldıysanız banknotların fotoğrafını eklemeyi unutmayın (sahte çıkma ihtimaline karşı).": (
        "💵 If you received cash dollars, don't forget to add photos of the banknotes (in case they turn out "
        "to be counterfeit).",
        "💵 إذا استلمت دولارات نقداً فلا تنسَ إضافة صور الأوراق النقدية (تحسباً لكونها مزورة)."),
    "📷 Fotoğraflar": ("📷 Photos", "📷 الصور"),
    "Fotoğraflar": ("Photos", "الصور"),
    "Fotoğraf yok": ("No photos", "لا توجد صور"),
    "Bu kayıtta fotoğraf yok. Şimdi eklemek ister misiniz?": (
        "This record has no photos. Add some now?", "لا توجد صور لهذا القيد. هل تريد إضافتها الآن؟"),
    "Büyütmek için çift tıklayın.": ("Double-click to enlarge.", "انقر مرتين للتكبير."),
    # kayıtlar
    "Kaydı Düzenle": ("Edit Record", "تعديل القيد"),
    "Yeni Kayıt": ("New Record", "قيد جديد"),
    "Kişi": ("Person", "الشخص"),
    "Tarih / Saat": ("Date / Time", "التاريخ / الوقت"),
    "Verdim (Çıktı)": ("Gave (Out)", "أعطيت (صادر)"),
    "Aldım (Girdi)": ("Received (In)", "استلمت (وارد)"),
    "Verdim": ("Gave", "أعطيت"),
    "Aldım": ("Received", "استلمت"),
    "İşlem": ("Type", "العملية"),
    "Para birimi": ("Currency", "العملة"),
    "Tutar": ("Amount", "المبلغ"),
    "Açıklama": ("Description", "الوصف"),
    "Tutar sıfırdan büyük olmalı.": ("Amount must be greater than zero.", "يجب أن يكون المبلغ أكبر من صفر."),
    "Tüm para birimleri": ("All currencies", "كل العملات"),
    "Açıklamada ara…": ("Search description…", "بحث في الوصف…"),
    "Birim": ("Cur.", "العملة"),
    "Verilen (Çıktı)": ("Given (Out)", "المُعطى (صادر)"),
    "Alınan (Girdi)": ("Received (In)", "المُستلم (وارد)"),
    "+ Verdim (Çıktı)": ("+ Gave (Out)", "+ أعطيت (صادر)"),
    "+ Aldım (Girdi)": ("+ Received (In)", "+ استلمت (وارد)"),
    "Değişiklik Geçmişi": ("Change History", "سجل التعديلات"),
    "📄 Döküm Al": ("📄 Statement", "📄 كشف حساب"),
    "Seçim": ("Selection", "اختيار"),
    "Önce tablodan bir kayıt seçin.": ("Select a record in the table first.", "اختر قيداً من الجدول أولاً."),
    "Kaydı sil": ("Delete record", "حذف القيد"),
    "{} tarihli {} kaydı ve fotoğrafları silinsin mi?": (
        "Delete the {} record of {} and its photos?", "هل تريد حذف قيد {} بمبلغ {} مع صوره؟"),
    "Geçmiş": ("History", "السجل"),
    "Bu kayıt hiç değiştirilmemiş.": ("This record has never been changed.", "لم يتم تعديل هذا القيد أبداً."),
    "önceki hali": ("previous version", "النسخة السابقة"),
    # döküm
    "Hesap Dökümü": ("Account Statement", "كشف الحساب"),
    "Günlük gruplama": ("Group by day", "تجميع يومي"),
    "Saatlik gruplama": ("Group by hour", "تجميع بالساعة"),
    "Başlangıç": ("From", "من"),
    "Bitiş": ("To", "إلى"),
    "Hızlı seçim…": ("Quick range…", "اختيار سريع…"),
    "Bugün": ("Today", "اليوم"),
    "Son 7 gün": ("Last 7 days", "آخر 7 أيام"),
    "Bu ay": ("This month", "هذا الشهر"),
    "Tümü": ("All", "الكل"),
    "Göster": ("Show", "عرض"),
    "PDF olarak kaydet": ("Save as PDF", "حفظ كملف PDF"),
    "Yazdır": ("Print", "طباعة"),
    "Hesap Dökümü — {}": ("Account Statement — {}", "كشف حساب — {}"),
    "Oluşturulma": ("Created", "تاريخ الإنشاء"),
    "Devreden bakiye": ("Opening balance", "الرصيد المُرحّل"),
    "Saat": ("Time", "الوقت"),
    "Bakiye": ("Balance", "الرصيد"),
    "Foto": ("Photo", "صور"),
    "Bu aralıkta kayıt yok.": ("No records in this range.", "لا توجد قيود في هذه الفترة."),
    "saat": ("hour", "الساعة"),
    "Gün toplamı": ("Day total", "مجموع اليوم"),
    "Saat toplamı": ("Hour total", "مجموع الساعة"),
    "verilen": ("given", "المُعطى"),
    "alınan": ("received", "المُستلم"),
    "Özet": ("Summary", "الملخص"),
    "Devreden": ("Opening", "المُرحّل"),
    "Kapanış bakiyesi": ("Closing balance", "الرصيد الختامي"),
    "Bakiye: pozitif = alacak (kişi borçlu), negatif = verecek (biz borçluyuz).": (
        "Balance: positive = receivable (the person owes us), negative = payable (we owe).",
        "الرصيد: موجب = لنا (الشخص مدين لنا)، سالب = علينا (نحن مدينون)."),
    "PDF kaydet": ("Save PDF", "حفظ PDF"),
    "Kaydedildi": ("Saved", "تم الحفظ"),
    "Döküm kaydedildi:\n{}": ("Statement saved:\n{}", "تم حفظ الكشف:\n{}"),
    # ana pencere
    "Tüm Kayıtlar Dökümü": ("Full Statement", "كشف جميع القيود"),
    "Yedek Al": ("Backup", "نسخ احتياطي"),
    "Tam Ekran (F11)": ("Full Screen (F11)", "ملء الشاشة (F11)"),
    "Programdan çıkmak istiyor musunuz?": ("Do you want to exit?", "هل تريد الخروج من البرنامج؟"),
    "Yedek kaydet": ("Save backup", "حفظ النسخة الاحتياطية"),
    "Yedek": ("Backup", "نسخة احتياطية"),
    "Yedek alındı:\n{}\n\nYedeği USB bellek gibi ayrı bir yerde saklamanız önerilir.": (
        "Backup saved:\n{}\n\nKeep the backup in a separate place such as a USB stick.",
        "تم حفظ النسخة الاحتياطية:\n{}\n\nيُنصح بحفظها في مكان منفصل مثل ذاكرة USB."),
    "Dil": ("Language", "اللغة"),
    # hatırlatıcılar
    "Tahsil edilecek (alınacak)": ("To collect", "للتحصيل (سنستلم)"),
    "Ödenecek (verilecek)": ("To pay", "للدفع (سنعطي)"),
    "Tamamlandı": ("Done", "مُنجز"),
    "Vakti geldi / gecikti": ("Due / overdue", "حان الموعد / متأخر"),
    "Yaklaşan": ("Upcoming", "قادم"),
    "Hatırlatıcıyı Düzenle": ("Edit Reminder", "تعديل التذكير"),
    "Yeni Hatırlatıcı": ("New Reminder", "تذكير جديد"),
    "Tür": ("Type", "النوع"),
    "(tutar belirtilmedi)": ("(no amount)", "(بدون مبلغ)"),
    "Bakiyeyi kullan": ("Use balance", "استخدام الرصيد"),
    "+1 gün": ("+1 day", "+يوم"),
    "+1 hafta": ("+1 week", "+أسبوع"),
    "+1 ay": ("+1 month", "+شهر"),
    "Hatırlatma zamanı": ("Reminder time", "موعد التذكير"),
    "🔔 Hatırlatıcılar": ("🔔 Reminders", "🔔 التذكيرات"),
    "Vakti gelenler": ("Due now", "المستحقة الآن"),
    "Bekleyenler": ("Pending", "المعلقة"),
    "Durum": ("Status", "الحالة"),
    "+ Yeni Hatırlatıcı": ("+ New Reminder", "+ تذكير جديد"),
    "✓ Tamamlandı": ("✓ Done", "✓ تم"),
    "Ertele (+1 gün)": ("Snooze (+1 day)", "تأجيل (+يوم)"),
    "Kapat": ("Close", "إغلاق"),
    "Bugün ve geçmişte vakti gelen {} hatırlatıcı": ("{} reminders due today or earlier",
                                                     "{} تذكيرات مستحقة اليوم أو قبله"),
    "{} hatırlatıcı": ("{} reminders", "{} تذكيرات"),
    "Önce listeden bir hatırlatıcı seçin.": ("Select a reminder from the list first.", "اختر تذكيراً من القائمة أولاً."),
    "Hatırlatıcı silinsin mi?": ("Delete this reminder?", "هل تريد حذف هذا التذكير؟"),
    "🔔 Hatırlatıcı Ekle": ("🔔 Add Reminder", "🔔 إضافة تذكير"),
    "🔔 Hatırlatıcı": ("🔔 Reminder", "🔔 تذكير"),
    "Sıradaki hatırlatıcı": ("Next reminder", "التذكير التالي"),
    # belgeler / dekontlar
    "Belge": ("Document", "مستند"),
    "Bu dosyayı açacak bir program bulunamadı:\n{}": ("No program found to open this file:\n{}",
                                                      "لم يتم العثور على برنامج لفتح هذا الملف:\n{}"),
    "Tüm dosyalar (*);;Resimler (*.jpg *.jpeg *.png *.bmp *.webp *.heic *.gif);;PDF (*.pdf)": (
        "All files (*);;Images (*.jpg *.jpeg *.png *.bmp *.webp *.heic *.gif);;PDF (*.pdf)",
        "كل الملفات (*);;صور (*.jpg *.jpeg *.png *.bmp *.webp *.heic *.gif);;PDF (*.pdf)"),
    "<b>Dekont / Belgeler</b> — PDF, resim veya her türlü dosya. Açmak için çift tıklayın, dosyaları buraya "
    "sürükleyip bırakabilirsiniz.": (
        "<b>Receipts / Documents</b> — PDF, image or any file. Double-click to open; you can drag and drop files here.",
        "<b>الإيصالات / المستندات</b> — PDF أو صورة أو أي ملف. انقر مرتين للفتح، ويمكنك سحب الملفات وإفلاتها هنا."),
    "📎 Dekont / belge ekle": ("📎 Add receipt / document", "📎 إضافة إيصال / مستند"),
    "Seçili belgeyi kaldır": ("Remove selected document", "إزالة المستند المحدد"),
    "Dekont / belge seç": ("Select receipt / document", "اختيار إيصال / مستند"),
    "📎 Belgeler": ("📎 Documents", "📎 المستندات"),
    "DİKKAT: Bu kişiye ait {} kayıt ve belgeleri de kalıcı olarak silinecek!": (
        "WARNING: {} records of this person and their documents will also be permanently deleted!",
        "تنبيه: سيتم أيضاً حذف {} قيداً لهذا الشخص مع مستنداتها نهائياً!"),
    "{} tarihli {} kaydı ve belgeleri silinsin mi?": (
        "Delete the {} record of {} and its documents?", "هل تريد حذف قيد {} بمبلغ {} مع مستنداته؟"),
    "Belge yok": ("No document", "لا يوجد مستند"),
    "Bu kayıtta dekont / belge yok. Şimdi eklemek ister misiniz?": (
        "This record has no receipt / document. Add one now?", "لا يوجد إيصال / مستند لهذا القيد. هل تريد إضافته الآن؟"),
    "Dekont / Belgeler": ("Receipts / Documents", "الإيصالات / المستندات"),
    "Bu kayda dekont / belge eklenmedi. Belgesiz kaydedilsin mi?\n\n(Hayır derseniz belge ekleyebilirsiniz.)": (
        "No receipt / document was attached to this record. Save it without a document?\n\n"
        "(Choose No to add a document.)",
        "لم يتم إرفاق إيصال / مستند بهذا القيد. هل تريد حفظه بدون مستند؟\n\n(اختر لا لإضافة مستند.)"),
    "Sadece belgesiz kayıtlar": ("Only records without documents", "القيود بدون مستندات فقط"),
    "Bu kaydın dekontu / belgesi yok": ("This record has no receipt / document", "لا يوجد إيصال / مستند لهذا القيد"),
    "Açmak için çift tıklayın.": ("Double-click to open.", "انقر مرتين للفتح."),
    "Aç": ("Open", "فتح"),
    "Farklı kaydet…": ("Save as…", "حفظ باسم…"),
    # iletişim / kişi defteri (v1.1)
    "Telefonla arama": ("Phone call", "اتصال هاتفي"),
    "Arama": ("Call", "اتصال"),
    "Ara": ("Call", "اتصال"),
    "WhatsApp'ta mesaj yaz": ("Message on WhatsApp", "مراسلة عبر واتساب"),
    "Telegram'da mesaj yaz": ("Message on Telegram", "مراسلة عبر تيليجرام"),
    "Signal'de mesaj yaz": ("Message on Signal", "مراسلة عبر سيجنال"),
    "Bu simgeyi kapat": ("Turn this icon off", "إيقاف هذه الأيقونة"),
    "Kişi bilgilerini düzenle…": ("Edit contact details…", "تعديل بيانات الشخص…"),
    "açık: tıklayınca açılır": ("on: click to open", "مفعّل: انقر للفتح"),
    "kapalı: açmak için tıklayın": ("off: click to turn on", "متوقف: انقر للتفعيل"),
    "açık": ("on", "مفعّل"),
    "kapalı": ("off", "متوقف"),
    "tıklayınca değişir": ("click to change", "انقر للتغيير"),
    "Bu kişi için numara yazılmamış. Kişi Defteri'nden ekleyin.": (
        "No number saved for this person. Add one in the Contact Book.",
        "لا يوجد رقم لهذا الشخص. أضفه من دفتر الأسماء."),
    "Numarayı ülke koduyla yazın (ör. +90 5xx..., +963 9xx...).": (
        "Write the number with its country code (e.g. +90 5xx..., +963 9xx...).",
        "اكتب الرقم مع رمز الدولة (مثل +90 5xx... أو +963 9xx...)."),
    "Bu bağlantıyı açacak program bulunamadı.": ("No program was found to open this link.",
                                                 "لم يتم العثور على برنامج لفتح هذا الرابط."),
    "2. Telefon": ("Phone 2", "الهاتف 2"),
    "WhatsApp no": ("WhatsApp number", "رقم واتساب"),
    "Telegram kullanıcı adı / no": ("Telegram username / number", "اسم مستخدم / رقم تيليجرام"),
    "Signal no": ("Signal number", "رقم سيجنال"),
    "E-posta": ("E-mail", "البريد الإلكتروني"),
    "Adres": ("Address", "العنوان"),
    "Ad Soyad": ("Full name", "الاسم الكامل"),
    "Boşsa Telefon kullanılır": ("Phone is used if empty", "يُستخدم الهاتف إذا تُرك فارغاً"),
    "@kullanici veya +90…": ("@username or +90…", "@اسم_المستخدم أو +90…"),
    "Ulaşma yolları": ("Ways to reach", "طرق التواصل"),
    "📒 Kişi Defteri": ("📒 Contact Book", "📒 دفتر الأسماء"),
    "Kişi Defteri": ("Contact Book", "دفتر الأسماء"),
    "+ Yeni Kişi": ("+ New Person", "+ شخص جديد"),
    "Simgelere tıklayarak açıp kapatabilirsiniz. Diğer bilgileri hücreye çift tıklayıp düzenleyin; "
    "değişiklikler hemen kaydedilir.": (
        "Click the icons to turn them on or off. Double-click a cell to edit it; changes are saved immediately.",
        "انقر على الأيقونات لتفعيلها أو إيقافها. انقر نقراً مزدوجاً على أي خانة لتعديلها؛ تُحفظ التغييرات فوراً."),
    # bulut eşitleme (v1.2)
    "☁ Eşitleme": ("☁ Sync", "☁ المزامنة"),
    "☁ Eşitleme (telefon ⇄ bilgisayar)": ("☁ Sync (phone ⇄ computer)", "☁ المزامنة (الهاتف ⇄ الحاسوب)"),
    "☁ Telefon ile eşitleme": ("☁ Sync with your phone", "☁ المزامنة مع الهاتف"),
    "☁ Şimdi eşitle": ("☁ Sync now", "☁ زامن الآن"),
    "Kayıtlar, belgeler ve hatırlatıcılar kendi Firebase hesabınız üzerinden telefon ve bilgisayarlar arasında "
    "eşitlenir. İnternet yokken program normal çalışır; değişiklikler bağlantı gelince gönderilir.": (
        "Records, documents and reminders are synced between your phone and computers through your own Firebase "
        "account. Without internet the program works normally; changes are sent when the connection is back.",
        "تتم مزامنة القيود والمستندات والتذكيرات بين الهاتف والحواسيب عبر حسابك الخاص في Firebase. يعمل البرنامج "
        "بشكل طبيعي دون إنترنت، وتُرسل التغييرات عند عودة الاتصال."),
    "Firebase API key": ("Firebase API key", "مفتاح Firebase API"),
    "Proje ID": ("Project ID", "معرّف المشروع (Project ID)"),
    "Şifre": ("Password", "كلمة المرور"),
    "Gelişmiş": ("Advanced", "خيارات متقدمة"),
    "Emülatör adresi (yalnızca test)": ("Emulator host (testing only)", "عنوان المحاكي (للاختبار فقط)"),
    "Giriş yap": ("Sign in", "تسجيل الدخول"),
    "Hesap oluştur": ("Create account", "إنشاء حساب"),
    "Çıkış yap": ("Sign out", "تسجيل الخروج"),
    "Giriş yapıldı: {}": ("Signed in: {}", "تم تسجيل الدخول: {}"),
    "Giriş yapılmadı": ("Not signed in", "لم يتم تسجيل الدخول"),
    "Giriş yapılmadı.": ("Not signed in.", "لم يتم تسجيل الدخول."),
    "⟳ Eşitleniyor…": ("⟳ Syncing…", "⟳ جارٍ المزامنة…"),
    "✓ Son eşitleme: {}": ("✓ Last sync: {}", "✓ آخر مزامنة: {}"),
    "Henüz eşitleme yapılmadı.": ("Not synced yet.", "لم تتم المزامنة بعد."),
    "Eşitleme hatası": ("Sync error", "خطأ في المزامنة"),
    "Firestore kuralları (Rules):": ("Firestore rules (Rules):", "قواعد Firestore (Rules):"),
    "Kuralları kopyala": ("Copy rules", "نسخ القواعد"),
    "Kopyalandı ✓": ("Copied ✓", "تم النسخ ✓"),
    "Eşitleme hesabından çıkılsın mı?\nBu bilgisayardaki kayıtlar silinmez; yalnızca eşitleme durur.": (
        "Sign out of the sync account?\nThe records on this computer are not deleted; only syncing stops.",
        "هل تريد تسجيل الخروج من حساب المزامنة؟\nلن تُحذف القيود من هذا الحاسوب؛ ستتوقف المزامنة فقط."),
    "Bu e-posta ile zaten bir hesap var. “Giriş yap” düğmesini kullanın.": (
        "An account with this e-mail already exists. Use “Sign in”.",
        "يوجد حساب بهذا البريد الإلكتروني. استخدم زر “تسجيل الدخول”."),
    "E-posta veya şifre yanlış.": ("Wrong e-mail or password.", "البريد الإلكتروني أو كلمة المرور غير صحيحة."),
    "Şifre çok zayıf; en az 6 karakter olmalı.": ("The password is too weak; use at least 6 characters.",
                                                  "كلمة المرور ضعيفة جداً؛ يجب ألا تقل عن 6 أحرف."),
    "E-posta adresi geçersiz.": ("The e-mail address is invalid.", "عنوان البريد الإلكتروني غير صالح."),
    "E-posta adresini yazın.": ("Enter the e-mail address.", "اكتب عنوان البريد الإلكتروني."),
    "Şifreyi yazın.": ("Enter the password.", "اكتب كلمة المرور."),
    "E-posta/şifre ile giriş bu Firebase projesinde açık değil. Firebase konsolu → Authentication → Sign-in "
    "method → Email/Password → Enable (Etkinleştir).": (
        "E-mail/password sign-in is not enabled in this Firebase project. Firebase console → Authentication → "
        "Sign-in method → Email/Password → Enable.",
        "تسجيل الدخول بالبريد الإلكتروني وكلمة المرور غير مفعّل في مشروع Firebase هذا. وحدة تحكم Firebase ← "
        "Authentication ← Sign-in method ← Email/Password ← Enable."),
    "Bu projede Authentication başlatılmamış. Firebase konsolu → Authentication → Get started; sonra "
    "Email/Password'ü etkinleştirin.": (
        "Authentication has not been set up in this project. Firebase console → Authentication → Get started; "
        "then enable Email/Password.",
        "لم يتم إعداد Authentication في هذا المشروع. وحدة تحكم Firebase ← Authentication ← Get started، ثم فعّل "
        "Email/Password."),
    "API anahtarı geçersiz. Firebase konsolu → Proje ayarları → Genel → Web API Key değerini kopyalayın.": (
        "The API key is invalid. Copy the Web API Key from Firebase console → Project settings → General.",
        "مفتاح API غير صالح. انسخ قيمة Web API Key من وحدة تحكم Firebase ← إعدادات المشروع ← عام."),
    "Çok fazla deneme yapıldı. Biraz bekleyip tekrar deneyin.": (
        "Too many attempts. Wait a little and try again.", "محاولات كثيرة جداً. انتظر قليلاً ثم حاول مرة أخرى."),
    "Bu hesap Firebase'de devre dışı bırakılmış.": ("This account has been disabled in Firebase.",
                                                    "تم تعطيل هذا الحساب في Firebase."),
    "İnternete bağlanılamadı. Kayıtlarınız bu bilgisayarda güvende; bağlantı gelince otomatik eşitlenecek.": (
        "Could not connect to the internet. Your records are safe on this computer and will sync automatically "
        "when the connection is back.",
        "تعذّر الاتصال بالإنترنت. قيودك آمنة على هذا الحاسوب وستتم مزامنتها تلقائياً عند عودة الاتصال."),
    "Firestore kuralları ayarlanmamış (erişim reddedildi). Aşağıdaki kuralları Firestore → Rules sekmesine "
    "yapıştırıp Publish'e basın.": (
        "Firestore rules are not set (access denied). Paste the rules below into Firestore → Rules and press "
        "Publish.",
        "لم يتم ضبط قواعد Firestore (تم رفض الوصول). الصق القواعد أدناه في Firestore ← Rules ثم اضغط Publish."),
    "Firestore veritabanı oluşturulmamış. Firebase konsolu → Firestore Database → Create database. (Proje ID'yi "
    "de kontrol edin.)": (
        "The Firestore database has not been created. Firebase console → Firestore Database → Create database. "
        "(Also check the Project ID.)",
        "لم يتم إنشاء قاعدة بيانات Firestore. وحدة تحكم Firebase ← Firestore Database ← Create database. "
        "(تحقق أيضاً من معرّف المشروع.)"),
    "Oturumun süresi doldu. Lütfen yeniden giriş yapın.": ("Your session has expired. Please sign in again.",
                                                           "انتهت صلاحية الجلسة. يرجى تسجيل الدخول من جديد."),
    "Önce Firebase API anahtarını ve Proje ID'yi yazın.": ("First enter the Firebase API key and Project ID.",
                                                          "أدخل أولاً مفتاح Firebase API ومعرّف المشروع."),
    "Sunucu hatası. Biraz sonra tekrar denenecek.": ("Server error. It will be retried shortly.",
                                                    "خطأ في الخادم. ستتم إعادة المحاولة بعد قليل."),
    "Beklenmeyen bir hata oluştu.": ("An unexpected error occurred.", "حدث خطأ غير متوقع."),
    "<b>Kurulum (Firebase konsolunda bir kez yapılır)</b><ol>"
    "<li><b>console.firebase.google.com</b> adresinde bir proje oluşturun. Proje ayarları → Genel → "
    "<i>Web uygulaması ekle</i> (&lt;/&gt;) deyin; görünen <b>apiKey</b> ve <b>projectId</b> "
    "değerlerini soldaki kutulara yazın.</li>"
    "<li><b>Authentication</b> → Get started → Sign-in method → <b>Email/Password</b> → Enable "
    "(Etkinleştir) → Save.</li>"
    "<li><b>Firestore Database</b> → Create database (veritabanı oluştur). Sonra <b>Rules</b> "
    "sekmesine aşağıdaki kuralları yapıştırıp <b>Publish</b>'e basın.</li></ol>"
    "İlk cihazda <b>Hesap oluştur</b>, diğer cihazlarda (telefon, öbür bilgisayar) aynı e-posta ve "
    "şifreyle <b>Giriş yap</b>. Şifre bu bilgisayara kaydedilmez.": (
        "<b>Setup (done once in the Firebase console)</b><ol>"
        "<li>Create a project at <b>console.firebase.google.com</b>. Project settings → General → <i>Add app → "
        "Web</i> (&lt;/&gt;); enter the shown <b>apiKey</b> and <b>projectId</b> values in the boxes on the "
        "left.</li>"
        "<li><b>Authentication</b> → Get started → Sign-in method → <b>Email/Password</b> → Enable → Save.</li>"
        "<li><b>Firestore Database</b> → Create database. Then paste the rules below into the <b>Rules</b> tab "
        "and press <b>Publish</b>.</li></ol>"
        "On the first device press <b>Create account</b>; on the other devices (phone, other computer) "
        "<b>Sign in</b> with the same e-mail and password. The password is not stored on this computer.",
        "<b>الإعداد (مرة واحدة في وحدة تحكم Firebase)</b><ol>"
        "<li>أنشئ مشروعاً على <b>console.firebase.google.com</b>. إعدادات المشروع ← عام ← <i>إضافة تطبيق ويب</i> "
        "(&lt;/&gt;)، ثم اكتب قيمتي <b>apiKey</b> و<b>projectId</b> الظاهرتين في الخانات المجاورة.</li>"
        "<li><b>Authentication</b> ← Get started ← Sign-in method ← <b>Email/Password</b> ← Enable ← Save.</li>"
        "<li><b>Firestore Database</b> ← Create database. ثم الصق القواعد أدناه في تبويب <b>Rules</b> واضغط "
        "<b>Publish</b>.</li></ol>"
        "على الجهاز الأول اضغط <b>إنشاء حساب</b>، وعلى الأجهزة الأخرى (الهاتف، الحاسوب الآخر) <b>سجّل الدخول</b> "
        "بنفس البريد الإلكتروني وكلمة المرور. لا تُحفظ كلمة المرور على هذا الحاسوب."),
    # uygulama içi güncelleme (v1.4)
    "⬆ Güncelleme": ("⬆ Update", "⬆ التحديث"),
    "⬆ Güncelle": ("⬆ Update now", "⬆ حدّث الآن"),
    "Tekrar denetle": ("Check again", "تحقق مرة أخرى"),
    "Kullandığınız sürüm: {}": ("Your version: {}", "إصدارك الحالي: {}"),
    "Yeni sürüm denetleniyor…": ("Checking for a new version…", "جارٍ البحث عن إصدار جديد…"),
    "Program güncel. Yeni sürüm yok.": ("The program is up to date.", "البرنامج محدّث. لا يوجد إصدار جديد."),
    "Yeni sürüm hazır: {}": ("New version ready: {}", "إصدار جديد جاهز: {}"),
    "⬆ Yeni sürüm: {}": ("⬆ New version: {}", "⬆ إصدار جديد: {}"),
    "⬆ Güncelleniyor…": ("⬆ Updating…", "⬆ جارٍ التحديث…"),
    "Güncelleme indiriliyor… %{}": ("Downloading update… {}%", "جارٍ تنزيل التحديث… {}٪"),
    "Güncelleme indiriliyor…": ("Downloading update…", "جارٍ تنزيل التحديث…"),
    "{} / {} MB": ("{} / {} MB", "{} / {} MB"),
    "{} MB": ("{} MB", "{} MB"),
    "{} MB/sn": ("{} MB/s", "{} MB/s"),
    "{} KB/sn": ("{} KB/s", "{} KB/s"),
    "~{} sn": ("~{} s", "~{} s"),
    "~{} dk": ("~{} min", "~{} min"),
    "~{} dk {} sn": ("~{} min {} s", "~{} min {} s"),
    "Kalan:": ("Left:", "المتبقي:"),
    "Hız:": ("Speed:", "السرعة:"),
    "Kalan süre:": ("Time left:", "الوقت المتبقي:"),
    "Güncelleme indiriliyor… {}": ("Downloading update… {}", "جارٍ تنزيل التحديث… {}"),
    "%{} · {} / {} MB · kalan {} MB · {}": ("{}% · {} / {} MB · {} MB left · {}", "{}% · {} / {} ميغابايت · متبقٍ {} ميغابايت · {}"),
    "☁ Eşitle": ("☁ Sync", "☁ مزامنة"),
    "Eşitleme kapalı (giriş yapılmamış)": ("Sync off (not signed in)", "المزامنة متوقفة (لم يتم تسجيل الدخول)"),
    "☁ ⟳ Eşitleniyor…": ("☁ ⟳ Syncing…", "☁ ⟳ جارٍ المزامنة…"),
    "☁ ! Eşitle": ("☁ ! Sync", "☁ ! مزامنة"),
    "Tıklayın: şimdi eşitle · Sağ tık: eşitleme ayarları": ("Click: sync now · Right-click: sync settings", "انقر: مزامنة الآن · زر يمين: إعدادات المزامنة"),
    "Güncelleme kuruldu. Program yeniden başlatılıyor…": ("Update installed. Restarting…",
                                                         "تم تثبيت التحديث. جارٍ إعادة التشغيل…"),
    "Güncelleme kuruldu. Programı kapatıp yeniden açın.": ("Update installed. Close and reopen the program.",
                                                          "تم تثبيت التحديث. أغلق البرنامج وافتحه من جديد."),
    "Güncelleme sadece program dosyalarını yeniler; kayıtlarınız, kişileriniz ve dekontlarınız olduğu gibi kalır.": (
        "The update only replaces program files; your records, contacts and receipts stay as they are.",
        "التحديث يستبدل ملفات البرنامج فقط؛ تبقى سجلاتك وجهات الاتصال والإيصالات كما هي."),
    "Güncelleme hatası: {}": ("Update error: {}", "خطأ في التحديث: {}"),
    "Güncelleme sunucusu ayarlı değil. ☁ Eşitleme ekranında Firebase bilgilerini girin.": (
        "No update server is set. Enter the Firebase details in the ☁ Sync screen.",
        "خادم التحديث غير مضبوط. أدخل بيانات Firebase في شاشة ☁ المزامنة."),
    "Güncelleme bilgisine erişilemedi (Firestore kuralları).": ("Could not read the update info (Firestore rules).",
                                                               "تعذّر قراءة معلومات التحديث (قواعد Firestore)."),
    "İndirilen güncelleme bozuk, tekrar deneyin.": ("The downloaded update is damaged, try again.",
                                                  "التحديث الذي تم تنزيله تالف، حاول مرة أخرى."),
    "Program klasörüne yazılamadı. Programı yazma izni olan bir klasörde çalıştırın.": (
        "Could not write to the program folder. Run the program from a folder you can write to.",
        "تعذّرت الكتابة في مجلد البرنامج. شغّل البرنامج من مجلد لديك صلاحية الكتابة فيه."),
    "Bu kurulumda güncelleme yeni kurulum dosyasıyla yapılır.": ("This installation is updated with a new setup file.",
                                                                "يتم تحديث هذا التثبيت بملف تثبيت جديد."),
    # otomatik güncelleme denetimi ve bildirimi (v1.6)
    "⚙ Ayarlar": ("⚙ Settings", "⚙ الإعدادات"),
    "⚙ Denetim ayarları": ("⚙ Check settings", "⚙ إعدادات الفحص"),
    "⬆ Güncelleme denetimi": ("⬆ Update check", "⬆ فحص التحديثات"),
    "Program her açıldığında yeni sürümü denetle": ("Check for a new version every time the program starts",
                                                   "ابحث عن إصدار جديد عند كل تشغيل للبرنامج"),
    "Belirli aralıklarla denetle, her:": ("Check at regular intervals, every:", "افحص على فترات منتظمة، كل:"),
    "saniye": ("seconds", "ثانية"),
    "dakika": ("minutes", "دقيقة"),
    "5 sn": ("5 sec", "5 ث"),
    "30 sn": ("30 sec", "30 ث"),
    "1 dk": ("1 min", "1 د"),
    "5 dk": ("5 min", "5 د"),
    "30 dk": ("30 min", "30 د"),
    "1 saat": ("1 hour", "1 ساعة"),
    "6 saat": ("6 hours", "6 ساعات"),
    "24 saat": ("24 hours", "24 ساعة"),
    "Yeni sürüm bulununca bildirim göster": ("Show a notification when a new version is found",
                                             "أظهر إشعارًا عند العثور على إصدار جديد"),
    "Yalnızca açılışta denetim için “Belirli aralıklarla” kutusunu boş bırakın. En kısa aralık {} saniyedir. Bildirim her yeni sürüm için bir kez gelir.": (
        "To check only at startup, leave “regular intervals” unticked. The shortest interval is {} seconds. "
        "You are notified once for each new version.",
        "للفحص عند التشغيل فقط اترك خيار «على فترات منتظمة» فارغًا. أقصر فترة هي {} ثوانٍ. "
        "يصلك الإشعار مرة واحدة لكل إصدار جديد."),
    "En kısa aralık {} saniyedir.": ("The shortest interval is {} seconds.", "أقصر فترة هي {} ثوانٍ."),
    "Ayarlar kaydedilemedi: {}": ("Settings could not be saved: {}", "تعذّر حفظ الإعدادات: {}"),
    "Kurmak için tıklayın.": ("Click to install.", "انقر للتثبيت."),
    "⬆ Şimdi güncelle": ("⬆ Update now", "⬆ حدّث الآن"),
    "Sonra": ("Later", "لاحقًا"),
    "Program her açıldığında yeni sürüm denetlenir.": ("A new version is checked every time the program starts.",
                                                      "يتم البحث عن إصدار جديد عند كل تشغيل للبرنامج."),
}


def _settings_path():
    from db import data_dir
    return os.path.join(data_dir(), "ayarlar.json")


def _installer_default():
    """Kurulumda seçilen dil (kurulum programı dil.txt dosyasına yazar)."""
    import sys
    base = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
    try:
        with open(os.path.join(base, "dil.txt"), encoding="utf-8-sig") as f:
            return f.read().strip()
    except OSError:
        return "tr"


def load_language():
    global _lang
    try:
        with open(_settings_path(), encoding="utf-8") as f:
            lang = json.load(f).get("dil", "tr")
    except (OSError, ValueError):
        lang = _installer_default()
    _lang = lang if lang in LANGS else "tr"
    return _lang


def set_language(lang):
    global _lang
    _lang = lang
    try:
        with open(_settings_path(), "w", encoding="utf-8") as f:
            json.dump({"dil": lang}, f)
    except OSError:
        pass


def lang():
    return _lang


def is_rtl():
    return _lang == "ar"


def _(text):
    if _lang == "tr":
        return text
    pair = T.get(text)
    if pair is None:
        return text
    return pair[0] if _lang == "en" else pair[1]
