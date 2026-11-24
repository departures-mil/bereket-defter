"""Ana ekrandaki hadislerin İngilizce ve Arapça karşılıkları (v1.21.1).
Arapça: hadisin Buhârî/Müslim'deki asıl metni (Türkçesi kısaltılmışsa aynı yerden kısaltılmış, "…" ile; anlatı olanlarda
rivayetin özeti + Peygamber'in sözü aynen). İngilizce: Türkçe metne sadık çeviri. Anahtar = main.QUOTES'taki Türkçe metin.
Telefon kopyası mobil/js/i18n_mobile.js içinde (test eşitliği denetler)."""

HADIS = {
    "“Alışveriş yapanlar doğru söyler ve kusuru açıklarlarsa alışverişleri bereketli olur; gizler ve yalan söylerlerse alışverişlerinin bereketi kaçar.” (Buhârî, 2079; Müslim, 1532)": (
        "“If the buyer and the seller speak the truth and make things clear, their sale is blessed; if they hide and lie, the blessing of their sale is wiped out.” (Bukhari 2079; Muslim 1532)",
        "«البيّعان بالخيار ما لم يتفرّقا، فإن صدقا وبيّنا بورك لهما في بيعهما، وإن كتما وكذبا مُحقت بركة بيعهما» (البخاري ٢٠٧٩؛ مسلم ١٥٣٢)"),
    "“Satarken, alırken ve alacağını isterken hoşgörülü davranan kişiye Allah rahmet etsin.” (Buhârî, 2076)": (
        "“May Allah have mercy on a man who is easy-going when he sells, when he buys and when he asks for repayment.” (Bukhari 2076)",
        "«رحم الله رجلًا سمحًا إذا باع، وإذا اشترى، وإذا اقتضى» (البخاري ٢٠٧٦)"),
    "“Zenginin borcunu ödemeyi geciktirmesi zulümdür. Sizden birinin alacağı ödeme gücü olan birine havale edilirse, onu kabul etsin.” (Buhârî, 2287; Müslim, 1564)": (
        "“Delay in paying a debt by a rich person is injustice. If the debt of one of you is transferred to a well-off person, let him accept it.” (Bukhari 2287; Muslim 1564)",
        "«مَطْلُ الغنيّ ظلم، فإذا أُتبع أحدكم على مليٍّ فليتبع» (البخاري ٢٢٨٧؛ مسلم ١٥٦٤)"),
    "“Kim insanların malını ödemek niyetiyle alırsa Allah ona ödemeyi kolaylaştırır; kim telef etmek niyetiyle alırsa Allah onu telef eder.” (Buhârî, 2387)": (
        "“Whoever takes people's money intending to repay it, Allah will repay it for him; whoever takes it intending to destroy it, Allah will destroy him.” (Bukhari 2387)",
        "«من أخذ أموال الناس يريد أداءها أدّى الله عنه، ومن أخذ يريد إتلافها أتلفه الله» (البخاري ٢٣٨٧)"),
    "“Sizin en hayırlınız, borcunu en güzel şekilde ödeyeninizdir.” (Buhârî, 2305; Müslim, 1601)": (
        "“The best of you are those who are best in repaying their debts.” (Bukhari 2305; Muslim 1601)",
        "«إنّ خياركم أحسنكم قضاءً» (البخاري ٢٣٠٥؛ مسلم ١٦٠١)"),
    "Bir alacaklı borcunu sert bir dille istedi; sahabe ona yönelince Resûlullah: “Bırakın onu, hak sahibinin söz hakkı vardır” buyurdu ve borcunu daha iyisiyle ödetti. (Buhârî, 2306; Müslim, 1601)": (
        "A creditor demanded his due harshly; when the Companions turned on him, the Messenger of Allah said: “Leave him, for the one who has a right is entitled to speak,” and had him repaid with something better. (Bukhari 2306; Muslim 1601)",
        "أتى رجلٌ النبيَّ ﷺ يتقاضاه فأغلظ له، فهمّ به أصحابه، فقال رسول الله ﷺ: «دعوه، فإنّ لصاحب الحقّ مقالًا»، وأمر أن يُعطى خيرًا من حقّه. (البخاري ٢٣٠٦؛ مسلم ١٦٠١)"),
    "“Bir tüccar insanlara borç verir, darda olanı görünce yardımcılarına ‘Ona göz yumun, umulur ki Allah da bize göz yumar’ derdi. Allah da onu affetti.” (Buhârî, 2078; Müslim, 1562)": (
        "“There was a merchant who used to lend to people; when he saw someone in hardship he would tell his servants: ‘Let him off, perhaps Allah will let us off.’ So Allah let him off.” (Bukhari 2078; Muslim 1562)",
        "«كان تاجرٌ يداين الناس، فإذا رأى معسرًا قال لفتيانه: تجاوزوا عنه لعلّ الله أن يتجاوز عنّا، فتجاوز الله عنه» (البخاري ٢٠٧٨؛ مسلم ١٥٦٢)"),
    "“Kıyamet gününün sıkıntılarından Allah'ın kendisini kurtarmasını isteyen, darda kalan borçluya süre tanısın ya da borcunu bağışlasın.” (Müslim, 1563)": (
        "“Whoever would be pleased for Allah to save him from the distress of the Day of Resurrection, let him give respite to a debtor in hardship or remit his debt.” (Muslim 1563)",
        "«من سرّه أن يُنجيه الله من كُرَب يوم القيامة، فليُنفّس عن معسر أو يضع عنه» (مسلم ١٥٦٣)"),
    "“Kim darda kalan birine kolaylık gösterirse, Allah da ona dünyada ve ahirette kolaylık gösterir.” (Müslim, 2699)": (
        "“Whoever makes things easy for someone in hardship, Allah will make things easy for him in this world and the Hereafter.” (Muslim 2699)",
        "«ومن يسّر على معسر، يسّر الله عليه في الدنيا والآخرة» (مسلم ٢٦٩٩)"),
    "Resûlullah alacaklısına borcunun yarısını bırakmasını işaret etti; o da bıraktı. Sonra borçluya: “Kalk, kalanını öde” buyurdu. (Buhârî, 457; Müslim, 1558)": (
        "The Messenger of Allah signalled to a creditor to forgo half of the debt; he did so. Then he told the debtor: “Get up and pay him the rest.” (Bukhari 457; Muslim 1558)",
        "أشار رسول الله ﷺ إلى كعب بن مالك: «أن ضع الشطر من دينك»، قال: قد فعلت يا رسول الله، قال ﷺ للمدين: «قم فاقضه». (البخاري ٤٥٧؛ مسلم ١٥٥٨)"),
    "Resûlullah namazda “Allah'ım! Günahtan ve borçtan sana sığınırım” diye dua ederdi. Sebebi sorulunca: “Kişi borçlanınca konuşur yalan söyler, söz verir sözünden döner” buyurdu. (Buhârî, 2397; Müslim, 589)": (
        "In his prayer the Messenger of Allah used to say: “O Allah, I seek refuge in You from sin and from debt.” When asked why, he said: “When a man falls into debt, he speaks and lies, and he promises and breaks his promise.” (Bukhari 2397; Muslim 589)",
        "كان رسول الله ﷺ يدعو في الصلاة: «اللهمّ إنّي أعوذ بك من المأثم والمغرم»، فقيل له: ما أكثر ما تستعيذ من المغرم! فقال: «إنّ الرجل إذا غرم حدّث فكذب، ووعد فأخلف». (البخاري ٢٣٩٧؛ مسلم ٥٨٩)"),
    "“Borç hariç, şehidin bütün günahları bağışlanır.” (Müslim, 1886)": (
        "“Every sin of the martyr is forgiven except debt.” (Muslim 1886)",
        "«يُغفر للشهيد كلّ ذنب إلّا الدَّين» (مسلم ١٨٨٦)"),
    "Resûlullah'a borçlu ölen biri getirilince, borcunu ödeyecek bir şey bırakıp bırakmadığını sorardı. Bırakmışsa cenaze namazını kılar, bırakmamışsa “Arkadaşınızın namazını siz kılın” derdi. (Buhârî, 2298; Müslim, 1619)": (
        "When a deceased man who owed a debt was brought to the Messenger of Allah, he would ask whether he had left enough to pay it. If so, he prayed the funeral prayer; if not, he said: “Pray over your companion.” (Bukhari 2298; Muslim 1619)",
        "كان رسول الله ﷺ يُؤتى بالرجل المتوفّى عليه الدَّين فيسأل: «هل ترك لدينه فضلًا؟» فإن حُدِّث أنّه ترك وفاءً صلّى، وإلّا قال: «صلّوا على صاحبكم». (البخاري ٢٢٩٨؛ مسلم ١٦١٩)"),
    "Resûlullah bir Yahudiden veresiye yiyecek satın aldı ve zırhını ona rehin bıraktı. (Buhârî, 2068; Müslim, 1603)": (
        "The Messenger of Allah bought food from a Jew on credit and left his armour with him as a pledge. (Bukhari 2068; Muslim 1603)",
        "اشترى رسول الله ﷺ من يهوديّ طعامًا إلى أجل، ورهنه درعه. (البخاري ٢٠٦٨؛ مسلم ١٦٠٣)"),
    "“Kim selem (peşin ödemeli vadeli alışveriş) yaparsa, belli ölçek, belli tartı ve belli vadeyle yapsın.” (Buhârî, 2240; Müslim, 1604)": (
        "“Whoever pays in advance for something (salam), let him do so for a known measure, a known weight and a known term.” (Bukhari 2240; Muslim 1604)",
        "«من أسلف في شيء، ففي كيلٍ معلوم، ووزنٍ معلوم، إلى أجلٍ معلوم» (البخاري ٢٢٤٠؛ مسلم ١٦٠٤)"),
    "“Kim malını iflas etmiş birinin elinde aynen bulursa, ona herkesten daha çok o hak sahibidir.” (Buhârî, 2402; Müslim, 1559)": (
        "“Whoever finds his very own property with a man who has gone bankrupt has more right to it than anyone else.” (Bukhari 2402; Muslim 1559)",
        "«من أدرك ماله بعينه عند رجل قد أفلس، فهو أحقّ به من غيره» (البخاري ٢٤٠٢؛ مسلم ١٥٥٩)"),
    "“Kimin kardeşine karşı bir hakkı (zulmü) varsa, dinarın ve dirhemin olmayacağı gün gelmeden bugün onunla helalleşsin.” (Buhârî, 2449)": (
        "“Whoever has wronged his brother, let him seek his pardon today, before the day comes when there will be neither dinar nor dirham.” (Bukhari 2449)",
        "«من كانت له مظلمة لأخيه من عِرضه أو شيء فليتحلّله منه اليوم، قبل أن لا يكون دينار ولا درهم» (البخاري ٢٤٤٩)"),
    "“Asıl müflis, kıyamet günü namaz, oruç ve zekâtla gelip de birinin malını yemiş, birine haksızlık etmiş olarak gelen kimsedir; iyilikleri hak sahiplerine verilir.” (Müslim, 2581)": (
        "“The truly bankrupt one is he who comes on the Day of Resurrection with prayer, fasting and zakat, but having consumed this one's wealth and wronged that one; his good deeds are given to those he wronged.” (Muslim 2581)",
        "«إنّ المفلس من أمّتي يأتي يوم القيامة بصلاة وصيام وزكاة، ويأتي قد شتم هذا… وأكل مال هذا… فيُعطى هذا من حسناته، وهذا من حسناته» (مسلم ٢٥٨١)"),
    "“Kim bir Müslümanın malını haksız yere almak için yalan yere yemin ederse, Allah'a, Allah ona gazaplı olarak kavuşur.” (Buhârî, 2356; Müslim, 138)": (
        "“Whoever swears a false oath to unjustly take the property of a Muslim will meet Allah while He is angry with him.” (Bukhari 2356; Muslim 138)",
        "«من حلف على يمين وهو فيها فاجر ليقتطع بها مال امرئ مسلم، لقي الله وهو عليه غضبان» (البخاري ٢٣٥٦؛ مسلم ١٣٨)"),
    "“Ben ancak bir insanım. Bana davalaşarak gelirsiniz; kiminiz delilini diğerinden daha iyi anlatabilir. Kime kardeşinin hakkından bir şey verirsem, ona ateşten bir parça vermiş olurum.” (Buhârî, 2680; Müslim, 1713)": (
        "“I am only a human being. You bring your disputes to me, and some of you may be more eloquent in presenting his case than others. If I give someone something of his brother's right, I am only giving him a piece of the Fire.” (Bukhari 2680; Muslim 1713)",
        "«إنّما أنا بشر، وإنّكم تختصمون إليّ، ولعلّ بعضكم أن يكون ألحن بحجّته من بعض… فمن قطعتُ له من حقّ أخيه شيئًا فلا يأخذه، فإنّما أقطع له به قطعة من النار» (البخاري ٢٦٨٠؛ مسلم ١٧١٣)"),
    "“İnsanlara iddia ettikleri her şey verilseydi, bazıları başkalarının canını ve malını isterdi. Fakat yemin, kendisine iddiada bulunulana düşer.” (Müslim, 1711)": (
        "“If people were given whatever they claimed, some would claim the lives and property of others. But the oath is upon the one against whom the claim is made.” (Muslim 1711)",
        "«لو يُعطى الناس بدعواهم لادّعى ناسٌ دماءَ رجالٍ وأموالَهم، ولكنّ اليمين على المدّعى عليه» (مسلم ١٧١١)"),
    "“Yemin malı sattırır, fakat bereketi yok eder.” (Buhârî, 2087; Müslim, 1606)": (
        "“Swearing (oaths) makes goods sell, but it wipes out the blessing.” (Bukhari 2087; Muslim 1606)",
        "«الحَلِف مَنفقة للسلعة، مَمحقة للبركة» (البخاري ٢٠٨٧؛ مسلم ١٦٠٦)"),
    "“Bizi aldatan bizden değildir.” (Müslim, 101)": (
        "“Whoever cheats us is not one of us.” (Muslim 101)",
        "«من غشّنا فليس منّا» (مسلم ١٠١)"),
    "“Kim bir yiyecek satın alırsa, onu teslim almadan satmasın.” (Buhârî, 2136; Müslim, 1525)": (
        "“Whoever buys food, let him not sell it until he has taken possession of it.” (Bukhari 2136; Muslim 1525)",
        "«من ابتاع طعامًا فلا يبعه حتى يستوفيه» (البخاري ٢١٣٦؛ مسلم ١٥٢٥)"),
    "“Kimse kardeşinin alışverişi üzerine alışveriş yapmasın.” (Buhârî, 2140; Müslim, 1412)": (
        "“Let no one make a sale over the sale of his brother.” (Bukhari 2140; Muslim 1412)",
        "«لا يبيع الرجل على بيع أخيه» (البخاري ٢١٤٠؛ مسلم ١٤١٢)"),
    "“Allah faiz yiyene, yedirene, onu yazana ve iki şahidine lanet etti.” Ve “Onlar (günahta) eşittir” buyurdu. (Müslim, 1598)": (
        "“Allah cursed the one who consumes usury (riba), the one who pays it, the one who records it and its two witnesses.” And he said: “They are all the same.” (Muslim 1598)",
        "لعن رسول الله ﷺ آكلَ الربا، ومُوكِلَه، وكاتبَه، وشاهدَيه، وقال: «هم سواء». (مسلم ١٥٩٨)"),
    "“Altın altınla, gümüş gümüşle, buğday buğdayla... misli misline, eşit olarak ve peşin olarak (değiştirilir).” (Müslim, 1587)": (
        "“Gold for gold, silver for silver, wheat for wheat... like for like, equal for equal, hand to hand.” (Muslim 1587)",
        "«الذهب بالذهب، والفضّة بالفضّة، والبُرّ بالبُرّ… مثلًا بمثل، سواءً بسواء، يدًا بيد» (مسلم ١٥٨٧)"),
    "“Münafığın alameti üçtür: konuşunca yalan söyler, söz verince sözünden döner, kendisine bir şey emanet edilince hıyanet eder.” (Buhârî, 33; Müslim, 59)": (
        "“The signs of a hypocrite are three: when he speaks he lies, when he promises he breaks his promise, and when he is entrusted he betrays the trust.” (Bukhari 33; Muslim 59)",
        "«آية المنافق ثلاث: إذا حدّث كذب، وإذا وعد أخلف، وإذا اؤتمن خان» (البخاري ٣٣؛ مسلم ٥٩)"),
    "“Vasiyet edeceği bir şeyi olan Müslümanın, vasiyeti yanında yazılı olmadan iki gece geçirmesi doğru değildir.” (Buhârî, 2738; Müslim, 1627)": (
        "“It is not right for a Muslim who has something to bequeath to spend two nights without having his will written down with him.” (Bukhari 2738; Muslim 1627)",
        "«ما حقّ امرئ مسلم له شيء يوصي فيه، يبيت ليلتين إلّا ووصيّته مكتوبة عنده» (البخاري ٢٧٣٨؛ مسلم ١٦٢٧)"),
}
