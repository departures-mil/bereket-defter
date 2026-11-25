"""Bereket Alacak-Verecek Defteri — ana program."""
import html
import os
import re
import queue
import random
import sys
from datetime import datetime, timedelta

from PySide6.QtCore import (QByteArray, QDateTime, QFileInfo, QLibraryInfo, QLocale, QPoint, QRectF, QTranslator,
                            QSize, Qt, QTimer, QUrl)
from PySide6.QtGui import (QPalette, QAction, QBrush, QColor, QDesktopServices, QIcon, QImage, QKeySequence,
                           QLinearGradient, QPainter, QPen, QPixmap, QRadialGradient, QTextDocument)
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (QProgressBar, QAbstractItemView, QApplication, QButtonGroup, QCheckBox, QComboBox, QDateTimeEdit,
                               QDialog, QDialogButtonBox, QDoubleSpinBox, QFileDialog, QFileIconProvider, QFormLayout, QFrame,
                               QGridLayout, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QListWidget,
                               QListWidgetItem, QMenu, QMessageBox, QPushButton, QRadioButton, QScrollArea, QSizePolicy, QSystemTrayIcon,
                               QStyle, QStyledItemDelegate, QStyleOptionViewItem, QTableWidget, QTableWidgetItem,
                               QPlainTextEdit, QSpinBox, QTextBrowser, QTextEdit, QVBoxLayout, QWidget)

import i18n
from i18n import _
import fccore
from fccore import style as fcstyle
try:
    import fc_agent  # Asistan Agent (ortak-cekirdek/python/fc_agent.py)
except Exception:  # pragma: no cover
    fc_agent = None
AJAN = None
from db import CHANNELS, CONTACT_FIELDS, CURRENCIES, CURRENCY_NAMES, CURRENCY_SYMBOLS, DB, parse_old
from sync import RULES, SyncEngine
import ekler   # v1.22: güvenlik, raporlar, taksit, mesaj / mutabakat, senet, hızlı kayıt, CSV

APP_TITLE = "Bereket Alacak-Verecek Defteri"
# Sürüm (semver X.Y.Z; etiket vX.Y.Z). Tek kaynak: masaustu/surum.py (CI, kurulum ve telefon aynı sürümü okur)
from surum import APP_VERSION
# Ana ekranda 10 saniyede bir sırayla değişen alacak-verecek, borç ve alışverişle ilgili hadisler (yalnızca Buhârî ve Müslim). Programın içinde durur, internet gerekmez.
QUOTES = [
    "“Alışveriş yapanlar doğru söyler ve kusuru açıklarlarsa alışverişleri bereketli olur; gizler ve yalan söylerlerse alışverişlerinin bereketi kaçar.” (Buhârî, 2079; Müslim, 1532)",
    "“Satarken, alırken ve alacağını isterken hoşgörülü davranan kişiye Allah rahmet etsin.” (Buhârî, 2076)",
    "“Zenginin borcunu ödemeyi geciktirmesi zulümdür. Sizden birinin alacağı ödeme gücü olan birine havale edilirse, onu kabul etsin.” (Buhârî, 2287; Müslim, 1564)",
    "“Kim insanların malını ödemek niyetiyle alırsa Allah ona ödemeyi kolaylaştırır; kim telef etmek niyetiyle alırsa Allah onu telef eder.” (Buhârî, 2387)",
    "“Sizin en hayırlınız, borcunu en güzel şekilde ödeyeninizdir.” (Buhârî, 2305; Müslim, 1601)",
    "Bir alacaklı borcunu sert bir dille istedi; sahabe ona yönelince Resûlullah: “Bırakın onu, hak sahibinin söz hakkı vardır” buyurdu ve borcunu daha iyisiyle ödetti. (Buhârî, 2306; Müslim, 1601)",
    "“Bir tüccar insanlara borç verir, darda olanı görünce yardımcılarına ‘Ona göz yumun, umulur ki Allah da bize göz yumar’ derdi. Allah da onu affetti.” (Buhârî, 2078; Müslim, 1562)",
    "“Kıyamet gününün sıkıntılarından Allah'ın kendisini kurtarmasını isteyen, darda kalan borçluya süre tanısın ya da borcunu bağışlasın.” (Müslim, 1563)",
    "“Kim darda kalan birine kolaylık gösterirse, Allah da ona dünyada ve ahirette kolaylık gösterir.” (Müslim, 2699)",
    "Resûlullah alacaklısına borcunun yarısını bırakmasını işaret etti; o da bıraktı. Sonra borçluya: “Kalk, kalanını öde” buyurdu. (Buhârî, 457; Müslim, 1558)",
    "Resûlullah namazda “Allah'ım! Günahtan ve borçtan sana sığınırım” diye dua ederdi. Sebebi sorulunca: “Kişi borçlanınca konuşur yalan söyler, söz verir sözünden döner” buyurdu. (Buhârî, 2397; Müslim, 589)",
    "“Borç hariç, şehidin bütün günahları bağışlanır.” (Müslim, 1886)",
    "Resûlullah'a borçlu ölen biri getirilince, borcunu ödeyecek bir şey bırakıp bırakmadığını sorardı. Bırakmışsa cenaze namazını kılar, bırakmamışsa “Arkadaşınızın namazını siz kılın” derdi. (Buhârî, 2298; Müslim, 1619)",
    "Resûlullah bir Yahudiden veresiye yiyecek satın aldı ve zırhını ona rehin bıraktı. (Buhârî, 2068; Müslim, 1603)",
    "“Kim selem (peşin ödemeli vadeli alışveriş) yaparsa, belli ölçek, belli tartı ve belli vadeyle yapsın.” (Buhârî, 2240; Müslim, 1604)",
    "“Kim malını iflas etmiş birinin elinde aynen bulursa, ona herkesten daha çok o hak sahibidir.” (Buhârî, 2402; Müslim, 1559)",
    "“Kimin kardeşine karşı bir hakkı (zulmü) varsa, dinarın ve dirhemin olmayacağı gün gelmeden bugün onunla helalleşsin.” (Buhârî, 2449)",
    "“Asıl müflis, kıyamet günü namaz, oruç ve zekâtla gelip de birinin malını yemiş, birine haksızlık etmiş olarak gelen kimsedir; iyilikleri hak sahiplerine verilir.” (Müslim, 2581)",
    "“Kim bir Müslümanın malını haksız yere almak için yalan yere yemin ederse, Allah'a, Allah ona gazaplı olarak kavuşur.” (Buhârî, 2356; Müslim, 138)",
    "“Ben ancak bir insanım. Bana davalaşarak gelirsiniz; kiminiz delilini diğerinden daha iyi anlatabilir. Kime kardeşinin hakkından bir şey verirsem, ona ateşten bir parça vermiş olurum.” (Buhârî, 2680; Müslim, 1713)",
    "“İnsanlara iddia ettikleri her şey verilseydi, bazıları başkalarının canını ve malını isterdi. Fakat yemin, kendisine iddiada bulunulana düşer.” (Müslim, 1711)",
    "“Yemin malı sattırır, fakat bereketi yok eder.” (Buhârî, 2087; Müslim, 1606)",
    "“Bizi aldatan bizden değildir.” (Müslim, 101)",
    "“Kim bir yiyecek satın alırsa, onu teslim almadan satmasın.” (Buhârî, 2136; Müslim, 1525)",
    "“Kimse kardeşinin alışverişi üzerine alışveriş yapmasın.” (Buhârî, 2140; Müslim, 1412)",
    "“Allah faiz yiyene, yedirene, onu yazana ve iki şahidine lanet etti.” Ve “Onlar (günahta) eşittir” buyurdu. (Müslim, 1598)",
    "“Altın altınla, gümüş gümüşle, buğday buğdayla... misli misline, eşit olarak ve peşin olarak (değiştirilir).” (Müslim, 1587)",
    "“Münafığın alameti üçtür: konuşunca yalan söyler, söz verince sözünden döner, kendisine bir şey emanet edilince hıyanet eder.” (Buhârî, 33; Müslim, 59)",
    "“Vasiyet edeceği bir şeyi olan Müslümanın, vasiyeti yanında yazılı olmadan iki gece geçirmesi doğru değildir.” (Buhârî, 2738; Müslim, 1627)",
]
DAY_NAMES = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
GREEN, RED = "#0f8f6a", "#c0392b"          # ekran renkleri: refresh_colors() şemadan alır
PRINT_GREEN, PRINT_RED = "#0f8f6a", "#c0392b"   # döküm (kâğıt / PDF) her zaman açık renk


def tok(name):
    """Seçili renk şemasının (Falcon, Klasik, …) belirteci; ortak çekirdekten."""
    return fcstyle.tok(name)


def refresh_colors():
    global GREEN, RED
    GREEN, RED = tok("ok-text"), tok("danger-text")


def resource(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "assets", name)


def logo_pixmap(size):
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    r = QSvgRenderer(resource("logo.svg"))
    p = QPainter(pm)
    r.render(p, QRectF(0, 0, size, size))
    p.end()
    return pm


def fmt(x):
    """1234567.5 -> 1.234.567,50"""
    s = f"{abs(x):,.2f}"
    if i18n.lang() == "tr":
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if x < 0 else "") + s


def money(x, cur):
    if ekler.GIZLE[0]:   # v1.22: "tutarları gizle" (döküm / senet / mesaj her zaman açık yazar)
        return f"{ekler.MASKE} {CURRENCY_SYMBOLS[cur]}"
    return f"{fmt(x)} {CURRENCY_SYMBOLS[cur]}"


def ts_display(ts):
    try:
        d = datetime.strptime((ts or "")[:16], "%Y-%m-%d %H:%M")
    except ValueError:  # başka cihazdan beklenmeyen biçim gelirse olduğu gibi göster
        return ts or ""
    return d.strftime("%d.%m.%Y %H:%M")


def app_qss():
    """Uygulamaya özgü ek QSS (çekirdeğin Falcon QSS'inin üstüne); renkler seçili şemadan."""
    T = {k: fcstyle.q(v) for k, v in fcstyle.scheme_tokens().items() if str(v).startswith("#") and k.startswith(("accent", "text", "muted", "danger",
                                                                                         "warn", "ok", "panel", "border", "on-", "label", "active"))}
    return """
QLabel#quote {{ color: {muted}; font-style: italic; font-size: 15px; }}
QLabel#clock {{ color: {label}; font-size: 16px; font-weight: 600; }}
QLabel#h2 {{ font-size: 19px; font-weight: 700; color: {accent}; }}
QLabel#muted {{ color: {muted}; }}
QLabel#banner {{ background: {warn-soft}; color: {warn-text}; border: 1px solid {warn-line}; font-size: 16px; font-weight: 700;
                 padding: 10px 16px; border-radius: 12px; }}
QPushButton#danger {{ color: {danger-text}; background: {danger-soft}; border-color: {danger-line}; }}
QPushButton#danger:hover {{ border-color: {danger-text}; }}
QPushButton#gold {{ color: {warn-text}; background: {warn-soft}; border-color: {warn-line}; font-weight: 600; }}
QPushButton#primary {{ color: {on-accent}; background: {accent}; border-color: transparent; font-weight: 600; }}
QListWidget#plist {{ border: 0; background: transparent; }}
QListWidget#plist::item {{ padding: 10px; border-radius: 10px; margin: 2px 0; }}
QListWidget#plist::item:selected {{ background: {active-1}; color: {text}; }}
QFrame#tile {{ background: {panel-hover}; border: 1px solid {border}; border-radius: 14px; }}
QLabel#tileTitle {{ font-weight: 700; color: {accent}; }}
QLabel#hint {{ background: {warn-soft}; color: {warn-text}; padding: 8px; border-radius: 8px; }}
QAbstractSpinBox {{ min-height: 34px; }}
""".format(**T)


def card():
    f = QFrame()
    f.setObjectName("card")
    return f


class BalanceTile(QFrame):
    def __init__(self, cur):
        super().__init__()
        self.cur = cur
        self.setObjectName("tile")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 10, 14, 10)
        t = QLabel(_(CURRENCY_NAMES[cur]))
        t.setObjectName("tileTitle")
        self.main = QLabel()
        self.main.setWordWrap(True)
        self.main.setStyleSheet("font-size:22px;font-weight:700;")
        self.sub = QLabel()
        self.sub.setWordWrap(True)
        self.sub.setObjectName("muted")
        lay.addWidget(t)
        lay.addWidget(self.main)
        lay.addWidget(self.sub)

    def set_person(self, verilen, alinan, bakiye):
        if abs(bakiye) < 0.005:
            self.main.setText(f"{_('Hesap kapalı')}  0 {CURRENCY_SYMBOLS[self.cur]}")
            self.main.setStyleSheet(f"font-size:22px;font-weight:700;color:{tok('muted')};")
        elif bakiye > 0:
            self.main.setText(f"{_('Alacak')}: {money(bakiye, self.cur)}")
            self.main.setStyleSheet(f"font-size:22px;font-weight:700;color:{GREEN};")
        else:
            self.main.setText(f"{_('Verecek')}: {money(-bakiye, self.cur)}")
            self.main.setStyleSheet(f"font-size:22px;font-weight:700;color:{RED};")
        self.sub.setText(f"{_('Verilen')} {money(verilen, self.cur)}  •  {_('Alınan')} {money(alinan, self.cur)}")

    def set_totals(self, alacak, verecek):
        self.main.setText(f"<span style='color:{GREEN}'>{_('Alacak')} {money(alacak, self.cur)}</span>")
        self.main.setStyleSheet("font-size:19px;font-weight:700;")
        self.sub.setText(f"<span style='color:{RED}'>{_('Verecek')} {money(verecek, self.cur)}</span>")



# ---------------------------------------------------------------- iletişim simgeleri
CH_NAMES = {"wa": "WhatsApp", "tg": "Telegram", "sg": "Signal", "call": "Telefonla arama"}
CH_OPEN = {"wa": "WhatsApp'ta mesaj yaz", "tg": "Telegram'da mesaj yaz", "sg": "Signal'de mesaj yaz", "call": "Ara"}
CH_COLORS = {"wa": "#25D366", "tg": "#229ED9", "sg": "#3A76F0", "call": "#0f8f6a"}
_HANDSET = ("M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57"
            ".55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2"
            " 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z")
_PLANE = ("M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3"
          "l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93"
          "c-.23.23-.42.42-.83.42z")
_ch_cache = {}


def _channel_svg(ch, active):
    color = CH_COLORS[ch] if active else "#c3ccc9"
    if ch == "call":
        g = f'<path transform="translate(10.5,10.5) scale(1.12)" d="{_HANDSET}" fill="#fff"/>'
    elif ch == "tg":
        g = f'<path transform="translate(8.5,9.5) scale(1.25)" d="{_PLANE}" fill="#fff"/>'
    elif ch == "wa":
        g = ('<path d="M24 10A14 14 0 0 0 12 31.2L10 38L17 36.1A14 14 0 1 0 24 10z" fill="none" stroke="#fff"'
             ' stroke-width="2.6" stroke-linejoin="round"/>'
             f'<path transform="translate(16.5,16.5) scale(0.62)" d="{_HANDSET}" fill="#fff"/>')
    else:
        g = ('<circle cx="24" cy="24" r="15" fill="none" stroke="#fff" stroke-width="2.4" stroke-dasharray="5 2.6"/>'
             '<path d="M24 14.5A9.5 9.5 0 0 0 15.8 28.8L14.5 34L19.6 32.6A9.5 9.5 0 1 0 24 14.5z" fill="#fff"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
            f'<circle cx="24" cy="24" r="23" fill="{color}"/>{g}</svg>')


def channel_pixmap(ch, size, active=True):
    key = (ch, size, bool(active))
    if key not in _ch_cache:
        img = QImage(size * 2, size * 2, QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.transparent)
        pa = QPainter(img)
        pa.setRenderHint(QPainter.Antialiasing)
        QSvgRenderer(QByteArray(_channel_svg(ch, active).encode())).render(pa)
        pa.end()
        pm = QPixmap.fromImage(img)
        pm.setDevicePixelRatio(2)
        _ch_cache[key] = pm
    return _ch_cache[key]


def kisi_etiketleri(p):
    """v1.22: kişinin etiketleri (virgül / noktalı virgülle ayrılmış)."""
    try:
        raw = p["tags"] or ""
    except (IndexError, KeyError):
        raw = ""
    return [t.strip() for t in re.split(r"[,;،]", raw) if t.strip()]


def active_channels(p):
    return [c for c in CHANNELS if p["ch_" + c]]


def _phone_digits(num):
    num = (num or "").strip()
    digits = "".join(c for c in num if c.isdigit())
    intl = num.startswith("+") or digits.startswith("00")
    if digits.startswith("00"):
        digits = digits[2:]
    return digits, intl


