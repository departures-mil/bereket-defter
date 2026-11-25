"""v1.22 eklerinin çevirileri (Türkçe anahtar: (English, العربية)). i18n.T'ye eklenir."""
import i18n

i18n.T.update({
    # kilit / PIN
    "Devam etmek için PIN kodunuzu girin.": ("Enter your PIN to continue.", "أدخل رمز PIN للمتابعة."),
    "Kilidi aç": ("Unlock", "فتح القفل"),
    "PIN'i unuttum": ("I forgot my PIN", "نسيت رمز PIN"),
    "Çok fazla hatalı deneme. {} saniye sonra tekrar deneyin.": ("Too many wrong attempts. Try again in {} seconds.",
                                                                 "محاولات خاطئة كثيرة. حاول مجدداً بعد {} ثانية."),
    "PIN yanlış.": ("Wrong PIN.", "رمز PIN غير صحيح."),
    "Güvenliğiniz için PIN buradan sıfırlanamaz. Programı kapatın, veri klasöründeki “guvenlik.json” dosyasını silin ve "
    "programı yeniden açın; kayıtlarınız silinmez.\n\nVeri klasörü:\n{}": (
        "For your security the PIN cannot be reset here. Close the program, delete the “guvenlik.json” file in the data folder and "
        "open the program again; your records are not deleted.\n\nData folder:\n{}",
        "لأمانك لا يمكن إعادة تعيين رمز PIN من هنا. أغلق البرنامج واحذف الملف «guvenlik.json» من مجلد البيانات ثم افتح البرنامج "
        "مجدداً؛ لن تُحذف سجلاتك.\n\nمجلد البيانات:\n{}"),
    "Güvenlik ve otomatik yedek": ("Security and automatic backup", "الأمان والنسخ الاحتياطي التلقائي"),
    "PIN kilidi, tutarları gizleme ve her gün kendiliğinden alınan yedekler. Bu ayarlar yalnız bu bilgisayarda geçerlidir.": (
        "PIN lock, hiding amounts and backups taken automatically every day. These settings apply to this computer only.",
        "قفل PIN وإخفاء المبالغ والنسخ الاحتياطية التي تؤخذ تلقائياً كل يوم. تسري هذه الإعدادات على هذا الحاسوب فقط."),
    "PIN kilidi: açık": ("PIN lock: on", "قفل PIN: مفعّل"),
    "PIN kilidi: kapalı": ("PIN lock: off", "قفل PIN: غير مفعّل"),
    "PIN belirle / değiştir": ("Set / change PIN", "تعيين / تغيير رمز PIN"),
    "PIN'i kaldır": ("Remove PIN", "إزالة رمز PIN"),
    "Şimdi kilitle": ("Lock now", "القفل الآن"),
    "Kendiliğinden kilitleme": ("Do not lock automatically", "عدم القفل تلقائياً"),
    "1 dakika boşta kalınca": ("After 1 minute idle", "بعد دقيقة من عدم الاستخدام"),
    "5 dakika boşta kalınca": ("After 5 minutes idle", "بعد 5 دقائق من عدم الاستخدام"),
    "15 dakika boşta kalınca": ("After 15 minutes idle", "بعد 15 دقيقة من عدم الاستخدام"),
    "30 dakika boşta kalınca": ("After 30 minutes idle", "بعد 30 دقيقة من عدم الاستخدام"),
    "Tutarları gizle (ekranda ••••• görünür; Ctrl+H)": ("Hide amounts (shown as ••••• on screen; Ctrl+H)",
                                                         "إخفاء المبالغ (تظهر ••••• على الشاشة؛ Ctrl+H)"),
    "Her gün otomatik yedek al": ("Take an automatic backup every day", "أخذ نسخة احتياطية تلقائية كل يوم"),
    "Son yedek: {}": ("Last backup: {}", "آخر نسخة احتياطية: {}"),
    "Henüz yedek yok.": ("No backups yet.", "لا توجد نسخ احتياطية بعد."),
    "Yedekleri gör / geri getir": ("View backups / recover", "عرض النسخ الاحتياطية / الاسترجاع"),
    "Yedek klasörünü aç": ("Open backup folder", "فتح مجلد النسخ الاحتياطية"),
    "Mesajların ve senetlerin altına yazılacak adınız": ("Your name, written under messages and notes",
                                                         "اسمك الذي يُكتب في نهاية الرسائل والسندات"),
    "Adınız": ("Your name", "اسمك"),
    # kısayollar
    "Klavye kısayolları": ("Keyboard shortcuts", "اختصارات لوحة المفاتيح"),
    "Yeni kayıt: Verdim": ("New record: Gave", "سجل جديد: أعطيت"),
    "Yeni kayıt: Aldım": ("New record: Received", "سجل جديد: استلمت"),
    "Hızlı kayıt": ("Quick entry", "إدخال سريع"),
    "Kişi ara": ("Search people", "البحث عن شخص"),
    "Döküm al": ("Account statement", "كشف الحساب"),
    "Raporlar": ("Reports", "التقارير"),
    "Mesaj / mutabakat": ("Message / reconciliation", "رسالة / مطابقة الحساب"),
    "Tutarları gizle / göster": ("Hide / show amounts", "إخفاء / إظهار المبالغ"),
    "Kilitle": ("Lock", "قفل"),
    "Eşitle": ("Sync", "مزامنة"),
    "Seçili kaydı sil": ("Delete the selected record", "حذف السجل المحدد"),
    "Şu anki PIN": ("Current PIN", "رمز PIN الحالي"),
    "Yeni PIN (4–8 rakam)": ("New PIN (4–8 digits)", "رمز PIN الجديد (4–8 أرقام)"),
    "Yeni PIN (tekrar)": ("New PIN (again)", "رمز PIN الجديد (مرة أخرى)"),
    "PIN bu bilgisayarda saklanır ve eşitlenmez. Telefonda ayrı PIN belirleyebilirsiniz.": (
        "The PIN is stored on this computer and is not synced. You can set a separate PIN on the phone.",
        "يُحفظ رمز PIN على هذا الحاسوب ولا تتم مزامنته. يمكنك تعيين رمز منفصل على الهاتف."),
    "PIN": ("PIN", "رمز PIN"),
    "Şu anki PIN yanlış.": ("The current PIN is wrong.", "رمز PIN الحالي غير صحيح."),
    "PIN 4–8 rakamdan oluşmalı.": ("The PIN must be 4–8 digits.", "يجب أن يتكون رمز PIN من 4 إلى 8 أرقام."),
    "İki PIN aynı değil.": ("The two PINs do not match.", "رمزا PIN غير متطابقين."),
    # yedekler
    "Yedekler ve geri getirme": ("Backups and recovery", "النسخ الاحتياطية والاسترجاع"),
    "Bir yedek seçin: içinde ne olduğu ve bu cihazda eksik olanlar görünür. “Eksikleri geri getir” yalnız eksik kayıtları ekler; "
    "mevcut kayıtlarınıza dokunmaz, hiçbir şeyi silmez.": (
        "Select a backup to see what it contains and what is missing on this device. “Recover missing items” only adds the missing "
        "records; it does not touch your existing records and deletes nothing.",
        "اختر نسخة احتياطية لترى محتواها وما ينقص على هذا الجهاز. «استرجاع الناقص» يضيف السجلات الناقصة فقط؛ "
        "ولا يمسّ سجلاتك الحالية ولا يحذف شيئاً."),
    "Başka bir yedek dosyası seç…": ("Choose another backup file…", "اختيار ملف نسخة احتياطية آخر…"),
    "Şimdi yedek al": ("Back up now", "نسخ احتياطي الآن"),
    "Eksikleri geri getir": ("Recover missing items", "استرجاع الناقص"),
    "Bu dosya geçerli bir yedek değil.": ("This file is not a valid backup.", "هذا الملف ليس نسخة احتياطية صالحة."),
    "Kayıt": ("Record", "سجل"),
    "Hatırlatıcı": ("Reminder", "تذكير"),
    "{}: {} (bu cihazda eksik: {})": ("{}: {} (missing on this device: {})", "{}: {} (الناقص على هذا الجهاز: {})"),
    "Geri getirilecek bir şey yok; bu yedekteki her şey bu cihazda var.": (
        "Nothing to recover; everything in this backup already exists on this device.",
        "لا يوجد ما يُسترجع؛ كل ما في هذه النسخة موجود على هذا الجهاز."),
    "Bu yedekte olup bu cihazda olmayan {} öğe var.": ("{} items in this backup are not on this device.",
                                                      "في هذه النسخة {} عنصراً غير موجود على هذا الجهاز."),
    "Yedek dosyası": ("Backup file", "ملف النسخة الاحتياطية"),
    "Yedekte olup bu cihazda olmayan kayıtlar eklensin mi? Mevcut kayıtlarınız değişmez.": (
        "Add the records that are in the backup but not on this device? Your existing records will not change.",
        "هل تُضاف السجلات الموجودة في النسخة الاحتياطية وغير الموجودة على هذا الجهاز؟ لن تتغير سجلاتك الحالية."),
    "Geri getirildi: {} kişi, {} kayıt, {} hatırlatıcı, {} belge.": (
        "Recovered: {} people, {} records, {} reminders, {} documents.",
        "تم الاسترجاع: {} شخص، {} سجل، {} تذكير، {} مستند."),
    # taksit
    "Taksit / ödeme planı": ("Instalment / payment plan", "خطة الأقساط / السداد"),
    "Toplam tutarı eşit taksitlere böler ve her taksit için bir hatırlatıcı kurar. Ödeme geldikçe “Aldım” / “Verdim” kaydını "
    "girip hatırlatıcıyı tamamlandı yapın.": (
        "Splits the total into equal instalments and sets a reminder for each one. As payments arrive, enter a “Received” / “Gave” "
        "record and mark the reminder as done.",
        "يقسّم المبلغ الإجمالي إلى أقساط متساوية ويضبط تذكيراً لكل قسط. عند كل دفعة أدخل سجل «استلمت» / «أعطيت» "
        "واجعل التذكير مكتملاً."),
    "Toplam tutar": ("Total amount", "المبلغ الإجمالي"),
    "Taksit sayısı": ("Number of instalments", "عدد الأقساط"),
    "Her ay": ("Monthly", "شهرياً"),
    "15 günde bir": ("Every 15 days", "كل 15 يوماً"),
    "Her hafta": ("Weekly", "أسبوعياً"),
    "Sıklık": ("Frequency", "التكرار"),
    "İlk taksit": ("First instalment", "القسط الأول"),
    "Planı kaydet": ("Save plan", "حفظ الخطة"),
    "{} taksit × {}": ("{} instalments × {}", "{} أقساط × {}"),
    "Toplam tutarı yazın.": ("Enter the total amount.", "أدخل المبلغ الإجمالي."),
    "Taksit {}/{}": ("Instalment {}/{}", "القسط {}/{}"),
    # mesaj
    "Bakiye bildirimi ve mutabakat": ("Balance notice and reconciliation", "إشعار الرصيد ومطابقة الحساب"),
    "Kibar ödeme hatırlatması": ("Polite payment reminder", "تذكير لطيف بالسداد"),
    "Hesap kapandı / teşekkür": ("Account settled / thank you", "إغلاق الحساب / شكر"),
    "Mesaj": ("Message", "الرسالة"),
    "Metni dilediğiniz gibi düzeltebilirsiniz. Mutabakat mesajına karşı taraf “Onaylıyorum” diye cevap verirse hesaplarınız "
    "uyuşuyor demektir.": (
        "You can edit the text as you like. If the other party replies “Confirmed” to the reconciliation message, your accounts match.",
        "يمكنك تعديل النص كما تشاء. إذا ردّ الطرف الآخر على رسالة المطابقة بـ«أوافق» فهذا يعني أن حساباتكما متطابقة."),
    "Kopyalandı": ("Copied", "تم النسخ"),
    "Mesaj panoya kopyalandı; Telegram'da sohbete yapıştırın (Ctrl+V).": (
        "The message was copied to the clipboard; paste it into the Telegram chat (Ctrl+V).",
        "نُسخت الرسالة إلى الحافظة؛ الصقها في محادثة Telegram (Ctrl+V)."),
    # senet
    "Borç senedi": ("Promissory note", "سند دين"),
    "Bakara 282'deki gibi: borç, vadesiyle birlikte yazılır; bir kâtip yazar ve iki şahit bulunur. Senedi yazdırıp taraflara imzalatın.": (
        "As in al-Baqarah 2:282: the debt is written down together with its due date, a scribe writes it and two witnesses are present. "
        "Print the note and have the parties sign it.",
        "كما في سورة البقرة (282): يُكتب الدين مع أجله، ويكتبه كاتب بحضور شاهدين. اطبع السند واجعل الطرفين يوقّعان عليه."),
    "Borçlu ile alacaklıyı yer değiştir": ("Swap debtor and creditor", "تبديل المدين والدائن"),
    "Borçlu": ("Debtor", "المدين"),
    "Alacaklı": ("Creditor", "الدائن"),
    "ör. bin beş yüz dolar": ("e.g. one thousand five hundred dollars", "مثال: ألف وخمسمئة دولار"),
    "Yazıyla (isteğe bağlı)": ("In words (optional)", "كتابةً (اختياري)"),
    "Düzenlenme tarihi": ("Date of issue", "تاريخ التحرير"),
    "Vade": ("Due date", "تاريخ الاستحقاق"),
    "ör. elden nakit, banka havalesi": ("e.g. cash in hand, bank transfer", "مثال: نقداً يداً بيد، تحويل مصرفي"),
    "Ödeme şekli (isteğe bağlı)": ("Payment method (optional)", "طريقة السداد (اختياري)"),
    "Yazan (kâtip)": ("Scribe (written by)", "الكاتب"),
    "1. şahit": ("Witness 1", "الشاهد الأول"),
    "2. şahit": ("Witness 2", "الشاهد الثاني"),
    "Senedin dili": ("Language of the note", "لغة السند"),
    "Önizle": ("Preview", "معاينة"),
    # hızlı kayıt
    "ör. Ahmet'e 500 TL verdim kira için": ("e.g. gave Ahmet 500 TL for rent", "مثال: أعطيت أحمد 500 ليرة تركية ثمن الإيجار"),
    "Yazın": ("Type", "اكتب"),
    "Örnekler: “Ali'den 200 dolar aldım” · “received 50$ from John” · “أعطيت محمد 100 دولار”. İnternet gerekmez; aşağıdaki "
    "alanları kontrol edip kaydedin.": (
        "Examples: “Ali'den 200 dolar aldım” · “received 50$ from John” · “أعطيت محمد 100 دولار”. No internet needed; check the "
        "fields below and save.",
        "أمثلة: «Ali'den 200 dolar aldım» · «received 50$ from John» · «أعطيت محمد 100 دولار». لا حاجة للإنترنت؛ "
        "تحقق من الحقول أدناه ثم احفظ."),
    "“{}” kayıtlı değil; kaydedince yeni kişi olarak eklenir.": ("“{}” is not registered; it will be added as a new person when you save.",
                                                                "«{}» غير مسجل؛ سيُضاف كشخص جديد عند الحفظ."),
    "Kişi adını yazın.": ("Enter the person's name.", "أدخل اسم الشخص."),
    "Tutarı yazın.": ("Enter the amount.", "أدخل المبلغ."),
    # geri al
    "Geri al": ("Undo", "تراجع"),
    "Ayarlar → Arşiv'de de durur.": ("It is also kept in Settings → Archive.", "ويبقى محفوظاً أيضاً في الإعدادات ← الأرشيف."),
    "Geri alındı": ("Restored", "تمت الاستعادة"),
    # raporlar
    "Yenile": ("Refresh", "تحديث"),
    "Kayıtları CSV olarak dışa aktar": ("Export records as CSV", "تصدير السجلات بصيغة CSV"),
    "Bakiyeleri CSV olarak dışa aktar": ("Export balances as CSV", "تصدير الأرصدة بصيغة CSV"),
    "CSV'den içe aktar…": ("Import from CSV…", "استيراد من CSV…"),
    "Genel durum": ("Overall position", "الوضع العام"),
    "Net": ("Net", "الصافي"),
    "Kişi (alacak / verecek)": ("People (receivable / payable)", "الأشخاص (مستحق لي / مستحق عليّ)"),
    "Kurlar (elle):": ("Exchange rates (manual):", "أسعار الصرف (يدوياً):"),
    "Yaşlandırma (son hareketten bu yana geçen gün)": ("Aging (days since the last transaction)", "أعمار الأرصدة (الأيام منذ آخر حركة)"),
    "Açık bakiyeler, kişiyle o para biriminde yapılan son işlemden bu yana geçen süreye göre gruplanır. Uzun süredir hareketsiz "
    "alacaklar takip gerektirir.": (
        "Open balances are grouped by the time since the last transaction with that person in that currency. Receivables that have "
        "been inactive for a long time need follow-up.",
        "تُجمَّع الأرصدة المفتوحة حسب المدة المنقضية منذ آخر معاملة مع الشخص بتلك العملة. المستحقات الراكدة منذ مدة طويلة تحتاج إلى متابعة."),
    "En büyük bakiyeler": ("Largest balances", "أكبر الأرصدة"),
    "Alacaklı olduğum kişiler": ("People who owe me", "الأشخاص المدينون لي"),
    "Son işlem": ("Last transaction", "آخر معاملة"),
    "Borçlu olduğum kişiler": ("People I owe", "الأشخاص الدائنون لي"),
    "Aylık hareket (son 12 ay)": ("Monthly activity (last 12 months)", "الحركة الشهرية (آخر 12 شهراً)"),
    "Vadesi geçmiş hatırlatıcılar": ("Overdue reminders", "التذكيرات المتأخرة"),
    "Net durum (dolar karşılığı): {}": ("Net position (USD equivalent): {}", "الوضع الصافي (بما يعادل الدولار): {}"),
    "{} için kur girilmediğinden hesaba katılmadı.": ("{} not included because no exchange rate was entered.",
                                                      "لم تُحتسب {} لعدم إدخال سعر الصرف."),
    "{} gün": ("{} days", "{} يوماً"),
    "Toplam {} hatırlatıcının vadesi geçti.": ("{} reminders are overdue in total.", "تأخر موعد {} تذكيرات إجمالاً."),
    "Vadesi geçmiş hatırlatıcı yok.": ("No overdue reminders.", "لا توجد تذكيرات متأخرة."),
    "CSV kaydet": ("Save CSV", "حفظ CSV"),
    "Kaydedildi: {}": ("Saved: {}", "تم الحفظ: {}"),
    "{} kayıt bulundu.": ("{} records found.", "تم العثور على {} سجل."),
    "Eklenecek: {} kayıt, {} yeni kişi.": ("To be added: {} records, {} new people.", "سيُضاف: {} سجل، {} شخص جديد."),
    "Zaten var olduğu için atlanacak: {}": ("Skipped because they already exist: {}", "سيُتجاوز لوجوده مسبقاً: {}"),
    "tarih okunamadı": ("date could not be read", "تعذّرت قراءة التاريخ"),
    "kişi boş": ("person is empty", "الشخص فارغ"),
    "tutar okunamadı": ("amount could not be read", "تعذّرت قراءة المبلغ"),
    "para birimi bilinmiyor": ("unknown currency", "عملة غير معروفة"),
    "işlem (Verdim/Aldım) bilinmiyor": ("unknown type (Gave/Received)", "نوع العملية (أعطيت/استلمت) غير معروف"),
    "Okunamayan satırlar:": ("Rows that could not be read:", "الأسطر التي تعذّرت قراءتها:"),
    "Satır {}: {}": ("Row {}: {}", "السطر {}: {}"),
    "Beklenen sütunlar: Tarih; Kişi; İşlem (Verdim/Aldım); Birim (USD/TRY/SYP); Tutar; Açıklama": (
        "Expected columns: Date; Person; Type (Gave/Received); Currency (USD/TRY/SYP); Amount; Description",
        "الأعمدة المتوقعة: التاريخ؛ الشخص؛ العملية (أعطيت/استلمت)؛ العملة (USD/TRY/SYP)؛ المبلغ؛ البيان"),
    "İçe aktarılsın mı?": ("Import now?", "هل يتم الاستيراد؟"),
    "{} kayıt ve {} yeni kişi eklendi.": ("{} records and {} new people were added.", "أُضيف {} سجل و{} شخص جديد."),
    # ana pencere
    "✦ Hızlı kayıt: ör. Ahmet'e 500 TL verdim": ("✦ Quick entry: e.g. gave Ahmet 500 TL", "✦ إدخال سريع: مثال: أعطيت أحمد 500 ليرة تركية"),
    "Cümleyi yazıp Enter'a basın; kişi, tutar, para birimi ve işlem kendiliğinden doldurulur (Ctrl+K).": (
        "Type the sentence and press Enter; the person, amount, currency and type are filled in automatically (Ctrl+K).",
        "اكتب الجملة واضغط Enter؛ يُملأ الشخص والمبلغ والعملة ونوع العملية تلقائياً (Ctrl+K)."),
    "✦ Hızlı kayıt": ("✦ Quick entry", "✦ إدخال سريع"),
    "Tutarları gizle / göster (Ctrl+H)": ("Hide / show amounts (Ctrl+H)", "إخفاء / إظهار المبالغ (Ctrl+H)"),
    "💬 Mesaj / Mutabakat": ("💬 Message / Reconcile", "💬 رسالة / مطابقة"),
    "📅 Taksit Planı": ("📅 Instalment Plan", "📅 خطة الأقساط"),
    "📜 Borç Senedi": ("📜 Promissory Note", "📜 سند دين"),
    "Vadesi geçmiş hatırlatıcı var": ("Has an overdue reminder", "لديه تذكير متأخر"),
    "🏷 Bütün etiketler": ("🏷 All tags", "🏷 كل الوسوم"),
    "Etiketler": ("Tags", "الوسوم"),
    "ör. aile, iş, komşu (virgülle ayırın)": ("e.g. family, work, neighbour (separate with commas)", "مثال: عائلة، عمل، جار (افصل بفاصلة)"),
    "Önce soldaki listeden bir kişi seçin.": ("First select a person from the list on the left.", "اختر شخصاً من القائمة أولاً."),
    "Bu kişiye ait {} kayıt ve belgeleri de arşive taşınır; Ayarlar → Arşiv'den geri alabilirsiniz.": (
        "This person's {} records and their documents are also moved to the archive; you can restore them from Settings → Archive.",
        "تُنقل أيضاً سجلات هذا الشخص ({}) ومستنداتها إلى الأرشيف؛ ويمكنك استعادتها من الإعدادات ← الأرشيف."),
    "“{}” silindi": ("“{}” deleted", "تم حذف «{}»"),
    "Hoş geldiniz! Başlamak için soldan “+ Kişi Ekle”ye basın ya da üstteki hızlı kayıt kutusuna “Ahmet'e 500 TL verdim” gibi "
    "yazıp Enter'a basın.": (
        "Welcome! To start, press “+ Add Person” on the left, or type something like “gave Ahmet 500 TL” into the quick entry box "
        "at the top and press Enter.",
        "أهلاً بك! للبدء اضغط «+ إضافة شخص» من القائمة، أو اكتب في مربع الإدخال السريع في الأعلى عبارة مثل "
        "«أعطيت أحمد 500 ليرة تركية» ثم اضغط Enter."),
    "Süzgece uyan kayıt yok. Arama kutusunu ya da para birimi seçimini temizleyin.": (
        "No records match the filter. Clear the search box or the currency selection.",
        "لا توجد سجلات مطابقة للتصفية. امسح مربع البحث أو اختيار العملة."),
    "Bu sayfada henüz kayıt yok. “+ Verdim (Çıktı)” ya da “+ Aldım (Girdi)” ile ilk kaydı ekleyin.": (
        "No records here yet. Add the first one with “+ Gave (Out)” or “+ Received (In)”.",
        "لا توجد سجلات هنا بعد. أضف أول سجل عبر «+ أعطيت (صادر)» أو «+ استلمت (وارد)»."),
    "Kayıt silindi": ("Record deleted", "تم حذف السجل"),
    # telefon
    "Güvenliğiniz için PIN buradan sıfırlanamaz. Uygulamanın verilerini sıfırlamadan PIN kaldırılamaz; kayıtlarınız eşitlendiyse bulutta durur. Yardım için Ayarlar → Admin ile iletişim.": (
        "For your security the PIN cannot be reset here. It can only be removed by clearing the app's data; records that were synced stay in the cloud. "
        "For help: Settings → Contact the admin.",
        "لأمانك لا يمكن إعادة تعيين رمز PIN من هنا. لا يُزال الرمز إلا بمسح بيانات التطبيق؛ والسجلات التي تمت مزامنتها تبقى في السحابة. "
        "للمساعدة: الإعدادات ← التواصل مع المسؤول."),
    "PIN bu telefonda saklanır ve eşitlenmez. Bilgisayarda ayrı PIN belirleyebilirsiniz.": (
        "The PIN is stored on this phone and is not synced. You can set a separate PIN on the computer.",
        "يُحفظ رمز PIN على هذا الهاتف ولا تتم مزامنته. يمكنك تعيين رمز منفصل على الحاسوب."),
    "Otomatik yedek (bu telefonda)": ("Automatic backup (on this phone)", "نسخة احتياطية تلقائية (على هذا الهاتف)"),
    "Kopyalanamadı": ("Could not copy", "تعذّر النسخ"),
    "Hoş geldiniz! Başlamak için “+ Kişi Ekle”ye basın ya da üstteki hızlı kayıt kutusuna “Ahmet'e 500 TL verdim” gibi yazın.": (
        "Welcome! To start, press “+ Add Person”, or type something like “gave Ahmet 500 TL” into the quick entry box at the top.",
        "أهلاً بك! للبدء اضغط «+ إضافة شخص»، أو اكتب في مربع الإدخال السريع في الأعلى عبارة مثل «أعطيت أحمد 500 ليرة تركية»."),
    "PIN kilidi, tutarları gizleme ve her gün kendiliğinden alınan yedekler. Bu ayarlar yalnız bu telefonda geçerlidir.": (
        "PIN lock, hiding amounts and backups taken automatically every day. These settings apply to this phone only.",
        "قفل PIN وإخفاء المبالغ والنسخ الاحتياطية التي تؤخذ تلقائياً كل يوم. تسري هذه الإعدادات على هذا الهاتف فقط."),
    "Tutarları gizle (ekranda ••••• görünür)": ("Hide amounts (shown as ••••• on screen)", "إخفاء المبالغ (تظهر ••••• على الشاشة)"),
    "Yalnız açılışta kilitle": ("Lock only when the app opens", "القفل عند فتح التطبيق فقط"),
    "1 dakika arka planda kalınca": ("After 1 minute in the background", "بعد دقيقة في الخلفية"),
    "5 dakika arka planda kalınca": ("After 5 minutes in the background", "بعد 5 دقائق في الخلفية"),
    "15 dakika arka planda kalınca": ("After 15 minutes in the background", "بعد 15 دقيقة في الخلفية"),
    "30 dakika arka planda kalınca": ("After 30 minutes in the background", "بعد 30 دقيقة في الخلفية"),
})