def channel_url(p, ch):
    """(bağlantı, hata mesajı) döndürür."""
    if ch == "tg":
        user = (p["tg_user"] or "").strip().lstrip("@")
        if user and not all(c.isdigit() or c in "+ -()" for c in user):
            return "https://t.me/" + user, None
        num = user or p["phone"] or p["phone2"]
    elif ch == "wa":
        num = p["wa_phone"] or p["phone"] or p["phone2"]
    elif ch == "sg":
        num = p["sg_phone"] or p["phone"] or p["phone2"]
    else:
        num = p["phone"] or p["phone2"]
    digits, intl = _phone_digits(num)
    if not digits:
        return None, _("Bu kişi için numara yazılmamış. Kişi Defteri'nden ekleyin.")
    if ch == "call":
        return "tel:" + ("+" if intl else "") + digits, None
    if not intl:
        return None, _("Numarayı ülke koduyla yazın (ör. +90 5xx..., +963 9xx...).")
    return {"wa": f"https://wa.me/{digits}", "tg": f"https://t.me/+{digits}",
            "sg": f"https://signal.me/#p/+{digits}"}[ch], None


def open_channel(parent, p, ch):
    url, err = channel_url(p, ch)
    if err:
        QMessageBox.information(parent, _(CH_NAMES[ch]), err)
    elif not QDesktopServices.openUrl(QUrl(url)):
        QMessageBox.warning(parent, _(CH_NAMES[ch]), _("Bu bağlantıyı açacak program bulunamadı.") + "\n" + url)


class ChannelBar(QWidget):
    """Kişi adının yanındaki simgeler: kapalıysa tıklayınca açılır, açıksa menüden mesaj/arama veya kapatma."""

    def __init__(self, db, on_change, on_edit):
        super().__init__()
        self.db, self.on_change, self.on_edit, self.pid = db, on_change, on_edit, None
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        self.btns = {}
        for ch in CHANNELS:
            b = QPushButton()
            b.setCursor(Qt.PointingHandCursor)
            b.setIconSize(QSize(32, 32))
            b.setFixedSize(40, 40)
            b.setStyleSheet("QPushButton{background:transparent;border:none;padding:0;border-radius:20px;}"
                            f"QPushButton:hover{{background:{tok('panel-hover')};}}")
            b.clicked.connect(lambda checked=False, c=ch: self.clicked(c))
            lay.addWidget(b)
            self.btns[ch] = b

    def set_person(self, pid):
        self.pid = pid
        self.setVisible(pid is not None)
        if pid is None:
            return
        p = self.db.person(pid)
        for ch, b in self.btns.items():
            on = bool(p["ch_" + ch])
            b.setIcon(QIcon(channel_pixmap(ch, 32, on)))
            b.setToolTip(_(CH_NAMES[ch]) + " — " + (_("açık: tıklayınca açılır") if on
                                                     else _("kapalı: açmak için tıklayın")))

    def clicked(self, ch):
        p = self.db.person(self.pid)
        if not p["ch_" + ch]:
            self.db.set_channel(self.pid, ch, True)
            self.on_change()
            return
        m = QMenu(self)
        a_open = m.addAction(QIcon(channel_pixmap(ch, 20)), _(CH_OPEN[ch]))
        a_off = m.addAction(QIcon(channel_pixmap(ch, 20, False)), _("Bu simgeyi kapat"))
        m.addSeparator()
        a_edit = m.addAction(_("Kişi bilgilerini düzenle…"))
        b = self.btns[ch]
        r = m.exec(b.mapToGlobal(QPoint(0, b.height())))
        if r is a_open:
            open_channel(self, p, ch)
        elif r is a_off:
            self.db.set_channel(self.pid, ch, False)
            self.on_change()
        elif r is a_edit:
            self.on_edit()


class PersonDelegate(QStyledItemDelegate):
    """Kişi listesinde, adın sağına açık olan iletişim simgelerini çizer."""
    ICON = 20

    def paint(self, painter, option, index):
        chs = index.data(Qt.UserRole + 2) or []
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        text = opt.text
        opt.text = ""
        w = opt.widget
        style = w.style() if w else QApplication.style()
        style.drawControl(QStyle.CE_ItemViewItem, opt, painter, w)
        rtl = opt.direction == Qt.RightToLeft
        iw = len(chs) * (self.ICON + 4)
        r = opt.rect.adjusted(12, 0, -12, 0)
        tr = r.adjusted(iw + 6 if rtl else 0, 0, 0 if rtl else -(iw + 6), 0) if chs else r
        painter.save()
        painter.setFont(opt.font)
        selected = bool(opt.state & QStyle.State_Selected)
        painter.setPen(QColor(tok("text")))
        fm = painter.fontMetrics()
        text = text.replace("\u2028", "\n")
        lines = [fm.elidedText(t, Qt.ElideRight, tr.width()) for t in text.split("\n")]
        align = (Qt.AlignRight if rtl else Qt.AlignLeft) | Qt.AlignVCenter | Qt.AlignAbsolute
        painter.drawText(tr, align, "\n".join(lines))
        y = r.top() + (r.height() - self.ICON) // 2
        for i, ch in enumerate(chs):
            x = (r.left() + i * (self.ICON + 4)) if rtl else (r.right() - (len(chs) - i) * (self.ICON + 4) + 4)
            if selected:
                painter.setPen(Qt.NoPen)
                painter.setBrush(fcstyle.qcolor(tok("panel-solid")))
                painter.setRenderHint(QPainter.Antialiasing)
                painter.drawEllipse(x - 2, y - 2, self.ICON + 4, self.ICON + 4)
            painter.drawPixmap(x, y, channel_pixmap(ch, self.ICON))
        painter.restore()


# ---------------------------------------------------------------- diyaloglar
class PersonDialog(QDialog):
    def __init__(self, parent, row=None):
        super().__init__(parent)
        self.setWindowTitle(_("Kişi Düzenle") if row else _("Yeni Kişi"))
        self.setMinimumWidth(520)
        f = QFormLayout(self)

        def val(k):
            return (row[k] or "") if row else ""
        self.name = QLineEdit(val("name"))
        self.phone = QLineEdit(val("phone"))
        self.phone.setPlaceholderText("+90 5xx xxx xx xx")
        self.extra = {}
        for k, label, ph in (("phone2", "2. Telefon", ""), ("wa_phone", "WhatsApp no", "Boşsa Telefon kullanılır"),
                             ("tg_user", "Telegram kullanıcı adı / no", "@kullanici veya +90…"),
                             ("sg_phone", "Signal no", "Boşsa Telefon kullanılır"),
                             ("email", "E-posta", ""), ("address", "Adres", ""),
                             ("tags", "Etiketler", "ör. aile, iş, komşu (virgülle ayırın)")):
            e = QLineEdit(val(k))
            if ph:
                e.setPlaceholderText(_(ph))
            self.extra[k] = (e, label)
        self.note = QTextEdit(val("note"))
        self.note.setFixedHeight(70)
        f.addRow(_("Ad Soyad *"), self.name)
        f.addRow(_("Telefon"), self.phone)
        for k, (e, label) in self.extra.items():
            f.addRow(_(label), e)
        chrow = QGridLayout()
        self.chk = {}
        for i, ch in enumerate(CHANNELS):
            cb = QCheckBox(_(CH_NAMES[ch]) if ch != "call" else _("Arama"))
            cb.setIcon(QIcon(channel_pixmap(ch, 22)))
            cb.setChecked(bool(row["ch_" + ch]) if row else False)
            chrow.addWidget(cb, i // 2, i % 2)
            self.chk[ch] = cb
        f.addRow(_("Ulaşma yolları"), chrow)
        f.addRow(_("Not"), self.note)
        bb = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        bb.button(QDialogButtonBox.Save).setText(_("Kaydet"))
        bb.button(QDialogButtonBox.Cancel).setText(_("Vazgeç"))
        bb.accepted.connect(self.check)
        bb.rejected.connect(self.reject)
        f.addRow(bb)

    def check(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, _("Eksik"), _("Ad Soyad boş olamaz."))
            return
        self.accept()

    def values(self):
        extra = {k: e.text() for k, (e, label) in self.extra.items()}
        extra.update({"ch_" + ch: cb.isChecked() for ch, cb in self.chk.items()})
        return self.name.text(), self.phone.text(), self.note.toPlainText(), extra


class ContactBook(QDialog):
    """Ayrı, tam düzenlenebilir kişi defteri. Hücreye çift tıklayıp düzenlenir, hemen kaydedilir."""
    COLS = [("name", "Ad Soyad"), ("phone", "Telefon"), ("phone2", "2. Telefon"), ("wa_phone", "WhatsApp no"),
            ("tg_user", "Telegram kullanıcı adı / no"), ("sg_phone", "Signal no"), ("email", "E-posta"),
            ("address", "Adres"), ("note", "Not")]

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.changed = False
        self.setWindowTitle(_("Kişi Defteri"))
        self.resize(1250, 680)
        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        h = QLabel(_("Kişi Defteri"))
        h.setObjectName("h2")
        top.addWidget(h)
        top.addSpacing(16)
        self.search = QLineEdit()
        self.search.setPlaceholderText(_("🔍 Kişi ara…"))
        self.search.textChanged.connect(self.load)
        top.addWidget(self.search, 1)
        lay.addLayout(top)
        tip = QLabel(_("Simgelere tıklayarak açıp kapatabilirsiniz. Diğer bilgileri hücreye çift tıklayıp "
                       "düzenleyin; değişiklikler hemen kaydedilir."))
        tip.setObjectName("muted")
        tip.setWordWrap(True)
        lay.addWidget(tip)
        self.table = QTableWidget(0, len(CHANNELS) + len(self.COLS))
        heads = [""] * len(CHANNELS) + [_(t) for k, t in self.COLS]
        self.table.setHorizontalHeaderLabels(heads)
        for i, ch in enumerate(CHANNELS):
            hi = QTableWidgetItem(QIcon(channel_pixmap(ch, 20)), "")
            hi.setToolTip(_(CH_NAMES[ch]))
            self.table.setHorizontalHeaderItem(i, hi)
            self.table.setColumnWidth(i, 46)
        self.table.setIconSize(QSize(26, 26))
        self.table.verticalHeader().setVisible(False)
        self.table.setWordWrap(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed |
                                   QAbstractItemView.AnyKeyPressed)
        hh = self.table.horizontalHeader()
        for i in range(len(CHANNELS)):
            hh.setSectionResizeMode(i, QHeaderView.Fixed)
        for i in range(len(CHANNELS), self.table.columnCount()):
            hh.setSectionResizeMode(i, QHeaderView.Interactive)
        hh.setStretchLastSection(True)
        widths = [200, 170, 170, 170, 240, 170, 190, 200]
        for i, wdt in enumerate(widths):
            self.table.setColumnWidth(len(CHANNELS) + i, wdt)
        self.table.cellClicked.connect(self.cell_clicked)
        self.table.itemChanged.connect(self.item_changed)
        lay.addWidget(self.table, 1)
        bot = QHBoxLayout()
        b_new = QPushButton(_("+ Yeni Kişi"))
        b_new.clicked.connect(self.new_person)
        b_del = QPushButton(_("Sil"))
        b_del.setObjectName("danger")
        b_del.clicked.connect(self.delete_person)
        b_close = QPushButton(_("Kapat"))
        b_close.clicked.connect(self.accept)
        bot.addWidget(b_new)
        bot.addWidget(b_del)
        bot.addStretch(1)
        bot.addWidget(b_close)
        lay.addLayout(bot)
        self.load()

    def load(self, *_a):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for p in self.db.persons(self.search.text()):
            r = self.table.rowCount()
            self.table.insertRow(r)
            for i, ch in enumerate(CHANNELS):
                it = QTableWidgetItem()
                it.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self._set_toggle(it, ch, bool(p["ch_" + ch]))
                it.setData(Qt.UserRole, p["id"])
                self.table.setItem(r, i, it)
            for j, (k, t) in enumerate(self.COLS):
                it = QTableWidgetItem(p[k] or "")
                it.setData(Qt.UserRole, p["id"])
                self.table.setItem(r, len(CHANNELS) + j, it)
            self.table.setRowHeight(r, 38)
        self.table.blockSignals(False)

    @staticmethod
    def _set_toggle(it, ch, on):
        it.setIcon(QIcon(channel_pixmap(ch, 26, on)))
        it.setData(Qt.UserRole + 1, on)
        it.setToolTip(_(CH_NAMES[ch]) + " — " + (_("açık") if on else _("kapalı")) + " (" +
                      _("tıklayınca değişir") + ")")

    def cell_clicked(self, r, c):
        if c >= len(CHANNELS):
            return
        it = self.table.item(r, c)
        ch = CHANNELS[c]
        on = not it.data(Qt.UserRole + 1)
        self.db.set_channel(it.data(Qt.UserRole), ch, on)
        self.table.blockSignals(True)
        self._set_toggle(it, ch, on)
        self.table.blockSignals(False)
        self.changed = True

    def item_changed(self, it):
        c = it.column() - len(CHANNELS)
        if c < 0:
            return
        k = self.COLS[c][0]
        pid = it.data(Qt.UserRole)
        if k == "name" and not it.text().strip():
            QMessageBox.warning(self, _("Eksik"), _("Ad Soyad boş olamaz."))
            self.table.blockSignals(True)
            it.setText(self.db.person(pid)["name"])
            self.table.blockSignals(False)
            return
        self.db.update_contact(pid, {k: it.text()})
        self.changed = True

    def current_pid(self):
        r = self.table.currentRow()
        return self.table.item(r, 0).data(Qt.UserRole) if r >= 0 and self.table.item(r, 0) else None

    def new_person(self):
        d = PersonDialog(self)
        if d.exec():
            self.db.add_person(*d.values())
            self.changed = True
            self.search.clear()
            self.load()

    def delete_person(self):
        pid = self.current_pid()
        if pid is None:
            return
        p = self.db.person(pid)
        n = self.db.tx_count(pid)
        msg = _("'{}' silinsin mi?").format(p['name'])
        if n:
            msg += "\n\n" + _("DİKKAT: Bu kişiye ait {} kayıt ve belgeleri de kalıcı olarak silinecek!").format(n)
        if QMessageBox.warning(self, _("Kişiyi sil"), msg, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.delete_person(pid)
            self.changed = True
            self.load()


class PhotoView(QDialog):
    """Büyük fotoğraf görüntüleyici (yakınlaştırmalı)."""

    def __init__(self, parent, path):
        super().__init__(parent)
        self.setWindowTitle(os.path.basename(path))
        self.resize(1100, 800)
        self.src = QPixmap(path)
        self.zoom = 1.0
        lay = QVBoxLayout(self)
        self.area = QScrollArea()
        self.lbl = QLabel(alignment=Qt.AlignCenter)
        self.area.setWidget(self.lbl)
        self.area.setWidgetResizable(True)
        lay.addWidget(self.area, 1)
        row = QHBoxLayout()
        for text, fn in ((_("Yakınlaştır +"), lambda: self.set_zoom(self.zoom * 1.25)),
                         (_("Uzaklaştır −"), lambda: self.set_zoom(self.zoom / 1.25)),
                         (_("Sığdır"), lambda: self.set_zoom(None)),
                         (_("Harici programda aç"), lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(path)))):
            b = QPushButton(text)
            b.clicked.connect(fn)
            row.addWidget(b)
        lay.addLayout(row)
        QTimer.singleShot(0, lambda: self.set_zoom(None))

    def set_zoom(self, z):
        if self.src.isNull():
            self.lbl.setText(_("Fotoğraf açılamadı."))
            return
        if z is None:
            vs = self.area.viewport().size()
            z = min(vs.width() / self.src.width(), vs.height() / self.src.height(), 1.0)
        self.zoom = z
        self.lbl.setPixmap(self.src.scaled(self.src.size() * z, Qt.KeepAspectRatio, Qt.SmoothTransformation))


def file_thumb(path):
    """Resim, PDF (ilk sayfa) veya dosya türü simgesi."""
    pm = QPixmap(path)
    if not pm.isNull():
        return pm.scaled(240, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    if path.lower().endswith(".pdf"):
        try:
            from PySide6.QtPdf import QPdfDocument
            doc = QPdfDocument()
            doc.load(path)
            if doc.pageCount() > 0:
                sz = doc.pagePointSize(0)
                h = 180
                img = doc.render(0, QSize(max(1, int(sz.width() * h / max(sz.height(), 1))), h))
                doc.close()
                if not img.isNull():
                    return QPixmap.fromImage(img)
        except Exception:
            pass
    return QFileIconProvider().icon(QFileInfo(path)).pixmap(96, 96)


def open_file(parent, path):
    if not QPixmap(path).isNull():
        PhotoView(parent, path).exec()
    elif not QDesktopServices.openUrl(QUrl.fromLocalFile(path)):
        QMessageBox.warning(parent, _("Belge"), _("Bu dosyayı açacak bir program bulunamadı:\n{}").format(path))


class PhotoStrip(QListWidget):
    """Kayda ait belgeler (dekont, PDF, fotoğraf, her türlü dosya). Sürükle-bırak destekler."""

    def __init__(self):
        super().__init__()
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(120, 90))
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setFixedHeight(140)
        self.setStyleSheet(f"QListWidget{{background:{tok('panel-hover')};border-radius:10px;}}")
        self.itemDoubleClicked.connect(lambda it: open_file(self, it.data(Qt.UserRole + 1)))
        self.on_drop = None
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(False)

    def dragEnterEvent(self, e):
        if self.on_drop and e.mimeData().hasUrls():
            e.acceptProposedAction()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, e):
        files = [u.toLocalFile() for u in e.mimeData().urls() if u.isLocalFile()]
        files = [f for f in files if os.path.isfile(f)]
        if self.on_drop and files:
            self.on_drop(files)
            e.acceptProposedAction()

    def add(self, path, key, label=None):
        name = label or os.path.basename(path)
        it = QListWidgetItem(QIcon(file_thumb(path)), name if len(name) <= 18 else name[:15] + "…")
        it.setToolTip(name)
        it.setData(Qt.UserRole, key)
        it.setData(Qt.UserRole + 1, path)
        self.addItem(it)


IMG_FILTER = "Tüm dosyalar (*);;Resimler (*.jpg *.jpeg *.png *.bmp *.webp *.heic *.gif);;PDF (*.pdf)"


class TxDialog(QDialog):
    NEW_PERSON = "__yeni__"

    def __init__(self, parent, db, person_id=None, tx=None):
        super().__init__(parent)
        self.db, self.tx = db, tx
        self.created_pid = None   # "Yeni kişi ekle" ile açılan kişi (kayıttan sonra defteri açılır)
        self.new_photos, self.removed_photos = [], []
        self.setWindowTitle(_("Kaydı Düzenle") if tx else _("Yeni Kayıt"))
        self.setMinimumWidth(620)
        lay = QVBoxLayout(self)
        f = QFormLayout()
        self.person = QComboBox()
        for p in db.persons():
            self.person.addItem(p["name"], p["id"])
        pid = tx["person_id"] if tx else person_id
        if not tx:
            self.person.addItem(_("➕ Yeni kişi ekle"), self.NEW_PERSON)
        if pid is not None:
            self.person.setCurrentIndex(max(0, self.person.findData(pid)))
        f.addRow(_("Kişi"), self.person)
        # yeni kişi: yalnızca ad sorulur
        self.new_name = QLineEdit()
        self.new_name.setPlaceholderText(_("Ad Soyad"))
        self.new_name_lbl = QLabel(_("Yeni kişinin adı *"))
        f.addRow(self.new_name_lbl, self.new_name)
        self.person.currentIndexChanged.connect(self.update_new_person)
        self.update_new_person()

        self.when = QDateTimeEdit(QDateTime.currentDateTime())
        self.when.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.when.setLayoutDirection(Qt.LeftToRight)
        self.when.setCalendarPopup(True)
        if tx:
            self.when.setDateTime(QDateTime.fromString(tx["ts"][:16], "yyyy-MM-dd HH:mm"))
        f.addRow(_("Tarih / Saat"), self.when)

        drow = QHBoxLayout()
        self.r_ver = QRadioButton(_("Verdim (Çıktı)"))
        self.r_al = QRadioButton(_("Aldım (Girdi)"))
        self.r_ver.setStyleSheet(f"color:{RED};font-weight:600;")
        self.r_al.setStyleSheet(f"color:{GREEN};font-weight:600;")
        grp = QButtonGroup(self)
        grp.addButton(self.r_ver)
        grp.addButton(self.r_al)
        (self.r_al if tx and tx["direction"] == "ALDIM" else self.r_ver).setChecked(True)
        drow.addWidget(self.r_ver)
        drow.addWidget(self.r_al)
        f.addRow(_("İşlem"), drow)

        self.cur = QComboBox()
        for c in CURRENCIES:
            self.cur.addItem(_(CURRENCY_NAMES[c]), c)
        if tx:
            self.cur.setCurrentIndex(CURRENCIES.index(tx["currency"]))
        f.addRow(_("Para birimi"), self.cur)

        self.amount = QDoubleSpinBox()
        self.amount.setRange(0, 1e13)
        self.amount.setDecimals(2)
        self.amount.setLocale(QLocale(QLocale.Turkish, QLocale.Turkey) if i18n.lang() == "tr"
                               else QLocale(QLocale.English, QLocale.UnitedStates))
        self.amount.setGroupSeparatorShown(True)
        self.amount.setLayoutDirection(Qt.LeftToRight)
        self.amount.setStyleSheet("font-size:20px;font-weight:700;")
        if tx:
            self.amount.setValue(tx["amount"])
        f.addRow(_("Tutar"), self.amount)

        self.desc = QTextEdit(tx["description"] if tx else "")
        self.desc.setFixedHeight(70)
        f.addRow(_("Açıklama"), self.desc)
        lay.addLayout(f)

        self.hint = QLabel(_("💵 Nakit dolar aldıysanız banknotların fotoğrafını eklemeyi unutmayın "
                             "(sahte çıkma ihtimaline karşı)."))
        self.hint.setWordWrap(True)
        self.hint.setObjectName("hint")
        lay.addWidget(self.hint)
        doc_lbl = QLabel(_("<b>Dekont / Belgeler</b> — PDF, resim veya her türlü dosya. Açmak için çift "
                           "tıklayın, dosyaları buraya sürükleyip bırakabilirsiniz."))
        doc_lbl.setWordWrap(True)
        lay.addWidget(doc_lbl)
        self.strip = PhotoStrip()
        self.strip.on_drop = self.add_files
        lay.addWidget(self.strip)
        prow = QHBoxLayout()
        addp = QPushButton(_("📎 Dekont / belge ekle"))
        addp.clicked.connect(self.add_photos)
        delp = QPushButton(_("Seçili belgeyi kaldır"))
        delp.setObjectName("danger")
        delp.clicked.connect(self.remove_photo)
        prow.addWidget(addp)
        prow.addWidget(delp)
        prow.addStretch()
        lay.addLayout(prow)
        if tx:
            for ph in db.photos(tx["id"]):
                self.strip.add(db.photo_path(ph), ph["id"], ph["original_name"])

        bb = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        bb.button(QDialogButtonBox.Save).setText(_("Kaydet"))
        bb.button(QDialogButtonBox.Cancel).setText(_("Vazgeç"))
        bb.accepted.connect(self.save)
        bb.rejected.connect(self.reject)
        lay.addWidget(bb)
        self.r_al.toggled.connect(self.update_hint)
        self.cur.currentIndexChanged.connect(self.update_hint)
        self.update_hint()

    def update_hint(self):
        self.hint.setVisible(self.r_al.isChecked() and self.cur.currentData() == "USD")

    def is_new_person(self):
        return self.person.currentData() == self.NEW_PERSON

    def update_new_person(self, *_a):
        on = self.is_new_person()
        self.new_name_lbl.setVisible(on)
        self.new_name.setVisible(on)
        if on:
            self.new_name.setFocus()

    def add_photos(self):
        files, _f = QFileDialog.getOpenFileNames(self, _("Dekont / belge seç"), "", _(IMG_FILTER))
        self.add_files(files)

    def add_files(self, files):
        for f in files:
            self.new_photos.append(f)
            self.strip.add(f, None)

    def remove_photo(self):
        it = self.strip.currentItem()
        if not it:
            return
        key, path = it.data(Qt.UserRole), it.data(Qt.UserRole + 1)
        if key is not None:
            self.removed_photos.append(key)
        elif path in self.new_photos:
            self.new_photos.remove(path)
        self.strip.takeItem(self.strip.row(it))

    def save(self):
        creating = self.is_new_person()
        if creating:
            if not self.new_name.text().strip():
                QMessageBox.warning(self, _("Eksik"), _("Ad Soyad boş olamaz."))
                self.new_name.setFocus()
                return
        elif self.person.currentData() is None:
            QMessageBox.warning(self, _("Eksik"), _("Önce bir kişi ekleyin."))
            return
        amt = round(self.amount.value(), 2)
        if amt <= 0:
            QMessageBox.warning(self, _("Eksik"), _("Tutar sıfırdan büyük olmalı."))
            return
        if self.strip.count() == 0 and QMessageBox.question(
                self, _("Belge yok"), _("Bu kayda dekont / belge eklenmedi. Belgesiz kaydedilsin mi?\n\n"
                                        "(Hayır derseniz belge ekleyebilirsiniz.)")) != QMessageBox.Yes:
            return
        pid = self.person.currentData()
        if creating:
            # aynı adda kişi varsa yenisi açılmaz, o kişiye yazılır
            name = self.new_name.text().strip()
            same = [p["id"] for p in self.db.persons() if p["name"].strip().casefold() == name.casefold()]
            pid = same[0] if same else self.db.add_person(name)
            self.created_pid = pid
        args = (pid, self.when.dateTime().toString("yyyy-MM-dd HH:mm"),
                "ALDIM" if self.r_al.isChecked() else "VERDIM", self.cur.currentData(), amt,
                self.desc.toPlainText())
        if self.tx:
            tid = self.tx["id"]
            self.db.update_tx(tid, *args)
        else:
            tid = self.db.add_tx(*args)
        for pid in self.removed_photos:
            self.db.delete_photo(pid)
        for f in self.new_photos:
            try:
                self.db.add_photo(tid, f)
            except OSError as e:
                QMessageBox.warning(self, _("Belge"), _("{} kopyalanamadı: {}").format(f, e))
        self.accept()


class StatementDialog(QDialog):
    """Kişiye ait günlük / saatlik tam döküm."""

    def __init__(self, parent, db, person_id):
        super().__init__(parent)
        self.db, self.pid = db, person_id
        self.person = db.person(person_id) if person_id is not None else None
        self.setWindowTitle(_("Hesap Dökümü"))
        self.resize(1150, 850)
        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        first = db.con.execute("SELECT MIN(ts) FROM transactions" +
                               (" WHERE person_id=?" if person_id is not None else ""),
                               (person_id,) if person_id is not None else ()).fetchone()[0]
        start = QDateTime.fromString(first[:16], "yyyy-MM-dd HH:mm") if first else QDateTime.currentDateTime()
        self.d1 = QDateTimeEdit(QDateTime(start.date(), start.time().fromString("00:00", "HH:mm")))
        self.d2 = QDateTimeEdit(QDateTime(QDateTime.currentDateTime().date(),
                                          QDateTime.currentDateTime().time().fromString("23:59", "HH:mm")))
        for d in (self.d1, self.d2):
            d.setDisplayFormat("dd.MM.yyyy HH:mm")
            d.setLayoutDirection(Qt.LeftToRight)
            d.setCalendarPopup(True)
        self.group = QComboBox()
        self.group.addItem(_("Günlük gruplama"), "day")
        self.group.addItem(_("Saatlik gruplama"), "hour")
        self.cur = QComboBox()
        self.cur.addItem(_("Tüm para birimleri"), None)
        for c in CURRENCIES:
            self.cur.addItem(_(CURRENCY_NAMES[c]), c)
        top.addWidget(QLabel(_("Başlangıç")))
        top.addWidget(self.d1)
        top.addWidget(QLabel(_("Bitiş")))
        top.addWidget(self.d2)
        top.addWidget(self.group)
        top.addWidget(self.cur)
        quick = QComboBox()
        quick.addItems([_("Hızlı seçim…"), _("Bugün"), _("Son 7 gün"), _("Bu ay"), _("Tümü")])
        quick.activated.connect(lambda i: self.quick(i))
        top.addWidget(quick)
        b = QPushButton(_("Göster"))
        b.clicked.connect(self.render)
        top.addWidget(b)
        lay.addLayout(top)
        self.view = QTextBrowser()
        lay.addWidget(self.view, 1)
        row = QHBoxLayout()
        row.addStretch()
        pdf = QPushButton(_("PDF olarak kaydet"))
        pdf.clicked.connect(self.save_pdf)
        pr = QPushButton(_("Yazdır"))
        pr.setObjectName("gold")
        pr.clicked.connect(self.print_)
        row.addWidget(pdf)
        row.addWidget(pr)
        lay.addLayout(row)
        self.render()

    def quick(self, i):
        now = QDateTime.currentDateTime()
        end = QDateTime(now.date(), now.time().fromString("23:59", "HH:mm"))
        if i == 1:
            s = now.date()
        elif i == 2:
            s = now.date().addDays(-6)
        elif i == 3:
            s = now.date().addDays(1 - now.date().day())
        elif i == 4:
            s = now.date().addYears(-50)
        else:
            return
        self.d1.setDateTime(QDateTime(s, now.time().fromString("00:00", "HH:mm")))
        self.d2.setDateTime(end)
        self.render()

    def build_html(self):
        with ekler.gizlemeden():
            return self._build_html()

    def _build_html(self):
        start = self.d1.dateTime().toString("yyyy-MM-dd HH:mm")
        end = self.d2.dateTime().toString("yyyy-MM-dd HH:mm") + ":59"
        cur_filter = self.cur.currentData()
        curs = [cur_filter] if cur_filter else CURRENCIES
        hourly = self.group.currentData() == "hour"
        rows = self.db.transactions(self.pid, start, end, cur_filter)
        opening = {c: v[2] for c, v in self.db.balances(self.pid, start).items()}
        running = dict(opening)
        e = html.escape
        name = e(self.person["name"]) if self.person else _("Tüm kişiler")
        h = [f"""<html><body dir="{'rtl' if i18n.is_rtl() else 'ltr'}" style="font-family:'Segoe UI',Arial;font-size:11pt;color:#223">
<table width="100%"><tr><td><h2 style="color:#06513f;margin:0">{_(APP_TITLE)}</h2>
<span style="font-size:15pt"><b>{_("Hesap Dökümü — {}").format(name)}</b></span><br>
{e(self.d1.dateTime().toString('dd.MM.yyyy HH:mm'))} – {e(self.d2.dateTime().toString('dd.MM.yyyy HH:mm'))}
</td><td align="{'left' if i18n.is_rtl() else 'right'}" style="color:#667">{_("Oluşturulma")}: {datetime.now():%d.%m.%Y %H:%M}<br>
{e(self.person['phone']) if self.person and self.person['phone'] else ''}</td></tr></table><hr>"""]
        h.append(f"<p><b>{_('Devreden bakiye')}:</b> " + " &nbsp;|&nbsp; ".join(self.bal_txt(opening[c], c) for c in curs) + "</p>")
        cols = [_("Saat")] + ([] if self.person else [_("Kişi")]) + [_("İşlem"), _("Birim"), _("Verilen (Çıktı)"),
                                                               _("Alınan (Girdi)"), _("Bakiye"), _("Açıklama"), _("Belge")]
        th = ("<tr style='background:#06513f;color:white'>" + "".join(f"<th>{_(c)}</th>" for c in cols) + "</tr>")
        groups = {}
        for r in rows:
            key = r["ts"][:13] if hourly else r["ts"][:10]
            groups.setdefault(key, []).append(r)
        if not rows:
            h.append(f"<p style='color:#667'>{_('Bu aralıkta kayıt yok.')}</p>")
        for key, items in groups.items():
            d = datetime.strptime(key[:10], "%Y-%m-%d")
            title = f"{d:%d.%m.%Y} {_(DAY_NAMES[d.weekday()])}"
            if hourly:
                title += f" — {_('saat')} {key[11:13]}:00–{key[11:13]}:59"
            h.append(f"<h3 style='color:#0b6e74;margin-bottom:2px'>{title}</h3>")
            h.append("<table width='100%' cellspacing='0' cellpadding='5' border='1' "
                     "style='border-collapse:collapse;border-color:#cfd8d5'>" + th)
            sub = {c: [0.0, 0.0] for c in CURRENCIES}
            for r in items:
                c = r["currency"]
                ver = r["direction"] == "VERDIM"
                running[c] += r["amount"] if ver else -r["amount"]
                sub[c][0 if ver else 1] += r["amount"]
                h.append(
                    f"<tr><td>{r['ts'][11:16]}</td>" +
                    ("" if self.person else f"<td>{e(r['person_name'])}</td>") +
                    f"<td style='color:{PRINT_RED if ver else PRINT_GREEN}'>{_('Verdim') if ver else _('Aldım')}</td><td>{c}</td>"
                    f"<td align=right>{money(r['amount'], c) if ver else ''}</td>"
                    f"<td align=right>{'' if ver else money(r['amount'], c)}</td>"
                    f"<td align=right>{self.bal_txt(running[c], c, short=True)}</td>"
                    f"<td>{e(r['description'] or '')}</td><td align=center>{r['photo_count'] or '—'}</td></tr>")
            h.append("</table>")
            subs = [f"{c}: {_('verilen')} {money(v, c)}, {_('alınan')} {money(a, c)}" for c, (v, a) in sub.items() if v or a]
            h.append(f"<p style='color:#556;margin-top:3px'><i>{_('Saat toplamı') if hourly else _('Gün toplamı')} — "
                     + " | ".join(subs) + "</i></p>")
        tot = {c: [0.0, 0.0] for c in CURRENCIES}
        for r in rows:
            tot[r["currency"]][0 if r["direction"] == "VERDIM" else 1] += r["amount"]
        h.append(f"<hr><h3 style='color:#06513f'>{_('Özet')}</h3><table cellpadding='6' border='1' "
                 "style='border-collapse:collapse;border-color:#cfd8d5'><tr style='background:#06513f;color:white'>" +
                 "".join(f"<th>{_(c)}</th>" for c in (_("Para birimi"), _("Devreden"), _("Verilen"), _("Alınan"),
                                                     _("Kapanış bakiyesi"))) + "</tr>")
        for c in curs:
            h.append(f"<tr><td>{_(CURRENCY_NAMES[c])}</td><td align=right>{self.bal_txt(opening[c], c, True)}</td>"
                     f"<td align=right>{money(tot[c][0], c)}</td><td align=right>{money(tot[c][1], c)}</td>"
                     f"<td align=right><b>{self.bal_txt(running[c], c)}</b></td></tr>")
        h.append("</table><p style='color:#667;font-size:9pt'>" +
                 _("Bakiye: pozitif = alacak (kişi borçlu), negatif = verecek (biz borçluyuz).") + "</p></body></html>")
        return "".join(h)

    @staticmethod
    def bal_txt(b, c, short=False):
        if abs(b) < 0.005:
            return f"0 {CURRENCY_SYMBOLS[c]}"
        col = PRINT_GREEN if b > 0 else PRINT_RED
        label = "" if short else (_("Alacak") if b > 0 else _("Verecek")) + " "
        val = money(b if short else abs(b), c)
        return f"<span style='color:{col}'>{label}{val}</span>"

    def render(self):
        self.view.setHtml(self.build_html())

    def _doc(self):
        doc = QTextDocument()
        doc.setHtml(self.build_html())
        return doc

    def save_pdf(self):
        default = f"dokum_{self.person['name'] if self.person else 'tum'}_{datetime.now():%Y%m%d_%H%M}.pdf"
        path, _f = QFileDialog.getSaveFileName(self, _("PDF kaydet"), default, "PDF (*.pdf)")
        if not path:
            return
        pr = QPrinter(QPrinter.HighResolution)
        pr.setOutputFormat(QPrinter.PdfFormat)
        pr.setOutputFileName(path)
        self._doc().print_(pr)
        QMessageBox.information(self, _("Kaydedildi"), _("Döküm kaydedildi:\n{}").format(path))

    def print_(self):
        pr = QPrinter(QPrinter.HighResolution)
        if QPrintDialog(pr, self).exec() == QDialog.Accepted:
            self._doc().print_(pr)


KIND_TEXT = {"TAHSIL": "Tahsil edilecek (alınacak)", "ODEME": "Ödenecek (verilecek)"}


def reminder_state(r):
    """('done'|'late'|'today'|'soon', metin, renk)"""
    if r["done"]:
        return "done", _("Tamamlandı"), "#556"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if r["due"] <= now:
        return "late", _("Vakti geldi / gecikti"), RED
    if r["due"][:10] == now[:10]:
        return "today", _("Bugün"), tok("warn-text")
    return "soon", _("Yaklaşan"), GREEN


def reminder_text(r):
    amt = money(r["amount"], r["currency"]) if r["amount"] else r["currency"]
    return f"{ts_display(r['due'])} — {r['person_name']}: {_(KIND_TEXT[r['kind']])} {amt}"


class ReminderDialog(QDialog):
    def __init__(self, parent, db, person_id=None, rem=None):
        super().__init__(parent)
        self.db, self.rem = db, rem
        self.setWindowTitle(_("Hatırlatıcıyı Düzenle") if rem else _("Yeni Hatırlatıcı"))
        self.setMinimumWidth(700)
        f = QFormLayout(self)
        self.person = QComboBox()
        for p in db.persons():
            self.person.addItem(p["name"], p["id"])
        pid = rem["person_id"] if rem else person_id
        if pid is not None:
            self.person.setCurrentIndex(max(0, self.person.findData(pid)))
        f.addRow(_("Kişi"), self.person)
        krow = QHBoxLayout()
        self.r_tahsil = QRadioButton(_(KIND_TEXT["TAHSIL"]))
        self.r_odeme = QRadioButton(_(KIND_TEXT["ODEME"]))
        self.r_tahsil.setStyleSheet(f"color:{GREEN};font-weight:600;")
        self.r_odeme.setStyleSheet(f"color:{RED};font-weight:600;")
        grp = QButtonGroup(self)
        grp.addButton(self.r_tahsil)
        grp.addButton(self.r_odeme)
        (self.r_odeme if rem and rem["kind"] == "ODEME" else self.r_tahsil).setChecked(True)
        krow.addWidget(self.r_tahsil)
        krow.addWidget(self.r_odeme)
        f.addRow(_("Tür"), krow)
        self.cur = QComboBox()
        for c in CURRENCIES:
            self.cur.addItem(_(CURRENCY_NAMES[c]), c)
        if rem:
            self.cur.setCurrentIndex(CURRENCIES.index(rem["currency"]))
        f.addRow(_("Para birimi"), self.cur)
        arow = QHBoxLayout()
        self.amount = QDoubleSpinBox()
        self.amount.setRange(0, 1e13)
        self.amount.setDecimals(2)
        self.amount.setLocale(QLocale(QLocale.Turkish, QLocale.Turkey) if i18n.lang() == "tr"
                              else QLocale(QLocale.English, QLocale.UnitedStates))
        self.amount.setGroupSeparatorShown(True)
        self.amount.setLayoutDirection(Qt.LeftToRight)
        self.amount.setSpecialValueText(_("(tutar belirtilmedi)"))
        if rem:
            self.amount.setValue(rem["amount"])
        fill = QPushButton(_("Bakiyeyi kullan"))
        fill.clicked.connect(self.fill_balance)
        arow.addWidget(self.amount, 1)
        arow.addWidget(fill)
        f.addRow(_("Tutar"), arow)
        drow = QHBoxLayout()
        self.due = QDateTimeEdit()
        self.due.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.due.setLayoutDirection(Qt.LeftToRight)
        self.due.setCalendarPopup(True)
        self.due.setMinimumWidth(190)
        if rem:
            self.due.setDateTime(QDateTime.fromString(rem["due"][:16], "yyyy-MM-dd HH:mm"))
        else:
            t = QDateTime.currentDateTime().addDays(1)
            self.due.setDateTime(QDateTime(t.date(), t.time().fromString("10:00", "HH:mm")))
        drow.addWidget(self.due, 1)
        for label, days in ((_("+1 gün"), 1), (_("+1 hafta"), 7), (_("+1 ay"), 30)):
            b = QPushButton(label)
            b.clicked.connect(lambda _c=False, d=days: self.due.setDateTime(self.due.dateTime().addDays(d)))
            drow.addWidget(b)
        f.addRow(_("Hatırlatma zamanı"), drow)
        self.note = QTextEdit(rem["note"] if rem else "")
        self.note.setFixedHeight(70)
        f.addRow(_("Not"), self.note)
        bb = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        bb.button(QDialogButtonBox.Save).setText(_("Kaydet"))
        bb.button(QDialogButtonBox.Cancel).setText(_("Vazgeç"))
        bb.accepted.connect(self.save)
        bb.rejected.connect(self.reject)
        f.addRow(bb)

    def fill_balance(self):
        pid = self.person.currentData()
        if pid is None:
            return
        b = self.db.balances(pid)[self.cur.currentData()][2]
        if b > 0:
            self.r_tahsil.setChecked(True)
        elif b < 0:
            self.r_odeme.setChecked(True)
        self.amount.setValue(abs(b))

    def save(self):
        if self.person.currentData() is None:
            QMessageBox.warning(self, _("Eksik"), _("Önce bir kişi ekleyin."))
            return
        args = (self.person.currentData(), "ODEME" if self.r_odeme.isChecked() else "TAHSIL",
                self.cur.currentData(), round(self.amount.value(), 2),
                self.due.dateTime().toString("yyyy-MM-dd HH:mm"), self.note.toPlainText())
        if self.rem:
            self.db.update_reminder(self.rem["id"], *args)
            if self.rem["due"] != args[4]:
                self.db.set_reminder_done(self.rem["id"], False)
                getattr(self.db, "notified", set()).discard(self.rem["id"])
        else:
            self.db.add_reminder(*args)
        self.accept()


class RemindersDialog(QDialog):
    """Hatırlatıcı listesi. due_only=True: açılışta vadesi gelenleri gösterir."""

    def __init__(self, parent, db, person_id=None, due_only=False):
        super().__init__(parent)
        self.db, self.pid, self.due_only = db, person_id, due_only
        self.changed = False
        self.setWindowTitle(_("🔔 Hatırlatıcılar"))
        self.resize(1050, 560)
        lay = QVBoxLayout(self)
        top = QHBoxLayout()
        self.head = QLabel()
        self.head.setStyleSheet(f"font-size:19px;font-weight:700;color:{tok('accent')};")
        top.addWidget(self.head, 1)
        self.filter = QComboBox()
        self.filter.addItem(_("Vakti gelenler"), "due")
        self.filter.addItem(_("Bekleyenler"), "pending")
        self.filter.addItem(_("Tümü"), "all")
        self.filter.setCurrentIndex(0 if due_only else 1)
        self.filter.currentIndexChanged.connect(self.load)
        top.addWidget(self.filter)
        lay.addLayout(top)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([_("Durum"), _("Hatırlatma zamanı"), _("Kişi"), _("Tür"), _("Tutar"),
                                              _("Not")])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.doubleClicked.connect(lambda *_a: self.edit())
        lay.addWidget(self.table, 1)
        row = QHBoxLayout()
        for text, fn, name in ((_("+ Yeni Hatırlatıcı"), self.add, None), (_("Düzenle"), self.edit, None),
                               (_("✓ Tamamlandı"), self.toggle_done, "gold"),
                               (_("Ertele (+1 gün)"), self.snooze, None), (_("Sil"), self.delete, "danger")):
            b = QPushButton(text)
            if name:
                b.setObjectName(name)
            b.clicked.connect(fn)
            row.addWidget(b)
        row.addStretch()
        close = QPushButton(_("Kapat"))
        close.clicked.connect(self.accept)
        row.addWidget(close)
        lay.addLayout(row)
        self.load()

    def load(self, *_a):
        mode = self.filter.currentData()
        until = datetime.now().strftime("%Y-%m-%d 23:59") if mode == "due" else None
        rows = self.db.reminders(self.pid, pending_only=mode != "all", until=until)
        if mode == "due":
            self.head.setText(_("Bugün ve geçmişte vakti gelen {} hatırlatıcı").format(len(rows)))
        else:
            self.head.setText(_("{} hatırlatıcı").format(len(rows)))
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            _st, label, color = reminder_state(r)
            vals = [label, ts_display(r["due"]), r["person_name"], _(KIND_TEXT[r["kind"]]),
                    money(r["amount"], r["currency"]) if r["amount"] else r["currency"], r["note"] or ""]
            for j, v in enumerate(vals):
                it = QTableWidgetItem(v)
                if j == 0:
                    it.setData(Qt.UserRole, r["id"])
                    it.setForeground(QBrush(QColor(color)))
                    fnt = it.font()
                    fnt.setBold(True)
                    it.setFont(fnt)
                if j == 3:
                    it.setForeground(QBrush(QColor(GREEN if r["kind"] == "TAHSIL" else RED)))
                self.table.setItem(i, j, it)

    def selected(self):
        r = self.table.currentRow()
        if r < 0:
            QMessageBox.information(self, _("Seçim"), _("Önce listeden bir hatırlatıcı seçin."))
            return None
        return self.table.item(r, 0).data(Qt.UserRole)

    def _done(self):
        self.changed = True
        self.load()

    def add(self):
        if not self.db.persons():
            QMessageBox.information(self, _("Kişi yok"), _("Önce soldan bir kişi ekleyin."))
            return
        if ReminderDialog(self, self.db, self.pid).exec():
            self._done()

    def edit(self):
        rid = self.selected()
        if rid and ReminderDialog(self, self.db, rem=self.db.reminder(rid)).exec():
            self._done()

    def toggle_done(self):
        rid = self.selected()
        if rid:
            self.db.set_reminder_done(rid, not self.db.reminder(rid)["done"])
            self._done()

    def snooze(self):
        rid = self.selected()
        if not rid:
            return
        r = self.db.reminder(rid)
        base = max(datetime.strptime(r["due"][:16], "%Y-%m-%d %H:%M"), datetime.now())
        self.db.update_reminder(rid, r["person_id"], r["kind"], r["currency"], r["amount"],
                                (base + timedelta(days=1)).strftime("%Y-%m-%d %H:%M"), r["note"])
        self.db.set_reminder_done(rid, False)
        getattr(self.db, "notified", set()).discard(rid)
        self._done()

    def delete(self):
        rid = self.selected()
        if rid and QMessageBox.question(self, _("Sil"), _("Hatırlatıcı silinsin mi?")) == QMessageBox.Yes:
            self.db.delete_reminder(rid)
            self._done()


# ---------------------------------------------------------------- bulut eşitleme (v1.2)
SYNC_ERRORS = {
    "EMAIL_EXISTS": "Bu e-posta ile zaten bir hesap var. “Giriş yap” düğmesini kullanın.",
    "EMAIL_NOT_FOUND": "E-posta veya şifre yanlış.",
    "INVALID_PASSWORD": "E-posta veya şifre yanlış.",
    "INVALID_LOGIN_CREDENTIALS": "E-posta veya şifre yanlış.",
    "WEAK_PASSWORD": "Şifre çok zayıf; en az 6 karakter olmalı.",
    "INVALID_EMAIL": "E-posta adresi geçersiz.",
    "MISSING_EMAIL": "E-posta adresini yazın.",
    "MISSING_PASSWORD": "Şifreyi yazın.",
    "OPERATION_NOT_ALLOWED": "E-posta/şifre ile giriş bu Firebase projesinde açık değil. Firebase konsolu → "
                             "Authentication → Sign-in method → Email/Password → Enable (Etkinleştir).",
    "CONFIGURATION_NOT_FOUND": "Bu projede Authentication başlatılmamış. Firebase konsolu → Authentication → "
                               "Get started; sonra Email/Password'ü etkinleştirin.",
    "API_KEY_INVALID": "API anahtarı geçersiz. Firebase konsolu → Proje ayarları → Genel → Web API Key "
                       "değerini kopyalayın.",
    "TOO_MANY_ATTEMPTS_TRY_LATER": "Çok fazla deneme yapıldı. Biraz bekleyip tekrar deneyin.",
    "USER_DISABLED": "Bu hesap Firebase'de devre dışı bırakılmış.",
    "NETWORK": "İnternete bağlanılamadı. Kayıtlarınız bu bilgisayarda güvende; bağlantı gelince otomatik "
               "eşitlenecek.",
    "PERMISSION_DENIED": "Firestore kuralları ayarlanmamış (erişim reddedildi). Aşağıdaki kuralları Firestore → "
                         "Rules sekmesine yapıştırıp Publish'e basın.",
    "DB_NOT_FOUND": "Firestore veritabanı oluşturulmamış. Firebase konsolu → Firestore Database → Create "
                    "database. (Proje ID'yi de kontrol edin.)",
    "SESSION_EXPIRED": "Oturumun süresi doldu. Lütfen yeniden giriş yapın.",
    "NOT_CONFIGURED": "Önce Firebase API anahtarını ve Proje ID'yi yazın.",
    "NOT_SIGNED_IN": "Giriş yapılmadı.",
    "SERVER": "Sunucu hatası. Biraz sonra tekrar denenecek.",
    "INTERNAL": "Beklenmeyen bir hata oluştu.",
}
SYNC_HELP = ("<b>Kurulum (Firebase konsolunda bir kez yapılır)</b><ol>"
             "<li><b>console.firebase.google.com</b> adresinde bir proje oluşturun. Proje ayarları → Genel → "
             "<i>Web uygulaması ekle</i> (&lt;/&gt;) deyin; görünen <b>apiKey</b> ve <b>projectId</b> "
             "değerlerini soldaki kutulara yazın.</li>"
             "<li><b>Authentication</b> → Get started → Sign-in method → <b>Email/Password</b> → Enable "
             "(Etkinleştir) → Save.</li>"
             "<li><b>Firestore Database</b> → Create database (veritabanı oluştur). Sonra <b>Rules</b> "
             "sekmesine aşağıdaki kuralları yapıştırıp <b>Publish</b>'e basın.</li></ol>"
             "İlk cihazda <b>Hesap oluştur</b>, diğer cihazlarda (telefon, öbür bilgisayar) aynı e-posta ve "
             "şifreyle <b>Giriş yap</b>. Şifre bu bilgisayara kaydedilmez.")


def sync_error_text(code, detail=""):
    text = SYNC_ERRORS.get(code)
    if text is None:
        return _("Eşitleme hatası") + (f": {code} {detail}".rstrip() if code else "")
    text = _(text)
    if code in ("SERVER", "INTERNAL") and detail:
        text += f" ({detail[:160]})"
    return text


def sync_status_text(engine):
    """(metin, hata mı) — eşitleme düğmesi ve penceresi için."""
    if engine.busy:
        return _("⟳ Eşitleniyor…"), False
    ev = engine.last
    if ev and not ev["ok"]:
        return sync_error_text(ev["code"], ev["detail"]), True
    last = engine.cfg.get("lastSync") or ""
    if last:
        when = last[11:16] if last[:10] == datetime.now().strftime("%Y-%m-%d") else ts_display(last)
        return _("✓ Son eşitleme: {}").format(when), False
    return _("Henüz eşitleme yapılmadı."), False


class SyncDialog(QDialog):
    """☁ Telefon ile eşitleme ayarları (Firebase hesabı)."""

    def __init__(self, parent, engine, lan_only=False):
        super().__init__(parent)
        self.engine = engine
        self.lan_only = lan_only
        self.setWindowTitle(_("📶 Wi‑Fi ile eşitleme (internetsiz)") if lan_only else _("☁ Eşitleme (telefon ⇄ bilgisayar)"))
        self.setMinimumWidth(560 if lan_only else 1000)
        outer = QHBoxLayout(self)
        outer.setSpacing(18)
        left = QVBoxLayout()
        if lan_only:
            self._build_lan(left, engine)
            close = QPushButton(_("Kapat"))
            close.clicked.connect(self.accept)
            left.addWidget(close, 0, Qt.AlignRight if not i18n.is_rtl() else Qt.AlignLeft)
            outer.addLayout(left)
            return
        h = QLabel(_("☁ Telefon ile eşitleme"))
        h.setObjectName("h2")
        left.addWidget(h)
        intro = QLabel(_("Kayıtlar, belgeler ve hatırlatıcılar kendi Firebase hesabınız üzerinden telefon ve "
                         "bilgisayarlar arasında eşitlenir. İnternet yokken program normal çalışır; değişiklikler "
                         "bağlantı gelince gönderilir."))
        intro.setWordWrap(True)
        intro.setObjectName("muted")
        left.addWidget(intro)
        cfg = engine.cfg
        f = QFormLayout()
        self.api = QLineEdit(cfg.get("apiKey", ""))
        self.api.setPlaceholderText("AIza…")
        self.proj = QLineEdit(cfg.get("projectId", ""))
        self.proj.setPlaceholderText("bereket-defter")
        self.email = QLineEdit(cfg.get("email", ""))
        self.email.setPlaceholderText("ornek@gmail.com")
        self.pw = QLineEdit()
        self.pw.setEchoMode(QLineEdit.Password)
        self.pw.returnPressed.connect(self.sign_in)
        self.emu = QLineEdit(cfg.get("emulator", ""))
        self.emu.setPlaceholderText("127.0.0.1")
        for e in (self.api, self.proj, self.email, self.pw, self.emu):
            e.setLayoutDirection(Qt.LeftToRight)
            e.setMinimumHeight(34)
        f.addRow(_("Firebase API key"), self.api)
        f.addRow(_("Proje ID"), self.proj)
        f.addRow(_("E-posta"), self.email)
        f.addRow(_("Şifre"), self.pw)
        self.adv = QPushButton()
        self.adv.setFlat(True)
        self.adv.setCursor(Qt.PointingHandCursor)
        self.adv.setStyleSheet(f"QPushButton{{background:transparent;border:0;color:{tok('accent')};padding:2px;text-align:left;}}")
        self.adv.clicked.connect(lambda: self.show_advanced(not self.emu.isVisible()))
        f.addRow("", self.adv)
        self.emu_lbl = QLabel(_("Emülatör adresi (yalnızca test)"))
        f.addRow(self.emu_lbl, self.emu)
        left.addLayout(f)
        self.account = QLabel()
        self.account.setStyleSheet(f"font-weight:700;color:{tok('accent')};")
        left.addWidget(self.account)
        self.status = QLabel()
        self.status.setWordWrap(True)
        self.status.setMinimumHeight(48)
        for lbl in (intro, self.status):  # uzun / sağdan sola metin taşmasın
            lbl.setMinimumWidth(200)
            lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        left.addWidget(self.status)
        brow = QGridLayout()
        self.b_in = QPushButton(_("Giriş yap"))
        self.b_in.clicked.connect(self.sign_in)
        self.b_up = QPushButton(_("Hesap oluştur"))
        self.b_up.clicked.connect(self.sign_up)
        self.b_out = QPushButton(_("Çıkış yap"))
        self.b_out.setObjectName("danger")
        self.b_out.clicked.connect(self.sign_out)
        self.b_now = QPushButton(_("☁ Şimdi eşitle"))
        self.b_now.setObjectName("gold")
        self.b_now.clicked.connect(self.sync_now)
        brow.addWidget(self.b_in, 0, 0)
        brow.addWidget(self.b_up, 0, 1)
        brow.addWidget(self.b_now, 1, 0)
        brow.addWidget(self.b_out, 1, 1)
        left.addLayout(brow)
        self._build_lan(left, engine)
        left.addStretch(1)
        close = QPushButton(_("Kapat"))
        close.clicked.connect(self.accept)
        crow = QHBoxLayout()
        crow.addStretch(1)
        crow.addWidget(close)
        left.addLayout(crow)
        outer.addLayout(left, 4)

        helpbox = QFrame()
        helpbox.setProperty("fc", "card")
        right = QVBoxLayout(helpbox)
        right.setContentsMargins(14, 12, 14, 12)
        ht = QLabel(_(SYNC_HELP))
        ht.setWordWrap(True)
        ht.setTextFormat(Qt.RichText)
        right.addWidget(ht)
        right.addWidget(QLabel("<b>" + _("Firestore kuralları (Rules):") + "</b>"))
        self.rules = QPlainTextEdit(RULES)
        self.rules.setReadOnly(True)
        self.rules.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.rules.setLayoutDirection(Qt.LeftToRight)
        self.rules.setStyleSheet("font-family:Consolas,'Courier New',monospace;font-size:12px;")
        self.rules.setFixedHeight(180)
        right.addWidget(self.rules)
        cp = QPushButton(_("Kuralları kopyala"))
        cp.clicked.connect(lambda: (QApplication.clipboard().setText(RULES), cp.setText(_("Kopyalandı ✓"))))
        right.addWidget(cp, 0, Qt.AlignLeft if not i18n.is_rtl() else Qt.AlignRight)
        right.addStretch(1)
        outer.addWidget(helpbox, 6)
        self.show_advanced(bool(cfg.get("emulator")))
        self.refresh()
        self.resize(1100, max(700, self.sizeHint().height()))

    def _build_lan(self, left, engine):
        """Wi‑Fi (internetsiz) eşitleme: ikinci seçenek (üst çubuktaki Wi‑Fi düğmesi yalnız bunu açar)."""
        lan = getattr(engine, "lan_server", None)
        if lan is not None:
            wbox = QFrame()
            wbox.setProperty("fc", "card")
            wl = QVBoxLayout(wbox)
            wl.setContentsMargins(12, 10, 12, 10)
            wh = QLabel("<b>" + _("📶 Wi‑Fi ile eşitleme (internetsiz)") + "</b>")
            wl.addWidget(wh)
            wi = QLabel(_("Telefon ve bu bilgisayar aynı modeme / Wi‑Fi ağına bağlıyken internet olmadan da eşitlenir. "
                          "Telefonda: ☁ Eşitleme → 📶 Wi‑Fi ile eşitle → aşağıdaki adresi ve kodu yazın. "
                          "Aynı bulut hesabındaysanız kod sorulmaz. Kayıtlar silinmez, üst üste yazılmaz; son değişen kazanır."))
            wi.setWordWrap(True)
            wi.setObjectName("muted")
            wi.setMinimumWidth(200)
            wi.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
            wl.addWidget(wi)
            self.lan_info = QLabel()
            self.lan_info.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.lan_info.setLayoutDirection(Qt.LeftToRight)
            self.lan_info.setStyleSheet(f"font-size:17px;font-weight:700;color:{tok('accent')};")
            wl.addWidget(self.lan_info)
            self.lan_last = QLabel()
            self.lan_last.setObjectName("muted")
            wl.addWidget(self.lan_last)
            nb = QPushButton(_("Yeni kod üret"))
            nb.clicked.connect(lambda: (lan.new_code(), self.refresh_lan()))
            wl.addWidget(nb, 0, Qt.AlignLeft if not i18n.is_rtl() else Qt.AlignRight)
            left.addWidget(wbox)
            self.refresh_lan()

    def refresh_lan(self):
        lan = getattr(self.engine, "lan_server", None)
        if lan is None or not hasattr(self, "lan_info"):
            return
        import lan as lanmod
        if not lan.running:
            self.lan_info.setText(_("Wi‑Fi eşitleme başlatılamadı: {}").format(lan.error or "—"))
            return
        ips = lanmod.local_ips() or ["?"]
        self.lan_info.setText(_("Adres") + ": " + "  /  ".join(f"{ip}:{lanmod.PORT}" for ip in ips) + "\n" +
                              _("Kod") + ": " + lan.code())
        last = lan.last
        self.lan_last.setText(_("Son Wi‑Fi eşitleme: {} · gelen {} · giden {}").format(
            last.get("name") or _("telefon"), last.get("got", 0), last.get("sent", 0)) if last else "")

    def show_advanced(self, on):
        self.emu.setVisible(on)
        self.emu_lbl.setVisible(on)
        self.adv.setText(("▾ " if on else ("◂ " if i18n.is_rtl() else "▸ ")) + _("Gelişmiş"))

    def refresh(self):
        if self.lan_only:
            return
        eng = self.engine
        signed, busy = eng.signed_in(), eng.busy
        self.account.setText(_("Giriş yapıldı: {}").format(eng.cfg.get("email", "")) if signed
                             else _("Giriş yapılmadı"))
        for e in (self.api, self.proj, self.email, self.pw, self.emu):
            e.setEnabled(not signed and not busy)
        self.b_in.setEnabled(not signed and not busy)
        self.b_up.setEnabled(not signed and not busy)
        self.b_out.setEnabled(signed and not busy)
        self.b_now.setEnabled(signed and not busy)
        text, err = sync_status_text(eng)
        if not signed and not busy and not err:
            text = ""
        self.status.setText(text)
        self.status.setStyleSheet(f"color:{RED if err else GREEN};font-weight:600;")

    def on_event(self, ev):
        if ev.get("type") == "done" and ev.get("ok") and ev.get("op") in ("signin", "signup"):
            self.pw.clear()
        self.refresh()
        if ev.get("op") == "lan":
            self.refresh_lan()

    def _start(self, op):
        api, proj = self.api.text().strip(), self.proj.text().strip()
        if not api or not proj:
            self.status.setText(sync_error_text("NOT_CONFIGURED"))
            self.status.setStyleSheet(f"color:{RED};font-weight:600;")
            return
        self.engine.request(op, email=self.email.text().strip(), password=self.pw.text(), api_key=api,
                            project_id=proj, emulator=self.emu.text().strip() if self.emu.isVisible() else "")
        self.engine.busy = True  # olay gelene kadar düğmeler kapalı kalsın
        self.refresh()

    def sign_in(self):
        self._start("signin")

    def sign_up(self):
        self._start("signup")

    def sign_out(self):
        if QMessageBox.question(self, _("Çıkış yap"), _("Eşitleme hesabından çıkılsın mı?\nBu bilgisayardaki "
                                                         "kayıtlar silinmez; yalnızca eşitleme durur.")) \
                == QMessageBox.Yes:
            self.engine.request("signout")
            self.engine.busy = True
            self.refresh()

    def sync_now(self):
        self.engine.request("sync")
        self.engine.busy = True
        self.refresh()


# ---------------------------------------------------------------- ana pencere
class MainWindow(QWidget):
    """Defter sayfası (ortak çekirdek kabuğunun içinde). Dil ya da renk şeması değişince yeniden kurulur;
    eşitleme motoru, Wi‑Fi sunucusu ve bildirilen hatırlatıcılar db nesnesinde kalır."""
    ALL = -1

    def __init__(self, db, first_start=True, shell=None):
        super().__init__()
        self.db = db
        self.shell = shell
        refresh_colors()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.bg = QWidget()
        outer.addWidget(self.bg)
        root = QVBoxLayout(self.bg)
        root.setContentsMargins(24, 16, 24, 20)
        root.setSpacing(14)

        # --- üst satır: hadis + saat + günlük işler (pencere/eşitleme/güncelleme düğmeleri ortak üst çubukta)
        head = QHBoxLayout()
        head.setSpacing(12)
        self.quote_i = random.randrange(len(QUOTES))
        self.quote = QLabel(_(QUOTES[self.quote_i]))
        self.quote.setObjectName("quote")
        self.quote.setWordWrap(True)
        self.quote.setMinimumWidth(200)
        self.quote.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        head.addWidget(self.quote, 1)
        self.clock = QLabel()
        self.clock.setObjectName("clock")
        self.clock.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        head.addWidget(self.clock)
        self.goz = QPushButton("🙈" if ekler.GIZLE[0] else "👁")
        self.goz.setObjectName("light")
        self.goz.setToolTip(_("Tutarları gizle / göster (Ctrl+H)"))
        self.goz.clicked.connect(lambda: self.gizle_degistir(not ekler.GIZLE[0]))
        head.addWidget(self.goz)
        self.rem_btn = QPushButton()
        self.rem_btn.setObjectName("light")
        self.rem_btn.clicked.connect(lambda: self.open_reminders())
        head.addWidget(self.rem_btn)
        for text, fn in ((_("Tüm Kayıtlar Dökümü"), lambda: StatementDialog(self, self.db, None).exec()),
                         (_("Yedek Al"), self.backup)):
            b = QPushButton(text)
            b.setObjectName("light")
            b.clicked.connect(fn)
            head.addWidget(b)
        root.addLayout(head)
        hrow = QHBoxLayout()   # v1.22: hızlı kayıt (internetsiz ayrıştırıcı)
        self.hizli = QLineEdit()
        self.hizli.setPlaceholderText(_("✦ Hızlı kayıt: ör. Ahmet'e 500 TL verdim"))
        self.hizli.setToolTip(_("Cümleyi yazıp Enter'a basın; kişi, tutar, para birimi ve işlem kendiliğinden doldurulur (Ctrl+K)."))
        self.hizli.returnPressed.connect(lambda: self.hizli_kayit(self.hizli.text()))
        hrow.addWidget(self.hizli, 1)
        hb = QPushButton(_("✦ Hızlı kayıt"))
        hb.setObjectName("primary")
        hb.clicked.connect(lambda: self.hizli_kayit(self.hizli.text()))
        hrow.addWidget(hb)
        root.addLayout(hrow)
        self.banner = QLabel()
        self.banner.setWordWrap(True)
        self.banner.setObjectName("banner")
        self.banner.setCursor(Qt.PointingHandCursor)
        self.banner.mousePressEvent = lambda e: (self.banner.hide(), self.open_reminders())
        self.banner.hide()
        root.addWidget(self.banner)

        # --- genel özet
        summ = card()
        sl = QHBoxLayout(summ)
        sl.setContentsMargins(16, 12, 16, 12)
        cap = QLabel(_("Genel\nDurum"))
        cap.setObjectName("h2")
        sl.addWidget(cap)
        self.total_tiles = {c: BalanceTile(c) for c in CURRENCIES}
        for c in CURRENCIES:
            sl.addWidget(self.total_tiles[c], 1)
        root.addWidget(summ)

        body = QHBoxLayout()
        body.setSpacing(14)
        # --- kişiler
        left = card()
        left.setFixedWidth(320)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(14, 14, 14, 14)
        h = QLabel(_("Kişiler"))
        h.setObjectName("h2")
        ll.addWidget(h)
        self.search = QLineEdit()
        self.search.setPlaceholderText(_("🔍 Kişi ara…"))
        self.search.textChanged.connect(self.load_persons)
        ll.addWidget(self.search)
        self.f_tag = QComboBox()   # v1.22: etiket / grup süzgeci
        self.f_tag.currentIndexChanged.connect(self.load_persons)
        ll.addWidget(self.f_tag)
        self.fill_tags()
        self.plist = QListWidget()
        self.plist.setObjectName("plist")
        self.plist.setItemDelegate(PersonDelegate(self.plist))
        self.plist.currentItemChanged.connect(lambda *_a: self.load_person())
        self.plist.itemDoubleClicked.connect(lambda *_a: self.edit_person())
        ll.addWidget(self.plist, 1)
        pb = QGridLayout()
        b_add = QPushButton(_("+ Kişi Ekle"))
        b_add.clicked.connect(self.add_person)
        b_edit = QPushButton(_("Düzenle"))
        b_edit.clicked.connect(self.edit_person)
        b_del = QPushButton(_("Sil"))
        b_del.setObjectName("danger")
        b_del.clicked.connect(self.delete_person)
        b_book = QPushButton(_("📒 Kişi Defteri"))
        b_book.clicked.connect(self.open_book)
        pb.addWidget(b_add, 0, 0)
        pb.addWidget(b_book, 0, 1)
        pb.addWidget(b_edit, 1, 0)
        pb.addWidget(b_del, 1, 1)
        ll.addLayout(pb)
        body.addWidget(left)

        # --- kayıtlar
        right = card()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(16, 14, 16, 14)
        self.pname = QLabel()
        self.pname.setObjectName("h2")
        self.pinfo = QLabel()
        self.pinfo.setWordWrap(True)
        self.pinfo.setObjectName("muted")
        self.chbar = ChannelBar(self.db, self.load_persons, self.edit_person)
        nrow = QHBoxLayout()
        nrow.addWidget(self.pname)
        nrow.addSpacing(14)
        nrow.addWidget(self.chbar)
        nrow.addStretch(1)
        rl.addLayout(nrow)
        rl.addWidget(self.pinfo)
        tiles = QHBoxLayout()
        self.tiles = {c: BalanceTile(c) for c in CURRENCIES}
        for c in CURRENCIES:
            tiles.addWidget(self.tiles[c], 1)
        rl.addLayout(tiles)
        fl = QHBoxLayout()
        self.f_cur = QComboBox()
        self.f_cur.addItem(_("Tüm para birimleri"), None)
        for c in CURRENCIES:
            self.f_cur.addItem(_(CURRENCY_NAMES[c]), c)
        self.f_cur.currentIndexChanged.connect(self.load_tx)
        self.f_text = QLineEdit()
        self.f_text.setPlaceholderText(_("Açıklamada ara…"))
        self.f_text.textChanged.connect(self.load_tx)
        self.f_nodoc = QCheckBox(_("Sadece belgesiz kayıtlar"))
        self.f_nodoc.toggled.connect(self.load_tx)
        fl.addWidget(self.f_cur)
        fl.addWidget(self.f_text, 1)
        fl.addWidget(self.f_nodoc)
        rl.addLayout(fl)
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([_("Tarih / Saat"), _("Kişi"), _("İşlem"), _("Birim"), _("Verilen (Çıktı)"),
                                              _("Alınan (Girdi)"), _("Açıklama"), "📎"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(6, QHeaderView.Stretch)
        self.table.doubleClicked.connect(lambda *_a: self.edit_tx())
        rl.addWidget(self.table, 1)
        self.empty = QLabel()   # v1.22: boş durum yönlendirmesi
        self.empty.setObjectName("muted")
        self.empty.setAlignment(Qt.AlignCenter)
        self.empty.setWordWrap(True)
        self.empty.setStyleSheet("font-size:16px;padding:30px;")
        self.empty.hide()
        rl.addWidget(self.empty, 1)
        tb = QGridLayout()
        tb.setHorizontalSpacing(8)
        tb.setVerticalSpacing(6)
        acts = ((_("+ Verdim (Çıktı)"), lambda: self.add_tx("VERDIM"), "danger"),
                (_("+ Aldım (Girdi)"), lambda: self.add_tx("ALDIM"), None),
                (_("Düzenle"), self.edit_tx, None),
                (_("Sil"), self.delete_tx, "danger"),
                (_("📎 Belgeler"), self.show_photos, None),
                (_("Değişiklik Geçmişi"), self.show_history, None),
                (_("🔔 Hatırlatıcı Ekle"), self.add_reminder, None),
                (_("📄 Döküm Al"), self.statement, "gold"),
                (_("💬 Mesaj / Mutabakat"), self.mesaj, None),
                (_("📅 Taksit Planı"), self.taksit, None),
                (_("📜 Borç Senedi"), self.senet, None))
        self.kisi_btn = []
        for i, (text, fn, name) in enumerate(acts):
            b = QPushButton(text)
            if name:
                b.setObjectName(name)
            b.clicked.connect(fn)
            tb.addWidget(b, i // 6, i % 6)
            if fn in (self.mesaj, self.taksit):
                self.kisi_btn.append(b)
        rl.addLayout(tb)
        self.geri_al = ekler.GeriAlCubugu(self, self.db, self.load_persons)
        rl.addWidget(self.geri_al)
        body.addWidget(right, 1)
        root.addLayout(body, 1)

        g = getattr(self.db, "guvenlik", None)
        for seq, fn in (("Ctrl+N", lambda: self.add_tx("VERDIM")), ("Ctrl+Shift+N", lambda: self.add_tx("ALDIM")),
                        ("Ctrl+K", lambda: self.hizli_kayit("")), ("Ctrl+F", lambda: (self.search.setFocus(), self.search.selectAll())),
                        ("Ctrl+P", self.statement), ("Ctrl+M", self.mesaj),
                        ("Ctrl+R", lambda: self.shell is not None and self.shell.show_page("rapor")),
                        ("Ctrl+H", lambda: self.gizle_degistir(not ekler.GIZLE[0])),
                        ("Ctrl+L", lambda: g is not None and g.kilitle()),
                        ("F5", self.sync_button_clicked), ("Delete", self.delete_tx)):
            a = QAction(self)
            a.setShortcut(QKeySequence(seq))
            a.setShortcutContext(Qt.WindowShortcut)
            a.triggered.connect(fn)
            self.addAction(a)

        self.timer = QTimer(self, interval=1000, timeout=self.tick)
        self.timer.start()
        self.qtimer = QTimer(self, interval=10000, timeout=self.next_quote)
        self.qtimer.start()
        self.tick()
        self.load_persons()
        self.setup_sync()

        # hatırlatıcı bildirimleri
        if not hasattr(db, "notified"):
            db.notified = set()
        self.tray = QSystemTrayIcon(QIcon(logo_pixmap(64)), self)
        self.tray.setToolTip(_(APP_TITLE))
        self.tray.activated.connect(lambda *_a: self.open_reminders())
        self.tray_target = "reminder"
        self.tray.messageClicked.connect(lambda: self.open_reminders())
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray.show()
        self.rtimer = QTimer(self, interval=30000, timeout=self.check_reminders)
        self.rtimer.start()
        if first_start:
            QTimer.singleShot(700, self.startup_reminders)
        else:
            self.check_reminders(notify=False)

    # --- bulut eşitleme
    def setup_sync(self):
        if not hasattr(self.db, "sync_engine"):  # dil değişince pencere yeniden kurulur; motor aynı kalır
            self.db.sync_engine = SyncEngine(self.db.dir, self.db.path)
        self.sync = self.db.sync_engine
        if not hasattr(self.sync, "lan_server"):  # Wi‑Fi (internetsiz) eşitleme sunucusu, program açıkken
            import lan as lanmod
            self.sync.lan_server = lanmod.LanServer(self.sync, APP_VERSION)
            self.sync.lan_server.start()
        self.sync_dlg = None
        self.sync_wanted = False
        self.sync_refresh_pending = False
        self.sync_debounce = QTimer(self, singleShot=True, interval=3000, timeout=self.request_sync)
        self.db.on_change = self.sync_debounce.start
        self.sync_poll = QTimer(self, interval=250, timeout=self.poll_sync)
        self.sync_poll.start()
        self.sync_periodic = QTimer(self, interval=60000, timeout=self.request_sync)
        self.sync_periodic.start()
        self.update_sync_indicator()
        if self.sync.signed_in():
            QTimer.singleShot(1500, self.request_sync)

    def request_sync(self):
        if not self.sync.signed_in():
            return
        modal = QApplication.activeModalWidget()
        if modal is not None and modal is not self.sync_dlg:
            self.sync_wanted = True  # açık bir pencere varken veriyi değiştirme; kapanınca eşitle
            return
        self.sync_wanted = False
        self.sync.request("sync")

    def poll_sync(self):
        got = False
        while True:
            try:
                ev = self.sync.events.get_nowait()
            except queue.Empty:
                break
            got = True
            if ev.get("type") == "done" and ev.get("changed"):
                self.sync_refresh_pending = True
            if self.sync_dlg is not None:
                self.sync_dlg.on_event(ev)
        if got:
            self.update_sync_indicator()
        modal = QApplication.activeModalWidget()
        if modal is None or modal is self.sync_dlg:
            if self.sync_refresh_pending:
                self.refresh_after_sync()
            if self.sync_wanted:
                self.request_sync()

    def refresh_after_sync(self):
        """Gelen değişikliklerden sonra listeleri yenile; seçili kişi ve kayıt korunur."""
        self.sync_refresh_pending = False
        r = self.table.currentRow()
        tid = self.table.item(r, 0).data(Qt.UserRole) if r >= 0 and self.table.item(r, 0) else None
        scroll = self.table.verticalScrollBar().value()
        self.load_persons()
        for i in range(self.table.rowCount()):
            if tid is not None and self.table.item(i, 0).data(Qt.UserRole) == tid:
                self.table.setCurrentCell(i, 0)  # selectRow sağdan sola düzende seçimi bırakıyor
                break
        self.table.verticalScrollBar().setValue(scroll)
        self.update_reminder_button()

    def sync_button_clicked(self):
        """Giriş yapılmışsa hemen eşitler; yapılmamışsa ☁ Eşitleme penceresini açar."""
        if not self.sync.signed_in():
            self.open_sync()
            return
        if not self.sync.busy:
            self.sync_wanted = False
            self.sync.request("sync")
        self.update_sync_indicator()

    def update_sync_indicator(self):
        """Ortak üst çubuktaki Eşitle düğmesi: durum + bekleyen değişiklik sayısı; Wi‑Fi düğmesi: sunucu açık mı."""
        s = self.sync
        tb = getattr(self.shell, "tb", None) if self.shell is not None else None
        if tb is None:
            return
        if not s.signed_in():
            st = "off"
        elif s.busy:
            st = "syncing"
        else:
            _text, err = sync_status_text(s)
            st = "error" if err else "idle"
        try:
            pend = self.db.pending_changes() if s.signed_in() else 0
        except Exception:
            pend = 0
        tb.set_sync(st, pend)
        lan = getattr(s, "lan_server", None)
        tb.set_lan("on" if lan is not None and lan.running else "off")
        if s.signed_in() and s.cfg.get("projectId"):
            from fccore import usage
            usage.set_project(s.cfg.get("projectId"))

    def open_sync(self, lan_only=False):
        self.sync_dlg = SyncDialog(self, self.sync, lan_only=lan_only)
        try:
            self.sync_dlg.exec()
        finally:
            self.sync_dlg = None
        self.update_sync_indicator()

    # --- yardımcılar
    def next_quote(self):
        self.quote_i = (self.quote_i + 1) % len(QUOTES)
        self.quote.setText(_(QUOTES[self.quote_i]))

    def tick(self):
        n = datetime.now()
        self.clock.setText(f"{_(DAY_NAMES[n.weekday()])}, {n:%d.%m.%Y  %H:%M:%S}")

    def current_pid(self):
        it = self.plist.currentItem()
        return it.data(Qt.UserRole) if it else None

    def refresh_totals(self):
        for c, (a, v) in self.db.totals_overall().items():
            self.total_tiles[c].set_totals(a, v)

    # --- kişiler
    def load_persons(self, *_a):
        keep = self.current_pid()
        self.plist.blockSignals(True)
        self.plist.clear()
        it = QListWidgetItem(_("★  Tüm kişiler"))
        it.setData(Qt.UserRole, self.ALL)
        self.plist.addItem(it)
        tag = self.f_tag.currentData() if hasattr(self, "f_tag") else None
        late = ekler.E.gecikmis_kisiler(self.db)
        for p in self.db.persons(self.search.text()):
            if tag and tag not in kisi_etiketleri(p):
                continue
            bal = self.db.balances(p["id"])
            parts = []
            for c in CURRENCIES:
                b = bal[c][2]
                if abs(b) >= 0.005:
                    parts.append(("+" if b > 0 else "") + money(b, c))
            it = QListWidgetItem(("⏰ " if p["id"] in late else "") + p["name"] +
                                 ("\n" + "  ".join(parts) if parts else "\n" + _("Hesap kapalı")))
            if p["id"] in late:
                it.setToolTip(_("Vadesi geçmiş hatırlatıcı var"))
            it.setData(Qt.UserRole, p["id"])
            it.setData(Qt.UserRole + 2, active_channels(p))
            self.plist.addItem(it)
        self.plist.blockSignals(False)
        row = 0
        for i in range(self.plist.count()):
            if self.plist.item(i).data(Qt.UserRole) == keep:
                row = i
        self.plist.setCurrentRow(row)
        self.load_person()
        self.refresh_totals()

    # --- v1.22 ekleri
    def fill_tags(self):
        keep = self.f_tag.currentData()
        self.f_tag.blockSignals(True)
        self.f_tag.clear()
        self.f_tag.addItem(_("🏷 Bütün etiketler"), None)
        tags = sorted({t for p in self.db.persons() for t in kisi_etiketleri(p)}, key=str.lower)
        for t in tags:
            self.f_tag.addItem("🏷 " + t, t)
        self.f_tag.setCurrentIndex(max(self.f_tag.findData(keep), 0))
        self.f_tag.setVisible(bool(tags))
        self.f_tag.blockSignals(False)

    def gizle_degistir(self, on):
        ekler.GIZLE[0] = bool(on)
        g = getattr(self.db, "guvenlik", None)
        if g is not None:
            g.a["gizle"] = bool(on)
            g.kaydet()
        self.goz.setText("🙈" if on else "👁")
        self.load_persons()

    def hizli_kayit(self, text):
        d = ekler.HizliKayitDialog(self, self.db, text)
        if d.exec():
            self.hizli.clear()
            self.fill_tags()
            self.load_persons()
            for i in range(self.plist.count()):
                if self.plist.item(i).data(Qt.UserRole) == d.pid:
                    self.plist.setCurrentRow(i)

    def _kisi_sec(self):
        pid = self.current_pid()
        if pid in (None, self.ALL):
            QMessageBox.information(self, _("Seçim"), _("Önce soldaki listeden bir kişi seçin."))
            return None
        return pid

    def mesaj(self):
        pid = self._kisi_sec()
        if pid is not None:
            ekler.MesajDialog(self, self.db, pid).exec()

    def taksit(self):
        if not self.db.persons():
            QMessageBox.information(self, _("Kişi yok"), _("Önce bir kişi ekleyin."))
            return
        pid = self.current_pid()
        if ekler.TaksitDialog(self, self.db, None if pid in (None, self.ALL) else pid).exec():
            self.load_persons()
            self.check_reminders(notify=False)

    def senet(self):
        pid = self.current_pid()
        ekler.SenetDialog(self, self.db, None if pid in (None, self.ALL) else pid).exec()

    def add_person(self):
        d = PersonDialog(self)
        if d.exec():
            pid = self.db.add_person(*d.values())
            self.search.clear()
            self.fill_tags()
            self.load_persons()
            for i in range(self.plist.count()):
                if self.plist.item(i).data(Qt.UserRole) == pid:
                    self.plist.setCurrentRow(i)

    def open_book(self):
        d = ContactBook(self, self.db)
        d.exec()
        if d.changed:
            self.load_persons()

    def edit_person(self):
        pid = self.current_pid()
        if pid in (None, self.ALL):
            return
        d = PersonDialog(self, self.db.person(pid))
        if d.exec():
            self.db.update_person(pid, *d.values())
            self.fill_tags()
            self.load_persons()

    def delete_person(self):
        pid = self.current_pid()
        if pid in (None, self.ALL):
            return
        p = self.db.person(pid)
        n = self.db.tx_count(pid)
        msg = _("'{}' silinsin mi?").format(p['name'])
        if n:
            msg += "\n\n" + _("Bu kişiye ait {} kayıt ve belgeleri de arşive taşınır; Ayarlar → Arşiv'den geri alabilirsiniz.").format(n)
        if QMessageBox.warning(self, _("Kişiyi sil"), msg, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.delete_person(pid)
            self.fill_tags()
            self.load_persons()
            self.geri_al.goster(_("“{}” silindi").format(p["name"]))

    def load_person(self):
        pid = self.current_pid()
        if pid == self.ALL or pid is None:
            self.pname.setText(_("Tüm kişiler"))
            self.pinfo.setText(_("Bütün kişilerin kayıtları"))
            self.chbar.set_person(None)
            bal = self.db.balances()
        else:
            p = self.db.person(pid)
            self.pname.setText(p["name"])
            self.chbar.set_person(pid)
            info = [x for x in (p["phone"], p["phone2"], p["email"], p["note"]) if x]
            if kisi_etiketleri(p):
                info.insert(0, "🏷 " + ", ".join(kisi_etiketleri(p)))
            nxt = self.db.reminders(pid)
            if nxt:
                info.append("🔔 " + _("Sıradaki hatırlatıcı") + ": " + reminder_text(nxt[0]).split(" — ")[0] + " — " +
                            _(KIND_TEXT[nxt[0]["kind"]]) +
                            (" " + money(nxt[0]["amount"], nxt[0]["currency"]) if nxt[0]["amount"] else ""))
            self.pinfo.setText(" • ".join(info) or " ")
            bal = self.db.balances(pid)
        for c in CURRENCIES:
            self.tiles[c].set_person(*bal[c])
        self.load_tx()

    # --- kayıtlar
    def load_tx(self, *_a):
        pid = self.current_pid()
        rows = self.db.transactions(None if pid in (None, self.ALL) else pid,
                                    currency=self.f_cur.currentData(), text=self.f_text.text())
        rows = list(reversed(rows))  # en yeni üstte
        if self.f_nodoc.isChecked():
            rows = [r for r in rows if not r["photo_count"]]
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            ver = r["direction"] == "VERDIM"
            vals = [ts_display(r["ts"]), r["person_name"], _("Verdim") if ver else _("Aldım"), r["currency"],
                    money(r["amount"], r["currency"]) if ver else "",
                    "" if ver else money(r["amount"], r["currency"]),
                    (r["description"] or "") + ("  ✎" if r["updated_at"] else ""),
                    str(r["photo_count"]) if r["photo_count"] else "⚠"]
            for j, v in enumerate(vals):
                it = QTableWidgetItem(v)
                if j == 0:
                    it.setData(Qt.UserRole, r["id"])
                if j in (2, 4, 5):
                    it.setForeground(QBrush(QColor(RED if ver else GREEN)))
                    f = it.font()
                    f.setBold(True)
                    it.setFont(f)
                if j == 7:
                    it.setTextAlignment(Qt.AlignCenter)
                    if not r["photo_count"]:
                        it.setForeground(QBrush(QColor(tok("warn-text"))))
                        it.setToolTip(_("Bu kaydın dekontu / belgesi yok"))
                if j in (4, 5):
                    it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(i, j, it)
        self.table.setColumnHidden(1, pid not in (None, self.ALL))
        filtre = bool(self.f_text.text() or self.f_cur.currentData() or self.f_nodoc.isChecked())
        if rows:
            self.empty.hide()
        elif not self.db.persons():
            self.empty.setText(_("Hoş geldiniz! Başlamak için soldan “+ Kişi Ekle”ye basın ya da üstteki hızlı kayıt kutusuna "
                                 "“Ahmet'e 500 TL verdim” gibi yazıp Enter'a basın."))
        elif filtre:
            self.empty.setText(_("Süzgece uyan kayıt yok. Arama kutusunu ya da para birimi seçimini temizleyin."))
        else:
            self.empty.setText(_("Bu sayfada henüz kayıt yok. “+ Verdim (Çıktı)” ya da “+ Aldım (Girdi)” ile ilk kaydı ekleyin."))
        self.empty.setVisible(not rows)
        self.table.setVisible(bool(rows))

    def selected_tid(self):
        r = self.table.currentRow()
        if r < 0:
            QMessageBox.information(self, _("Seçim"), _("Önce tablodan bir kayıt seçin."))
            return None
        return self.table.item(r, 0).data(Qt.UserRole)

    def after_change(self):
        self.load_persons()

    # --- hatırlatıcılar
    def due_reminders(self):
        return self.db.reminders(until=datetime.now().strftime("%Y-%m-%d %H:%M"))

    def update_reminder_button(self):
        today = self.db.reminders(until=datetime.now().strftime("%Y-%m-%d 23:59"))
        n = len(today)
        self.rem_btn.setText(_("🔔 Hatırlatıcılar") + (f" ({n})" if n else ""))
        self.rem_btn.setObjectName("gold" if self.due_reminders() else "light")
        self.rem_btn.style().unpolish(self.rem_btn)
        self.rem_btn.style().polish(self.rem_btn)

    def check_reminders(self, notify=True):
        due = self.due_reminders()
        new = [r for r in due if r["id"] not in self.db.notified]
        for r in new:
            self.db.notified.add(r["id"])
        if notify and new:
            text = "\n".join(reminder_text(r) for r in new[:5])
            if len(new) > 5:
                text += "\n…"
            if QSystemTrayIcon.isSystemTrayAvailable() and self.tray.supportsMessages():
                self.tray_target = "reminder"
                self.tray.showMessage(_("🔔 Hatırlatıcı"), text, QIcon(logo_pixmap(64)), 15000)
            QApplication.beep()
            self.flash_banner(text)
        self.update_reminder_button()

    def flash_banner(self, text):
        """Tam ekranda da görünen bildirim şeridi."""
        self.banner.setText("🔔  " + text.replace("\n", "   •   "))
        self.banner.show()
        QTimer.singleShot(20000, self.banner.hide)

    def startup_reminders(self):
        self.check_reminders(notify=False)
        today = self.db.reminders(until=datetime.now().strftime("%Y-%m-%d 23:59"))
        if today:
            d = RemindersDialog(self, self.db, due_only=True)
            d.exec()
            self.update_reminder_button()

    def open_reminders(self, pid=None):
        RemindersDialog(self, self.db, pid).exec()
        self.update_reminder_button()
        self.load_person()

    def add_reminder(self):
        if not self.db.persons():
            QMessageBox.information(self, _("Kişi yok"), _("Önce soldan bir kişi ekleyin."))
            return
        pid = self.current_pid()
        if ReminderDialog(self, self.db, None if pid == self.ALL else pid).exec():
            self.check_reminders(notify=False)
            self.load_person()

    def add_tx(self, direction):
        pid = self.current_pid()
        d = TxDialog(self, self.db, None if pid == self.ALL else pid)
        (d.r_al if direction == "ALDIM" else d.r_ver).setChecked(True)
        if d.exec():
            if d.created_pid is not None:
                # yeni kişi: kayıttan sonra kişinin defterine geç
                self.search.clear()
                self.load_persons()
                for i in range(self.plist.count()):
                    if self.plist.item(i).data(Qt.UserRole) == d.created_pid:
                        self.plist.setCurrentRow(i)
            self.after_change()

    def edit_tx(self):
        tid = self.selected_tid()
        if tid and TxDialog(self, self.db, tx=self.db.tx(tid)).exec():
            self.after_change()

    def delete_tx(self):
        tid = self.selected_tid()
        if not tid:
            return
        t = self.db.tx(tid)
        if QMessageBox.warning(self, _("Kaydı sil"),
                               _("{} tarihli {} kaydı ve belgeleri silinsin mi?").format(ts_display(t['ts']),
                                                                             money(t['amount'], t['currency'])), QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.delete_tx(tid)
            self.after_change()
            self.geri_al.goster(_("Kayıt silindi"))

    def show_photos(self):
        tid = self.selected_tid()
        if not tid:
            return
        photos = self.db.photos(tid)
        if not photos:
            if QMessageBox.question(self, _("Belge yok"), _("Bu kayıtta dekont / belge yok. Şimdi eklemek ister misiniz?")) \
                    == QMessageBox.Yes:
                self.edit_tx()
            return
        d = QDialog(self)
        d.setWindowTitle(_("Dekont / Belgeler"))
        d.resize(900, 300)
        lay = QVBoxLayout(d)
        lay.addWidget(QLabel(_("Açmak için çift tıklayın.")))
        s = PhotoStrip()
        s.setFixedHeight(220)
        s.setIconSize(QSize(240, 180))
        for ph in photos:
            s.add(self.db.photo_path(ph), ph["id"], ph["original_name"])
        lay.addWidget(s)
        row = QHBoxLayout()
        ob = QPushButton(_("Aç"))
        ob.clicked.connect(lambda: s.currentItem() and open_file(d, s.currentItem().data(Qt.UserRole + 1)))
        sb = QPushButton(_("Farklı kaydet…"))
        sb.clicked.connect(lambda: self.export_doc(d, s.currentItem()))
        row.addWidget(ob)
        row.addWidget(sb)
        row.addStretch()
        lay.addLayout(row)
        if s.count():
            s.setCurrentRow(0)
        d.exec()

    def export_doc(self, parent, item):
        if not item:
            return
        src = item.data(Qt.UserRole + 1)
        path, _f = QFileDialog.getSaveFileName(parent, _("Farklı kaydet…"), item.toolTip() or os.path.basename(src))
        if path:
            import shutil
            shutil.copyfile(src, path)

    def show_history(self):
        tid = self.selected_tid()
        if not tid:
            return
        hist = self.db.history(tid)
        if not hist:
            QMessageBox.information(self, _("Geçmiş"), _("Bu kayıt hiç değiştirilmemiş."))
            return
        lines = []
        for hrow in hist:
            o = parse_old(hrow["old_values"])  # v1.2: JSON, eski sürümler: repr(dict)
            if o.get("currency") not in CURRENCY_SYMBOLS:
                continue
            lines.append(f"{hrow['at']}  — {_('önceki hali')}: {ts_display(o.get('ts', ''))}, "
                         f"{_('Verdim') if o.get('direction') == 'VERDIM' else _('Aldım')} "
                         f"{money(float(o.get('amount') or 0), o['currency'])}  {o.get('description') or ''}")
        if not lines:
            QMessageBox.information(self, _("Geçmiş"), _("Bu kayıt hiç değiştirilmemiş."))
            return
        QMessageBox.information(self, _("Değişiklik Geçmişi"), "\n".join(lines))

    def statement(self):
        pid = self.current_pid()
        StatementDialog(self, self.db, None if pid in (None, self.ALL) else pid).exec()

    def backup(self):
        path, _f = QFileDialog.getSaveFileName(self, _("Yedek kaydet"),
                                              f"AlacakVerecek_yedek_{datetime.now():%Y%m%d_%H%M}.zip", "ZIP (*.zip)")
        if path:
            self.db.backup(path)
            QMessageBox.information(self, _("Yedek"), _("Yedek alındı:\n{}\n\nYedeği USB bellek gibi ayrı bir yerde "
                                                       "saklamanız önerilir.").format(path))


# ---------------------------------------------------------------- ortak çekirdek kabuğu (v1.21)
APP_ID = "bereket-defter"
KLASIK = {   # 1.20'ye kadarki görünüm: yeşil başlık, açık kartlar (her zaman açık temaydı)
    "label": {"tr": "Klasik (eski görünüm)", "en": "Classic (previous look)", "ar": "الكلاسيكي (المظهر السابق)"},
    "light": {
        "bg": "#e7f1ee", "bg-grid": "#00000000", "panel": "#ffffffee", "panel-solid": "#ffffff", "panel-hover": "#f4faf8",
        "border": "#c9d3d0", "border-strong": "#0f8f6a", "text": "#111111", "muted": "#667777", "label": "#06513f",
        "nav-text": "#33504a", "nav-title": "#6a837d", "accent": "#0f8f6a", "accent-2": "#0b6e74", "on-accent": "#ffffff",
        "primary-1": "#0f8f6a", "primary-2": "#0b6e74", "active-1": "#0f8f6a29", "active-2": "#0f8f6a12", "active-line": "#0f8f6a66",
        "accent-soft": "#e3f4ee", "accent-line": "#0f8f6a59", "focus": "#0f8f6a", "focus-ring": "#0f8f6a33",
        "danger": "#c0392b", "danger-text": "#c0392b", "danger-soft": "#fbe6e3", "danger-line": "#c0392b59",
        "ok": "#0f8f6a", "ok-text": "#0f8f6a", "ok-soft": "#e3f4ee", "ok-line": "#0f8f6a59",
        "warn": "#e0a200", "warn-text": "#5a4300", "warn-soft": "#fff3b0", "warn-line": "#e0a20080",
        "sidebar-bg": "#ffffff", "topbar-bg": "#f4f6f5f0", "modal-bg": "#f4f6f5", "modal-border": "#c9d3d0",
        "badge-text": "#06513f", "badge-bg": "#e3f4ee", "badge-line": "#c9d3d0", "on-badge": "#ffffff",
        "bar-track": "#e6ecea", "scroll-thumb": "#0f8f6a59",
    },
    "dark": {
        "bg": "#062b23", "bg-grid": "#00000000", "panel": "#0b3a30ee", "panel-solid": "#0b3a30", "panel-hover": "#0f4a3d",
        "border": "#1c5a4b", "border-strong": "#34c29a", "text": "#eef7f4", "muted": "#a7c4bc", "label": "#cfeee4",
        "nav-text": "#cfeee4", "nav-title": "#8fb7ab", "accent": "#34c29a", "accent-2": "#2aa6ad", "on-accent": "#04241c",
        "primary-1": "#34c29a", "primary-2": "#2aa6ad", "active-1": "#34c29a33", "active-2": "#34c29a1a", "active-line": "#34c29a66",
        "accent-soft": "#0f4a3d", "accent-line": "#34c29a59", "focus": "#34c29a", "focus-ring": "#34c29a33",
        "danger": "#ff8a7a", "danger-text": "#ff8a7a", "danger-soft": "#4a1f1b", "danger-line": "#ff8a7a59",
        "ok": "#5ee0b5", "ok-text": "#5ee0b5", "ok-soft": "#0f4a3d", "ok-line": "#5ee0b559",
        "warn": "#ffd24a", "warn-text": "#ffd24a", "warn-soft": "#4a3a0a", "warn-line": "#ffd24a59",
        "sidebar-bg": "#06513f", "topbar-bg": "#0b6e74", "modal-bg": "#062b23", "modal-border": "#1c5a4b",
        "badge-text": "#eef7f4", "badge-bg": "#0f4a3d", "badge-line": "#1c5a4b", "on-badge": "#04241c",
        "bar-track": "#0f4a3d", "scroll-thumb": "#a7c4bc40",
    },
}

fccore.i18n.add({
    "tr": {"bd.nav": "Defter", "bd.nav.book": "Alacak-Verecek", "bd.nav.settings": "Ayarlar", "bd.nav.rapor": "Raporlar",
           "bd.rapor.sub": "Özet, yaşlandırma, en büyük bakiyeler, aylık hareket, gecikenler, CSV", "bd.tag": "Alacak-Verecek Defteri",
           "bd.sub": "Kişiler, kayıtlar, belgeler ve hatırlatıcılar", "bd.set.sub": "Görünüm, eşitleme, arşiv ve iletişim",
           "bd.sync": "Eşitleme (telefon ⇄ bilgisayar)",
           "bd.sync.desc": "Kayıtlar kendi Firebase hesabınızla telefon ve bilgisayarlar arasında eşitlenir; aynı ağdaysanız Wi‑Fi ile internetsiz de eşitlenir. Hiçbir kayıt silinmez ya da körü körüne üzerine yazılmaz.",
           "bd.sync.open": "Eşitleme ayarları", "bd.sync.lan": "Wi‑Fi eşitleme",
           "bd.arsiv": "Arşiv ve silinenler",
           "bd.arsiv.desc": "Başka cihazda silinen kayıtlar bu cihazda silinmez, burada arşivlenir. Kendi sildikleriniz de burada durur; istediğinizi geri alabilirsiniz.",
           "bd.arsiv.bos": "Arşivde kayıt yok.", "bd.arsiv.geri": "Geri al", "bd.arsiv.geriAlindi": "Geri alındı: {s}",
           "bd.arsiv.olmadi": "Geri alınamadı: bağlı olduğu kişi ya da kayıt yok. Önce onu geri alın.",
           "bd.arsiv.uzak": "başka cihazda silindi", "bd.arsiv.yerel": "bu cihazda silindi",
           "bd.arsiv.yedek": "Çakışma yedeği: {n} kayıt", "bd.arsiv.yedekKaydet": "Yedekleri kaydet (JSON)",
           "bd.tur.persons": "Kişi", "bd.tur.tx": "Kayıt", "bd.tur.rem": "Hatırlatıcı", "bd.tur.docs": "Belge",
           "bd.yedek": "Yedek", "bd.yedek.desc": "Kayıtların ve belgelerin tam yedeğini ZIP dosyası olarak alın. Yedeği USB bellek gibi ayrı bir yerde saklayın.",
           "bd.yedek.al": "Yedek al", "bd.cikis": "Programdan çıkmak istiyor musunuz?", "bd.cikis.t": "Çıkış",
           "bd.ob.fb": "Firebase bilgileri kaydedildi. Eşitleme penceresinde e-posta ve şifrenizle giriş yapın (ilk kez ise \"Hesap oluştur\")."},
    "en": {"bd.nav": "Ledger", "bd.nav.book": "Receivables & payables", "bd.nav.settings": "Settings", "bd.nav.rapor": "Reports",
           "bd.rapor.sub": "Summary, aging, largest balances, monthly activity, overdue items, CSV", "bd.tag": "Receivables & Payables Ledger",
           "bd.sub": "People, records, documents and reminders", "bd.set.sub": "Appearance, sync, archive and contact",
           "bd.sync": "Sync (phone ⇄ computer)",
           "bd.sync.desc": "Records sync between phones and computers through your own Firebase account; on the same network they also sync over Wi‑Fi without internet. Nothing is deleted or blindly overwritten.",
           "bd.sync.open": "Sync settings", "bd.sync.lan": "Wi‑Fi sync",
           "bd.arsiv": "Archive and deleted",
           "bd.arsiv.desc": "Records deleted on another device are not deleted here; they are archived. Records you deleted yourself are kept here too, and you can restore any of them.",
           "bd.arsiv.bos": "The archive is empty.", "bd.arsiv.geri": "Restore", "bd.arsiv.geriAlindi": "Restored: {s}",
           "bd.arsiv.olmadi": "Could not restore: the person or record it belongs to is missing. Restore that first.",
           "bd.arsiv.uzak": "deleted on another device", "bd.arsiv.yerel": "deleted on this device",
           "bd.arsiv.yedek": "Conflict backup: {n} records", "bd.arsiv.yedekKaydet": "Save backups (JSON)",
           "bd.tur.persons": "Person", "bd.tur.tx": "Record", "bd.tur.rem": "Reminder", "bd.tur.docs": "Document",
           "bd.yedek": "Backup", "bd.yedek.desc": "Take a full backup of records and documents as a ZIP file. Keep it somewhere separate, such as a USB stick.",
           "bd.yedek.al": "Back up", "bd.cikis": "Do you want to exit the program?", "bd.cikis.t": "Exit",
           "bd.ob.fb": "Firebase details saved. Sign in with your e-mail and password in the sync window (first time: \"Create account\")."},
    "ar": {"bd.nav": "الدفتر", "bd.nav.book": "الديون والمستحقات", "bd.nav.settings": "الإعدادات", "bd.nav.rapor": "التقارير",
           "bd.rapor.sub": "الملخص، أعمار الأرصدة، أكبر الأرصدة، الحركة الشهرية، المتأخرات، CSV", "bd.tag": "دفتر الديون والمستحقات",
           "bd.sub": "الأشخاص والسجلات والمستندات والتذكيرات", "bd.set.sub": "المظهر والمزامنة والأرشيف والتواصل",
           "bd.sync": "المزامنة (الهاتف ⇄ الحاسوب)",
           "bd.sync.desc": "تتم مزامنة السجلات بين الهواتف والحواسيب عبر حساب Firebase الخاص بك؛ وفي الشبكة نفسها تتم المزامنة عبر Wi‑Fi دون إنترنت أيضاً. لا يُحذف شيء ولا يُكتب فوق شيء دون تحقق.",
           "bd.sync.open": "إعدادات المزامنة", "bd.sync.lan": "مزامنة Wi‑Fi",
           "bd.arsiv": "الأرشيف والمحذوفات",
           "bd.arsiv.desc": "السجلات المحذوفة على جهاز آخر لا تُحذف هنا بل تُؤرشف. وتبقى هنا أيضاً السجلات التي حذفتها بنفسك، ويمكنك استعادة أيٍّ منها.",
           "bd.arsiv.bos": "الأرشيف فارغ.", "bd.arsiv.geri": "استعادة", "bd.arsiv.geriAlindi": "تمت الاستعادة: {s}",
           "bd.arsiv.olmadi": "تعذّرت الاستعادة: الشخص أو السجل المرتبط غير موجود. استعده أولاً.",
           "bd.arsiv.uzak": "حُذف على جهاز آخر", "bd.arsiv.yerel": "حُذف على هذا الجهاز",
           "bd.arsiv.yedek": "نسخة احتياطية للتعارضات: {n} سجل", "bd.arsiv.yedekKaydet": "حفظ النسخ الاحتياطية (JSON)",
           "bd.tur.persons": "شخص", "bd.tur.tx": "سجل", "bd.tur.rem": "تذكير", "bd.tur.docs": "مستند",
           "bd.yedek": "النسخ الاحتياطي", "bd.yedek.desc": "خذ نسخة احتياطية كاملة من السجلات والمستندات كملف ZIP، واحفظها في مكان منفصل مثل ذاكرة USB.",
           "bd.yedek.al": "نسخ احتياطي", "bd.cikis": "هل تريد الخروج من البرنامج؟", "bd.cikis.t": "خروج",
           "bd.ob.fb": "تم حفظ بيانات Firebase. سجّل الدخول ببريدك الإلكتروني وكلمة المرور في نافذة المزامنة (أول مرة: «إنشاء حساب»)."},
})


def build_app(app, db, first_start=True):
    """Çekirdek kabuğu: kenar çubuğu (Defter · Ayarlar), üst çubuk (Duyurular · Eşitle · Wi‑Fi · Güncelle · tema · dil |
    Küçült · Orta · Tam ekran · Kapat), ayarlar ızgarası (Görünüm … Hakkında, Admin ile iletişim EN SON)."""
    from fccore import settings as fcsettings, widgets as W
    from fccore.window import FcWindow, Shell
    from fccore.i18n import t

    class Win(FcWindow):
        def closeEvent(self, e):
            if getattr(self, "quitting", False) or QApplication.instance().property("fcUpdateQuit"):   # güncelleme kapanışı sormaz
                e.accept()
                return
            if QMessageBox.question(self, t("bd.cikis.t"), t("bd.cikis")) == QMessageBox.Yes:
                e.accept()
            else:
                e.ignore()

    win = Win(_(APP_TITLE))
    win.setWindowIcon(QIcon(logo_pixmap(128)))
    shell = Shell(win, name="Bereket", tag="bd.tag", version=APP_VERSION, logo="home")
    shell.logo.setPixmap(logo_pixmap(34))
    shell.db = db
    host = QWidget()
    hl = QVBoxLayout(host)
    hl.setContentsMargins(0, 0, 0, 0)
    shell.nav_group("bd.nav")
    shell.page("defter", "bd.nav.book", "home", host, sub="bd.sub", scroll=False)
    shell.defter = None
    if not hasattr(db, "guvenlik"):   # v1.22: PIN kilidi, tutar gizleme, otomatik yedek (bu cihaza özel ayarlar)
        db.guvenlik = ekler.Guvenlik(db)
    db.guvenlik.win = win
    shell.rapor = ekler.RaporSayfasi(db, shell)
    shell.page("rapor", "bd.nav.rapor", "gauge", shell.rapor, sub="bd.rapor.sub", scroll=False)

    def esitle(_state=None):
        d = shell.defter
        if d is not None:
            d.sync_button_clicked()

    def wifi(_state=None):
        d = shell.defter
        if d is not None:
            d.open_sync(lan_only=True)

    shell.tb = shell.topbar.mount(sync={"on_click": esitle}, lan={"on_click": wifi}, update=app.fc.updates,
                                  before=[app.fc.ann.button()] if app.fc.ann is not None else None)

    def build_defter(first=False):
        old = shell.defter
        i18n.set_language(fccore.i18n.lang())
        refresh_colors()
        shell.defter = MainWindow(db, first_start=first, shell=shell)
        hl.addWidget(shell.defter)
        if old is not None:
            old.setParent(None)
            old.deleteLater()
        if AJAN is not None:
            try:
                AJAN.attach_button(win)
            except Exception:
                pass

    # --- ayarlar
    setbox = QWidget()
    sl = QVBoxLayout(setbox)
    sl.setContentsMargins(0, 0, 0, 0)
    shell.nav_group("bd.nav.settings")
    shell.page("ayarlar", "bd.nav.settings", "settings", setbox, sub="bd.set.sub")
    shell.grid = None

    def sync_card():
        c = W.Card("bereket-sync", t("bd.sync"), "sync", t("bd.sync.desc"))
        c.add(W.hbox(W.button(t("bd.sync.open"), "btn small primary", icon="sync", slot=lambda: shell.defter and shell.defter.open_sync()),
                     W.button(t("bd.sync.lan"), "btn small", icon="wifi", slot=wifi), stretch_end=True))
        return c

    def backup_card():
        c = W.Card("bereket-yedek", t("bd.yedek"), "download", t("bd.yedek.desc"))
        c.add(W.hbox(W.button(t("bd.yedek.al"), "btn small", icon="download", slot=lambda: shell.defter and shell.defter.backup()),
                     stretch_end=True))
        return c

    def archive_card():
        c = W.Card("bereket-arsiv", t("bd.arsiv"), "box", t("bd.arsiv.desc"))
        rows = db.archived(60)
        if not rows:
            c.add(W.label(t("bd.arsiv.bos"), "muted"))
        for a in rows[:40]:
            line = QFrame()
            line.setProperty("fc", "fc-li")
            h = QHBoxLayout(line)
            h.setContentsMargins(10, 6, 10, 6)
            info = W.label(f"{t('bd.tur.' + a['tur'])} · {a['baslik'] or '—'}\n"
                           f"{t('bd.arsiv.uzak') if a['kaynak'] == 'uzak' else t('bd.arsiv.yerel')} · {ts_display(a['at'])}",
                           wrap=True)
            h.addWidget(info, 1)

            def geri(_=False, aid=a["id"], title=a["baslik"]):
                try:
                    ok = db.restore(aid)
                except Exception as e:  # pragma: no cover
                    ok = False
                    print("geri alınamadı", e)
                if ok:
                    W.toast(t("bd.arsiv.geriAlindi", {"s": title or ""}), "ok")
                    if shell.defter is not None:
                        shell.defter.load_persons()
                else:
                    W.toast(t("bd.arsiv.olmadi"), "error", 7000)
                rebuild_settings()
            h.addWidget(W.button(t("bd.arsiv.geri"), "btn small", icon="sync", slot=geri))
            c.add(line, top=6)
        conf = db.conflicts()
        if conf:
            c.add(W.label(t("bd.arsiv.yedek", {"n": len(conf)}), "muted"), top=10)

            def kaydet():
                import json as _json
                path, _f = QFileDialog.getSaveFileName(setbox, t("bd.arsiv.yedekKaydet"),
                                                      f"bereket-cakisma-yedekleri-{datetime.now():%Y%m%d}.json", "JSON (*.json)")
                if path:
                    with open(path, "w", encoding="utf-8") as f:
                        _json.dump([{k: r[k] for k in r.keys()} for r in conf], f, ensure_ascii=False, indent=1)
            c.add(W.hbox(W.button(t("bd.arsiv.yedekKaydet"), "btn small", icon="download", slot=kaydet), stretch_end=True), top=6)
        return c

    def agent_card():
        if AJAN is None:
            return None
        try:
            box = AJAN.card(setbox)
            box.setProperty("fc", "card")
            return box
        except Exception:
            return None

    def rebuild_settings():
        old = shell.grid
        shell.grid = fcsettings.build(cards=[sync_card(), ekler.guvenlik_karti(shell, db, W, rebuild_settings), archive_card(),
                                             backup_card(), ekler.kisayol_karti(W), agent_card()],
                                      usage={"firebase": True, "ai": False,
                                             "project": lambda: db.sync_engine.cfg.get("projectId") if getattr(db, "sync_engine", None) else ""},
                                      about={"version": APP_VERSION, "on_check": (app.fc.updates.check if app.fc.updates else None)},
                                      onboarding=onboarding_opts(shell))
        sl.addWidget(shell.grid)
        if old is not None:
            old.setParent(None)
            old.deleteLater()

    shell.page_changed.connect(lambda k: k == "ayarlar" and rebuild_settings())
    fccore.i18n.on_change(lambda l: (build_defter(), rebuild_settings(), shell.rapor.kur()))
    fcstyle.on_change(lambda st: (app.setStyleSheet(fcstyle.qss() + app_qss()), shell.defter is not None and
                                  getattr(shell, "_scheme", None) != (st.get("scheme"), st.get("effective")) and
                                  (setattr(shell, "_scheme", (st.get("scheme"), st.get("effective"))), build_defter())))
    shell._scheme = (fcstyle.scheme(), fcstyle.effective())
    app.setStyleSheet(fcstyle.qss() + app_qss())
    build_defter(first_start)
    rebuild_settings()
    shell.show_page("defter")
    QTimer.singleShot(0, db.guvenlik.kilitle)            # PIN varsa açılışta kilit ekranı
    QTimer.singleShot(5000, db.guvenlik.oto_yedek)       # günde bir otomatik yedek
    return win, shell


def onboarding_opts(shell):
    """İlk açılış rehberi: dil → görünüm → kendi Firebase'iniz (AI adımı yok)."""
    from fccore.i18n import t

    def on_fb(cfg, _code):
        eng = getattr(shell.db, "sync_engine", None)
        if eng is None or eng.signed_in():
            return
        with eng._lock:
            eng.cfg["apiKey"] = cfg.get("apiKey", "")
            eng.cfg["projectId"] = cfg.get("projectId", "")
        eng._save()
        shell._ob_fb = True

    def on_close():
        if getattr(shell, "_ob_fb", False) and shell.defter is not None:
            shell._ob_fb = False
            from fccore.widgets import toast
            toast(t("bd.ob.fb"), "info", 9000)
            QTimer.singleShot(400, shell.defter.open_sync)
    return {"firebase": True, "ai": False, "on_firebase": on_fb, "on_close": on_close}


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setApplicationName("Bereket Defter")
    i18n.load_language()
    db = DB()
    # çekirdek ayarları programın kendi veri klasöründe (fccore.json); ilk açılışta eski dil ayarı taşınır
    fccore.storage.use(db.dir, app=APP_ID)
    eski = os.path.exists(os.path.join(db.dir, "veriler.db")) and db.con.execute("SELECT COUNT(*) FROM persons").fetchone()[0] > 0
    if fccore.storage.get("lang") is None:
        fccore.storage.set("lang", i18n.lang())
        if eski:   # 1.20'den gelen kullanıcı: rehber gösterilmez, "neler yeni" gösterilir
            fccore.storage.set("onboarding.done", True)
            if fccore.storage.get("whatsnew.seen") is None:
                fccore.storage.set("whatsnew.seen", "1.20.0")
    fcstyle.register_scheme("klasik", dark=KLASIK["dark"], light=KLASIK["light"], label=KLASIK["label"])
    core = fccore.init(app, app_id=APP_ID, repo="bereket-defter", version=APP_VERSION, data_dir=db.dir, announcements=True,
                       agent=False)   # kendi Asistan Agent bağlantısı (fc_agent.py)
    from fccore import whatsnew
    from notlar import NOTES
    whatsnew.cfg["notes"] = lambda v: NOTES.get(str(v))
    app.fc = core
    i18n.set_language(fccore.i18n.lang())
    app.setWindowIcon(QIcon(logo_pixmap(128)))

    global AJAN
    if fc_agent is not None:
        try:
            AJAN = fc_agent.Agent(APP_ID, APP_VERSION, lang=lambda: fccore.i18n.lang(), sync=True)
        except Exception:
            AJAN = None
    win, shell = build_app(app, db, first_start=True)
    win.start()
    if AJAN is not None:
        try:
            AJAN.start(app, win)
        except Exception:
            pass
    core.after_show()
    if not fccore.storage.get("onboarding.done", False) and not core.whatsnew_shown:
        from fccore import onboarding as ob
        QTimer.singleShot(700, lambda: ob.maybe_start(**onboarding_opts(shell)))
    app._win, app._shell = win, shell
    smoke = os.environ.get("BEREKET_SMOKE")   # CI: paketlenmiş exe açılıyor mu (eksik modül / yazı tipi)
    if smoke:
        def _smoke():
            with open(smoke, "w", encoding="utf-8") as f:
                f.write("ok " + APP_VERSION + " " + fcstyle.scheme())
            win.quitting = True
            app.quit()
        QTimer.singleShot(4000, _smoke)
    code = app.exec()
    try:
        db.sync_engine.lan_server.stop()
    except Exception:
        pass
    return code


if __name__ == "__main__":
    sys.exit(main())
