"""Bereket Alacak-Verecek Defteri — ana program."""
import html
import os
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
try:
    import fc_agent  # Asistan Agent (ortak-cekirdek/python/fc_agent.py)
except Exception:  # pragma: no cover
    fc_agent = None
AJAN = None
from db import CHANNELS, CONTACT_FIELDS, CURRENCIES, CURRENCY_NAMES, CURRENCY_SYMBOLS, DB, parse_old
from sync import RULES, SyncEngine
import guncelle
import duyuru_istemci
import kullanim_sayac

APP_TITLE = "Bereket Alacak-Verecek Defteri"
# Her güncellemede yükseltilir (portable RAR adı ve kurulum sürümü de buna uyar)
APP_VERSION = "1.20"
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
GREEN, RED = "#0f8f6a", "#c0392b"


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
    return f"{fmt(x)} {CURRENCY_SYMBOLS[cur]}"


def ts_display(ts):
    try:
        d = datetime.strptime((ts or "")[:16], "%Y-%m-%d %H:%M")
    except ValueError:  # başka cihazdan beklenmeyen biçim gelirse olduğu gibi göster
        return ts or ""
    return d.strftime("%d.%m.%Y %H:%M")


STYLE = """
* { font-family: 'Segoe UI', Arial, sans-serif; font-size: 15px; }
QFrame#card { background: rgba(255,255,255,238); border-radius: 18px; }
QLabel#title { color: white; font-size: 30px; font-weight: 700; }
QLabel#quote { color: #fff3b0; font-size: 16px; font-style: italic; }
QLabel#clock { color: white; font-size: 18px; }
QLabel#h2 { font-size: 21px; font-weight: 700; color: #06513f; }
QLabel#muted { color: #667; }
QPushButton { background: #0f8f6a; color: white; border: none; border-radius: 10px; padding: 9px 16px;
              font-weight: 600; }
QPushButton:hover { background: #12a87c; }
QPushButton:disabled { background: #aab; }
QPushButton#danger { background: #c0392b; }
QPushButton#danger:hover { background: #d9493a; }
QPushButton#light { background: rgba(255,255,255,40); border: 1px solid rgba(255,255,255,120); }
QPushButton#light:hover { background: rgba(255,255,255,70); }
QPushButton#gold { background: #e0a200; color: #2b1d00; }
QLineEdit, QCheckBox, QComboBox, QDateTimeEdit, QDoubleSpinBox, QTextEdit, QPlainTextEdit, QSpinBox {
    border: 1px solid #c9d3d0; border-radius: 8px; padding: 6px; background: white; color: #111;
    selection-background-color: #0f8f6a; selection-color: white; }
QComboBox QAbstractItemView { background: white; color: #111; selection-background-color: #0f8f6a;
    selection-color: white; }
QTableWidget, QTableView { color: #111; }
QListWidget { border: none; background: transparent; }
QListWidget::item { padding: 10px; border-radius: 10px; margin: 2px 0; }
QListWidget::item:selected { background: #0f8f6a; color: white; }
QListWidget::item:hover:!selected { background: #e3f4ee; }
QTableWidget { border: none; gridline-color: #e6ecea; background: white; border-radius: 10px;
               alternate-background-color: #f4faf8; }
QHeaderView::section { background: #06513f; color: white; padding: 8px; border: none; font-weight: 600; }
"""


class Background(QWidget):
    """Moral veren gradyan arka plan."""

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        g = QLinearGradient(0, 0, w, h)
        g.setColorAt(0, QColor("#06513f"))
        g.setColorAt(0.55, QColor("#0b6e74"))
        g.setColorAt(1, QColor("#123a6b"))
        p.fillRect(self.rect(), g)
        # yükselen güneş
        rg = QRadialGradient(w * 0.85, h * 1.05, h * 0.9)
        rg.setColorAt(0, QColor(255, 210, 74, 120))
        rg.setColorAt(1, QColor(255, 210, 74, 0))
        p.fillRect(self.rect(), rg)
        # yükselen grafik çizgileri
        p.setPen(QPen(QColor(255, 255, 255, 22), 3))
        for k in range(6):
            off = k * h * 0.12
            pts = [(0, h * 0.95 - off), (w * 0.25, h * 0.85 - off), (w * 0.45, h * 0.9 - off),
                   (w * 0.7, h * 0.65 - off), (w, h * 0.45 - off)]
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                p.drawLine(int(x1), int(y1), int(x2), int(y2))
        # yıldızcıklar
        rnd = random.Random(7)
        p.setPen(Qt.NoPen)
        for _i in range(60):
            p.setBrush(QColor(255, 255, 255, rnd.randint(15, 60)))
            r = rnd.uniform(1, 3)
            p.drawEllipse(QRectF(rnd.uniform(0, w), rnd.uniform(0, h * 0.6), r, r))
        # filigran logo
        p.setOpacity(0.06)
        s = int(min(w, h) * 0.55)
        QSvgRenderer(resource("logo.svg")).render(p, QRectF(w - s * 0.8, h - s * 0.8, s, s))
        p.end()


def card():
    f = QFrame()
    f.setObjectName("card")
    return f


class BalanceTile(QFrame):
    def __init__(self, cur):
        super().__init__()
        self.cur = cur
        self.setStyleSheet("QFrame{background:#f4faf8;border-radius:14px;}")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 10, 14, 10)
        t = QLabel(_(CURRENCY_NAMES[cur]))
        t.setStyleSheet("font-weight:700;color:#06513f;")
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
            self.main.setStyleSheet("font-size:22px;font-weight:700;color:#556;")
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
                            "QPushButton:hover{background:#dff1ea;}")
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
        painter.setPen(QColor("white") if selected else QColor("#111111"))
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
                painter.setBrush(QColor("white"))
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
                             ("email", "E-posta", ""), ("address", "Adres", "")):
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
        self.setStyleSheet("QListWidget{background:#f4faf8;border-radius:10px;}")
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
        self.hint.setStyleSheet("background:#fff3b0;color:#5a4300;padding:8px;border-radius:8px;")
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
                    f"<td style='color:{RED if ver else GREEN}'>{_('Verdim') if ver else _('Aldım')}</td><td>{c}</td>"
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
        col = GREEN if b > 0 else RED
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
        return "today", _("Bugün"), "#d97a00"
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
        self.head.setStyleSheet("font-size:19px;font-weight:700;color:#06513f;")
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

    def __init__(self, parent, engine):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle(_("☁ Eşitleme (telefon ⇄ bilgisayar)"))
        self.setMinimumWidth(1000)
        outer = QHBoxLayout(self)
        outer.setSpacing(18)
        left = QVBoxLayout()
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
        self.adv.setStyleSheet("QPushButton{background:transparent;color:#0b6e74;padding:2px;text-align:left;}")
        self.adv.clicked.connect(lambda: self.show_advanced(not self.emu.isVisible()))
        f.addRow("", self.adv)
        self.emu_lbl = QLabel(_("Emülatör adresi (yalnızca test)"))
        f.addRow(self.emu_lbl, self.emu)
        left.addLayout(f)
        self.account = QLabel()
        self.account.setStyleSheet("font-weight:700;color:#06513f;")
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
        # --- Wi‑Fi (internetsiz) eşitleme: ikinci seçenek
        lan = getattr(engine, "lan_server", None)
        if lan is not None:
            wbox = QFrame()
            wbox.setStyleSheet("QFrame{background:#eef7f5;border-radius:12px;}")
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
            self.lan_info.setStyleSheet("font-size:17px;font-weight:700;color:#06513f;")
            wl.addWidget(self.lan_info)
            self.lan_last = QLabel()
            self.lan_last.setObjectName("muted")
            wl.addWidget(self.lan_last)
            nb = QPushButton(_("Yeni kod üret"))
            nb.clicked.connect(lambda: (lan.new_code(), self.refresh_lan()))
            wl.addWidget(nb, 0, Qt.AlignLeft if not i18n.is_rtl() else Qt.AlignRight)
            left.addWidget(wbox)
            self.refresh_lan()
        left.addStretch(1)
        close = QPushButton(_("Kapat"))
        close.clicked.connect(self.accept)
        crow = QHBoxLayout()
        crow.addStretch(1)
        crow.addWidget(close)
        left.addLayout(crow)
        outer.addLayout(left, 4)

        helpbox = QFrame()
        helpbox.setStyleSheet("QFrame{background:#f4faf8;border-radius:12px;}")
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


# ---------------------------------------------------------------- güncelleme
UPDATE_ERRORS = {
    "NETWORK": "İnternet bağlantısı yok veya sunucuya ulaşılamadı.",
    "BAD_PACKAGE": "İndirilen güncelleme bozuk, tekrar deneyin.",
    "WRITE": "Program klasörüne yazılamadı. Programı yazma izni olan bir klasörde çalıştırın.",
    "FROZEN": "Bu kurulumda güncelleme yeni kurulum dosyasıyla yapılır.",
}


def _num(x, dg):
    s = f"{x:.{dg}f}"
    return s if i18n.lang() == "en" else s.replace(".", ",")


def fmt_mb(b, ref=None):
    return _num(b / 1048576, 1 if (ref or b) >= 10 * 1048576 else 2)


def fmt_speed(bps):
    if bps >= 1048576:
        return _("{} MB/sn").format(_num(bps / 1048576, 1))
    return _("{} KB/sn").format(max(1, round(bps / 1024)))


def fmt_eta(sec):
    sec = max(1, int(round(sec)))
    if sec < 60:
        return _("~{} sn").format(sec)
    m, r = divmod(sec, 60)
    return _("~{} dk {} sn").format(m, r) if r else _("~{} dk").format(m)


def download_progress_info(done, total, speed):
    """İndirme bilgisi parça parça: (yüzde, [ (etiket, değer), ... ])"""
    if not total:
        return None
    left = max(total - done, 0)
    parts = [("", _("{} / {} MB").format(fmt_mb(done, total), fmt_mb(total, total))),
             (_("Kalan:"), _("{} MB").format(fmt_mb(left, total)))]
    if speed > 0:
        parts.append((_("Hız:"), fmt_speed(speed)))
        if left > 0 and done > 0:
            parts.append((_("Kalan süre:"), fmt_eta(left / speed)))
    return min(100, int(done * 100 / total)), parts


def download_progress_html(parts):
    """Her parça kendi içinde bölünmez (&nbsp;); satır yalnızca parçaların arasında kırılır."""
    from html import escape
    out = []
    for label, val in parts:
        txt = (f"<b>{escape(label)}</b> " if label else "") + "\u2066" + escape(val) + "\u2069"
        out.append(txt.replace(" ", "&nbsp;"))
    d = "rtl" if i18n.is_rtl() else "ltr"
    return f'<p dir="{d}" style="font-size:14px;">' + "&nbsp;&nbsp;·&nbsp; ".join(out) + "</p>"


def update_error_text(code):
    key = (code or "").split(":")[0].strip()
    return _(UPDATE_ERRORS[key]) if key in UPDATE_ERRORS else _("Güncelleme hatası: {}").format(code)


class UpdateDialog(QDialog):
    """⬆ Güncelleme: yeni sürüm varsa tek tıkla indirir, kurar ve programı yeniden başlatır."""

    def __init__(self, parent, updater, auto_install=False):
        super().__init__(parent)
        self.up = updater
        self.setWindowTitle(_("⬆ Güncelleme"))
        self.setMinimumWidth(560)
        lay = QVBoxLayout(self)
        h = QLabel(_("⬆ Güncelleme"))
        h.setObjectName("h2")
        lay.addWidget(h)
        self.cur = QLabel(_("Kullandığınız sürüm: {}").format("v" + APP_VERSION))
        lay.addWidget(self.cur)
        self.msg = QLabel()
        self.msg.setWordWrap(True)
        self.msg.setStyleSheet("font-size:17px;font-weight:700;")
        lay.addWidget(self.msg)
        # indirme: çubuk + bölünmeyen bilgi parçaları
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(12)
        self.bar.setStyleSheet("QProgressBar{border:none;border-radius:6px;background:rgba(0,0,0,0.08);}"
                               "QProgressBar::chunk{border-radius:6px;background:#0f8f6a;}")
        self.bar.hide()
        lay.addWidget(self.bar)
        self.stats = QLabel()
        self.stats.setTextFormat(Qt.RichText)
        self.stats.setWordWrap(True)
        self.stats.hide()
        lay.addWidget(self.stats)
        self.notes = QLabel()
        self.notes.setWordWrap(True)
        self.notes.setObjectName("muted")
        lay.addWidget(self.notes)
        info = QLabel(_("Güncelleme sadece program dosyalarını yeniler; kayıtlarınız, kişileriniz ve dekontlarınız "
                        "olduğu gibi kalır."))
        info.setWordWrap(True)
        info.setObjectName("muted")
        lay.addWidget(info)
        bb = QHBoxLayout()
        self.b_check = QPushButton(_("Tekrar denetle"))
        self.b_check.clicked.connect(self.up.check_async)
        self.b_go = QPushButton(_("⬆ Güncelle"))
        self.b_go.setObjectName("gold")
        self.b_go.clicked.connect(self.go)
        close = QPushButton(_("Kapat"))
        close.clicked.connect(self.reject)
        b_set = QPushButton(_("⚙ Denetim ayarları"))
        b_set.clicked.connect(lambda: self.parent().open_settings())
        bb.addWidget(self.b_check)
        bb.addWidget(b_set)
        bb.addStretch()
        bb.addWidget(close)
        bb.addWidget(self.b_go)
        lay.addLayout(bb)
        self.poll = QTimer(self, interval=300, timeout=self.refresh)
        self.poll.start()
        if auto_install and self.up.state == "available":
            self.up.install_async()
        elif self.up.state in ("idle", "none", "error"):
            self.up.check_async()
        self.refresh()

    def go(self):
        self.up.install_async()
        self.refresh()

    def refresh(self):
        st, info = self.up.state, self.up.info or {}
        busy = st in ("checking", "downloading", "installed")
        self.b_check.setEnabled(not busy)
        self.b_go.setVisible(st == "available")
        notes = str(info.get("notlar") or "").strip()
        self.notes.setText(notes if st == "available" else "")
        self.bar.setVisible(st == "downloading")
        self.stats.setVisible(st == "downloading")
        if st == "checking":
            self.msg.setText(_("Yeni sürüm denetleniyor…"))
        elif st == "none":
            self.msg.setText(_("Program güncel. Yeni sürüm yok."))
        elif st == "available":
            self.msg.setText(_("Yeni sürüm hazır: {}").format("v" + str(info.get("surum"))))
        elif st == "downloading":
            done, total = self.up.progress
            pi = download_progress_info(done, total, self.up.speed)
            if pi:
                self.msg.setText(_("Güncelleme indiriliyor… %{}").format(pi[0]))
                self.bar.setValue(pi[0])
                self.stats.setText(download_progress_html(pi[1]))
            else:
                self.msg.setText(_("Güncelleme indiriliyor…"))
                self.bar.setValue(0)
                self.stats.setText("")
        elif st == "installed":
            self.msg.setText(_("Güncelleme kuruldu. Program yeniden başlatılıyor…"))
            self.poll.stop()
            QTimer.singleShot(900, self.parent().restart_after_update)
        elif st == "error":
            self.msg.setText(update_error_text(self.up.error))
        else:
            self.msg.setText("")


class SettingsDialog(QDialog):
    """⚙ Ayarlar: yeni sürüm bildirimi. Denetim yalnızca program açılışında yapılır."""

    def __init__(self, parent, cfg):
        super().__init__(parent)
        self.setWindowTitle(_("⚙ Ayarlar"))
        self.setMinimumWidth(560)
        lay = QVBoxLayout(self)
        h = QLabel(_("⬆ Güncelleme denetimi"))
        h.setObjectName("h2")
        lay.addWidget(h)
        info = QLabel(_("Program her açıldığında yeni sürüm denetlenir."))
        info.setWordWrap(True)
        lay.addWidget(info)
        self.c_notify = QCheckBox(_("Yeni sürüm bulununca bildirim göster"))
        self.c_notify.setChecked(cfg["notify"])
        lay.addWidget(self.c_notify)
        # --- kullanım limitleri (kendi Firebase hesabının günlük sınırı)
        lay.addWidget(kullanim_sayac.KullanimKarti(self))
        # --- Asistan Agent (admin iletişimin önünde)
        if AJAN is not None:
            lay.addWidget(AJAN.card(self))
        # --- admin ile iletişim (ayarların sonu)
        h2 = QLabel(_("✉ Admin ile iletişime geç"))
        h2.setObjectName("h2")
        lay.addWidget(h2)
        cinfo = QLabel(_("Programı geliştirmemiz için öneri, istek ve hata bildirimlerinizi yazın; "
                         "mesajınız doğrudan yöneticiye ulaşır."))
        cinfo.setWordWrap(True)
        lay.addWidget(cinfo)
        self.c_name = QLineEdit()
        self.c_name.setPlaceholderText(_("Adınız (isteğe bağlı)"))
        self.c_name.setMaxLength(80)
        self.c_mail = QLineEdit()
        self.c_mail.setPlaceholderText(_("E-posta (yanıt için, isteğe bağlı)"))
        self.c_mail.setMaxLength(120)
        self.c_mail.setLayoutDirection(Qt.LeftToRight)
        row = QHBoxLayout()
        row.addWidget(self.c_name)
        row.addWidget(self.c_mail)
        lay.addLayout(row)
        self.c_msg = QTextEdit()
        self.c_msg.setPlaceholderText(_("Mesajınız"))
        self.c_msg.setAcceptRichText(False)
        self.c_msg.setMinimumHeight(110)
        lay.addWidget(self.c_msg)
        crow = QHBoxLayout()
        crow.addStretch()
        self.c_send = QPushButton(_("✉ Gönder"))
        self.c_send.clicked.connect(self.send_contact)
        crow.addWidget(self.c_send)
        lay.addLayout(crow)
        bb = QHBoxLayout()
        cancel = QPushButton(_("Vazgeç"))
        cancel.clicked.connect(self.reject)
        ok = QPushButton(_("Kaydet"))
        ok.clicked.connect(self.save)
        bb.addStretch()
        bb.addWidget(cancel)
        bb.addWidget(ok)
        lay.addLayout(bb)

    def save(self):
        self.result_cfg = {"notify": self.c_notify.isChecked()}
        self.accept()

    def send_contact(self):
        import base64 as _b64
        import json as _json
        import re as _re
        import urllib.request as _ur
        msg = self.c_msg.toPlainText().strip()[:5000]
        mail = self.c_mail.text().strip()
        if not msg:
            QMessageBox.information(self, _("✉ Admin ile iletişime geç"), _("Lütfen mesajınızı yazın."))
            return
        if mail and not _re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", mail):
            QMessageBox.information(self, _("✉ Admin ile iletişime geç"), _("E-posta adresi geçerli değil."))
            return
        to = _b64.b64decode("bW9jLmxpYW1ub3RvcnBANDMyMWxkaW50bWxkYmE=").decode()[::-1]
        body = {"_subject": "Bereket Defter: yeni mesaj", "_template": "table", "_captcha": "false",
                "Ad": self.c_name.text().strip() or "-", "Mesaj": msg, "Surum": APP_VERSION, "Cihaz": "Windows",
                "Dil": i18n._lang}
        if mail:
            body["email"] = mail
            body["_replyto"] = mail
        self.c_send.setEnabled(False)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # v1.17: iki bağımsız kanal; biri kabul ederse mesaj ulaşmış sayılır.
        # 1) Yöneticinin mesaj kutusu (Firestore "mesajlar", yalnızca yeni kayıt eklenebilir, kimse okuyamaz)
        # 2) E-posta kopyası (FormSubmit: Referer'sız isteği reddeder; etkinleştirilmiş site Referer olarak gönderilir)
        def _post(url, payload, extra):
            hdr = {"Content-Type": "application/json", "Accept": "application/json",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BereketDefter/" + APP_VERSION}
            hdr.update(extra)
            req = _ur.Request(url, data=_json.dumps(payload).encode("utf-8"), headers=hdr, method="POST")
            with _ur.urlopen(req, timeout=20) as r:
                return r.status, _json.loads(r.read().decode("utf-8") or "{}")
        ok = False
        try:
            F = lambda v: {"stringValue": str(v)[:4000]}
            fields = {"mesaj": F(msg), "konu": F("Bereket Defter · Mesaj"), "dil": F(i18n._lang), "surum": F(APP_VERSION),
                      "platform": F("Bereket Defter · Windows"),
                      "zaman": {"timestampValue": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}}
            if self.c_name.text().strip():
                fields["ad"] = F(self.c_name.text().strip()[:100])
            if mail:
                fields["iletisim"] = F(mail)
            st, _j = _post("https://firestore.googleapis.com/v1/projects/comm-calc-103111111/databases/(default)/documents/"
                           "mesajlar?key=AIzaSyB12RFS6ENPpmnnPsETfjedNH-3hmNWQvA", {"fields": fields}, {})
            ok = 200 <= st < 300
        except Exception:
            pass
        try:
            st, j = _post("https://formsubmit.co/ajax/" + to, body,
                          {"Referer": "https://formsubmit.co/", "Origin": "https://formsubmit.co"})
            ok = ok or str(j.get("success")).lower() == "true"
        except Exception:
            pass
        QApplication.restoreOverrideCursor()
        self.c_send.setEnabled(True)
        if ok:
            self.c_msg.clear()
            QMessageBox.information(self, _("✉ Admin ile iletişime geç"),
                                    _("Mesajınız yöneticiye iletildi. Teşekkürler!"))
        else:
            QMessageBox.warning(self, _("✉ Admin ile iletişime geç"),
                                _("Mesaj gönderilemedi. İnternet bağlantınızı kontrol edip tekrar deneyin."))


# ---------------------------------------------------------------- ana pencere
class MainWindow(QWidget):
    ALL = -1

    def __init__(self, db, first_start=True):
        super().__init__()
        self.db = db
        self.setWindowTitle(f"{_(APP_TITLE)}  v{APP_VERSION}")
        self.setWindowIcon(QIcon(logo_pixmap(128)))
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.bg = Background()
        outer.addWidget(self.bg)
        root = QVBoxLayout(self.bg)
        root.setContentsMargins(24, 16, 24, 20)
        root.setSpacing(14)

        # --- başlık
        head = QHBoxLayout()
        lg = QLabel()
        lg.setPixmap(logo_pixmap(96))
        head.addWidget(lg)
        tbox = QVBoxLayout()
        t = QLabel(f'{html.escape(_(APP_TITLE))} <span style="font-size:15px;font-weight:600;color:#cfeee4">'
                   f'v{APP_VERSION}</span>')
        t.setObjectName("title")
        self.quote_i = random.randrange(len(QUOTES))
        self.quote = QLabel(QUOTES[self.quote_i])
        self.quote.setObjectName("quote")
        self.quote.setWordWrap(True)
        t.setWordWrap(True)
        for lbl in (t, self.quote):
            lbl.setMinimumWidth(200)
            lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        tbox.addWidget(t)
        tbox.addWidget(self.quote)
        head.addLayout(tbox, 1)
        rbox = QVBoxLayout()
        self.clock = QLabel()
        self.clock.setObjectName("clock")
        self.clock.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        crow = QHBoxLayout()
        rbox.addLayout(crow)
        brow = QHBoxLayout()
        self.rem_btn = QPushButton()
        self.rem_btn.setObjectName("light")
        self.rem_btn.clicked.connect(lambda: self.open_reminders())
        for text, fn, name in ((_("Tüm Kayıtlar Dökümü"), lambda: StatementDialog(self, self.db, None).exec(), "light"),
                               (_("Yedek Al"), self.backup, "light"),
                               (_("☁ Eşitleme"), self.open_sync, "light"),
                               (_("⚙ Ayarlar"), self.open_settings, "light"),
                               (_("Tam Ekran (F11)"), self.toggle_full, "light"),
                               (_("Çıkış"), self.close, "danger")):
            b = QPushButton(text)
            b.setObjectName(name)
            b.clicked.connect(fn)
            brow.addWidget(b)
        self.lang_box = QComboBox()
        self.lang_box.setMinimumWidth(140)
        for code, label in i18n.LANGS.items():
            self.lang_box.addItem("🌐 " + label, code)
        self.lang_box.setCurrentIndex(list(i18n.LANGS).index(i18n.lang()))
        self.lang_box.currentIndexChanged.connect(self.change_language)
        crow.addWidget(self.lang_box)
        crow.addWidget(self.rem_btn)
        crow.addStretch()
        crow.addWidget(self.clock)
        crow.addSpacing(10)
        # sağ üst köşe: ☁ Eşitle + ⬆ Güncelleme (her zaman görünür)
        self.sync_ind = QPushButton(_("☁ Eşitle"))
        self.sync_ind.setObjectName("light")
        self.sync_ind.setStyleSheet("padding:6px 12px;")
        self.sync_ind.setCursor(Qt.PointingHandCursor)
        self.sync_ind.clicked.connect(self.sync_button_clicked)
        self.sync_ind.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sync_ind.customContextMenuRequested.connect(lambda *_a: self.open_sync())
        crow.addWidget(self.sync_ind)
        self.upd_btn = QPushButton(_("⬆ Güncelleme"))
        self.upd_btn.setObjectName("light")
        self.upd_btn.setStyleSheet("padding:6px 12px;")
        self.upd_btn.setCursor(Qt.PointingHandCursor)
        self.upd_btn.clicked.connect(self.open_update)
        crow.addWidget(self.upd_btn)
        # admin duyuruları (🔔)
        self.duyuru = duyuru_istemci.DuyuruIstemci(self, "bereket-defter", APP_VERSION, dil=i18n.lang, guncelle=self.open_update)
        crow.addWidget(self.duyuru.dugme)
        # pencere düğmeleri: küçült, yarım/tam ekran, kapat (tam ekranda Windows başlığı görünmediği için)
        crow.addSpacing(6)
        for txt, tip, fn in (("—", _("Küçült"), self.showMinimized),
                             ("❐", _("Yarım ekran / Tam ekran"), self.toggle_half),
                             ("✕", _("Kapat"), self.close)):
            b = QPushButton(txt)
            b.setObjectName("light")
            b.setToolTip(tip)
            b.setFixedSize(38, 32)
            b.setStyleSheet("padding:0; font-size:15px; font-weight:700;")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(fn)
            crow.addWidget(b)
        rbox.addLayout(brow)
        head.addLayout(rbox)
        root.addLayout(head)
        self.banner = QLabel()
        self.banner.setWordWrap(True)
        self.banner.setStyleSheet("background:#ffd24a;color:#2b1d00;font-size:17px;font-weight:700;"
                                  "padding:10px 16px;border-radius:12px;")
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
        self.plist = QListWidget()
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
                (_("📄 Döküm Al"), self.statement, "gold"))
        for i, (text, fn, name) in enumerate(acts):
            b = QPushButton(text)
            if name:
                b.setObjectName(name)
            b.clicked.connect(fn)
            tb.addWidget(b, i // 4, i % 4)
        rl.addLayout(tb)
        body.addWidget(right, 1)
        root.addLayout(body, 1)

        for seq, fn in ((QKeySequence("F11"), self.toggle_full), (QKeySequence("Ctrl+N"), lambda: self.add_tx("VERDIM"))):
            a = QAction(self)
            a.setShortcut(seq)
            a.triggered.connect(fn)
            self.addAction(a)

        self.timer = QTimer(self, interval=1000, timeout=self.tick)
        self.timer.start()
        self.qtimer = QTimer(self, interval=10000, timeout=self.next_quote)
        self.qtimer.start()
        self.tick()
        self.load_persons()
        self.setup_sync()
        self.setup_update()

        # hatırlatıcı bildirimleri
        if not hasattr(db, "notified"):
            db.notified = set()
        self.tray = QSystemTrayIcon(QIcon(logo_pixmap(64)), self)
        self.tray.setToolTip(_(APP_TITLE))
        self.tray.activated.connect(lambda *_a: self.open_reminders())
        self.tray_target = "reminder"
        self.tray.messageClicked.connect(self.tray_message_clicked)
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
        kullanim_sayac.baslat(self.db.dir, dil=i18n.lang, bulut=True, ai=False,
                              proje=lambda: (self.sync.cfg.get("projectId") if getattr(self, "sync", None) and self.sync.cfg.get("uid") else ""))
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
        s = self.sync
        tip = _("Tıklayın: şimdi eşitle · Sağ tık: eşitleme ayarları")
        if not s.signed_in():
            label, err = _("☁ Eşitle"), False
            text = _("Eşitleme kapalı (giriş yapılmamış)")
        else:
            text, err = sync_status_text(s)
            if s.busy:
                label = _("☁ ⟳ Eşitleniyor…")
            elif err:
                label = _("☁ ! Eşitle")
            else:
                last = s.cfg.get("lastSync") or ""
                label = _("☁ Eşitle") + (" ✓ " + last[11:16] if last else "")
        self.sync_ind.setText(label)
        self.sync_ind.setToolTip(text + "\n" + tip)
        name = "gold" if err else "light"
        if self.sync_ind.objectName() != name:
            self.sync_ind.setObjectName(name)
            self.sync_ind.style().unpolish(self.sync_ind)
            self.sync_ind.style().polish(self.sync_ind)

    def setup_update(self):
        first = not hasattr(self.db, "updater")
        if first:  # dil değişince pencere yeniden kurulur; denetleyici, ayarlar ve bildirilenler aynı kalır
            self.db.updater = guncelle.Updater(lambda: self.sync.cfg, APP_VERSION)
            self.db.upd_cfg = guncelle.load_settings(self.db.dir)
            self.db.upd_notified = set()
        self.updater = self.db.updater
        self.upd_seen = self.updater.seq
        self.upd_popup_wanted = False
        self.upd_poll = QTimer(self, interval=500, timeout=self.poll_update)
        self.upd_poll.start()
        if first:  # yalnızca program açılışında denetlenir
            QTimer.singleShot(2500, lambda: self.updater.check_async(quiet=True))
        self.update_update_button()

    def open_settings(self):
        d = SettingsDialog(self, self.db.upd_cfg)
        if d.exec():
            try:
                self.db.upd_cfg = guncelle.save_settings(self.db.dir, d.result_cfg)
            except OSError as e:
                self.db.upd_cfg = dict(d.result_cfg)
                QMessageBox.warning(self, _("⚙ Ayarlar"), _("Ayarlar kaydedilemedi: {}").format(e))

    def poll_update(self):
        self.update_update_button()
        up = self.updater
        modal = QApplication.activeModalWidget()
        if up.seq != self.upd_seen:
            self.upd_seen = up.seq
            if up.state == "available":
                ver = str(up.info.get("surum"))
                if ver not in self.db.upd_notified:
                    self.db.upd_notified.add(ver)
                    if self.db.upd_cfg["notify"] and not isinstance(modal, UpdateDialog):
                        self.notify_update(ver)
        if self.upd_popup_wanted and modal is None and not getattr(self, "restarting", False):
            self.upd_popup_wanted = False
            if up.state == "available":
                self.show_update_popup()

    def notify_update(self, ver):
        """Yeni sürüm bulundu: sistem bildirimi + (açık pencere yoksa hemen, varsa kapanınca) soru penceresi."""
        text = _("Yeni sürüm hazır: {}").format("v" + ver)
        tray = getattr(self, "tray", None)
        if tray is not None and QSystemTrayIcon.isSystemTrayAvailable() and tray.supportsMessages():
            self.tray_target = "update"
            tray.showMessage(_("⬆ Güncelleme"), text + "\n" + _("Kurmak için tıklayın."), QIcon(logo_pixmap(64)), 15000)
        QApplication.beep()
        self.upd_popup_wanted = True

    def show_update_popup(self):
        info = self.updater.info or {}
        box = QMessageBox(self)
        box.setWindowTitle(_("⬆ Güncelleme"))
        box.setIcon(QMessageBox.Information)
        box.setText(_("Yeni sürüm hazır: {}").format("v" + str(info.get("surum"))) + "\n" +
                    _("Kullandığınız sürüm: {}").format("v" + APP_VERSION))
        notes = str(info.get("notlar") or "").strip()
        box.setInformativeText((notes + "\n\n" if notes else "") +
                               _("Güncelleme sadece program dosyalarını yeniler; kayıtlarınız, kişileriniz ve dekontlarınız "
                                 "olduğu gibi kalır."))
        go = box.addButton(_("⬆ Şimdi güncelle"), QMessageBox.AcceptRole)
        box.addButton(_("Sonra"), QMessageBox.RejectRole)
        box.exec()
        if box.clickedButton() is go:
            self.open_update(auto_install=True)

    def tray_message_clicked(self):
        if getattr(self, "tray_target", "") == "update":
            self.upd_popup_wanted = False
            self.open_update()
        else:
            self.open_reminders()

    def update_update_button(self):
        st = self.updater.state
        if st == "available":
            text, name = _("⬆ Yeni sürüm: {}").format("v" + str(self.updater.info.get("surum"))), "gold"
        elif st == "downloading":
            done, total = self.updater.progress
            pct = f" %{min(100, int(done * 100 / total))}" if total else ""
            text, name = _("⬆ Güncelleniyor…") + pct, "gold"
        elif st == "installed":
            text, name = _("⬆ Güncelleniyor…"), "gold"
        else:
            text, name = _("⬆ Güncelleme"), "light"
        if self.upd_btn.text() != text or self.upd_btn.objectName() != name:
            self.upd_btn.setText(text)
            self.upd_btn.setObjectName(name)
            self.upd_btn.style().unpolish(self.upd_btn)
            self.upd_btn.style().polish(self.upd_btn)

    def open_update(self, auto_install=False):
        self.upd_popup_wanted = False
        UpdateDialog(self, self.updater, auto_install).exec()
        self.update_update_button()

    def restart_after_update(self):
        try:
            guncelle.restart_program()
        except OSError as e:
            QMessageBox.information(self, _("⬆ Güncelleme"),
                                    _("Güncelleme kuruldu. Programı kapatıp yeniden açın.") + f"\n\n{e}")
        self.restarting = True
        QApplication.exit(0)

    def open_sync(self):
        self.sync_dlg = SyncDialog(self, self.sync)
        try:
            self.sync_dlg.exec()
        finally:
            self.sync_dlg = None
        self.update_sync_indicator()

    # --- yardımcılar
    def next_quote(self):
        self.quote_i = (self.quote_i + 1) % len(QUOTES)
        self.quote.setText(QUOTES[self.quote_i])

    def tick(self):
        n = datetime.now()
        self.clock.setText(f"{_(DAY_NAMES[n.weekday()])}, {n:%d.%m.%Y  %H:%M:%S}")

    def toggle_half(self):
        """Tam ekran ↔ ekranın yarısı (sol yarı) arasında geçiş."""
        if self.isFullScreen() or self.isMaximized():
            self.showNormal()
            g = self.screen().availableGeometry()
            self.setGeometry(g.x(), g.y(), g.width() // 2, g.height())
        else:
            self.showFullScreen()

    def toggle_full(self):
        self.showNormal() if self.isFullScreen() else self.showFullScreen()

    def change_language(self, i):
        code = self.lang_box.itemData(i)
        if code != i18n.lang():
            i18n.set_language(code)
            self.restarting = True
            QApplication.exit(RESTART)

    def closeEvent(self, e):
        if getattr(self, "restarting", False):
            e.accept()
            return
        if QMessageBox.question(self, _("Çıkış"), _("Programdan çıkmak istiyor musunuz?")) == QMessageBox.Yes:
            e.accept()
        else:
            e.ignore()

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
        for p in self.db.persons(self.search.text()):
            bal = self.db.balances(p["id"])
            parts = []
            for c in CURRENCIES:
                b = bal[c][2]
                if abs(b) >= 0.005:
                    parts.append(("+" if b > 0 else "") + money(b, c))
            it = QListWidgetItem(p["name"] + ("\n" + "  ".join(parts) if parts else "\n" + _("Hesap kapalı")))
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

    def add_person(self):
        d = PersonDialog(self)
        if d.exec():
            pid = self.db.add_person(*d.values())
            self.search.clear()
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
            self.load_persons()

    def delete_person(self):
        pid = self.current_pid()
        if pid in (None, self.ALL):
            return
        p = self.db.person(pid)
        n = self.db.tx_count(pid)
        msg = _("'{}' silinsin mi?").format(p['name'])
        if n:
            msg += "\n\n" + _("DİKKAT: Bu kişiye ait {} kayıt ve belgeleri de kalıcı olarak silinecek!").format(n)
        if QMessageBox.warning(self, _("Kişiyi sil"), msg, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.delete_person(pid)
            self.load_persons()

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
                        it.setForeground(QBrush(QColor("#d97a00")))
                        it.setToolTip(_("Bu kaydın dekontu / belgesi yok"))
                if j in (4, 5):
                    it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(i, j, it)
        self.table.setColumnHidden(1, pid not in (None, self.ALL))

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


RESTART = 1000


def apply_language(app):
    for t in getattr(app, "_translators", []):
        app.removeTranslator(t)
    app._translators = []
    t = QTranslator(app)
    if t.load(f"qtbase_{i18n.lang()}", QLibraryInfo.path(QLibraryInfo.TranslationsPath)):
        app.installTranslator(t)
        app._translators.append(t)
    app.setLayoutDirection(Qt.RightToLeft if i18n.is_rtl() else Qt.LeftToRight)
    app.setApplicationName(_(APP_TITLE))


def force_light_theme(app):
    """Windows koyu modda da yazılar siyah, arka planlar beyaz kalsın."""
    try:
        app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    except AttributeError:
        pass
    app.setStyle("Fusion")
    pal = QPalette()
    black, white = QColor("#111111"), QColor("#ffffff")
    for grp in (QPalette.Active, QPalette.Inactive):
        pal.setColor(grp, QPalette.Window, QColor("#f4f6f5"))
        pal.setColor(grp, QPalette.WindowText, black)
        pal.setColor(grp, QPalette.Base, white)
        pal.setColor(grp, QPalette.AlternateBase, QColor("#f4faf8"))
        pal.setColor(grp, QPalette.Text, black)
        pal.setColor(grp, QPalette.Button, QColor("#eef2f1"))
        pal.setColor(grp, QPalette.ButtonText, black)
        pal.setColor(grp, QPalette.ToolTipBase, QColor("#fffbe6"))
        pal.setColor(grp, QPalette.ToolTipText, black)
        pal.setColor(grp, QPalette.PlaceholderText, QColor("#8a9590"))
        pal.setColor(grp, QPalette.Highlight, QColor("#0f8f6a"))
        pal.setColor(grp, QPalette.HighlightedText, white)
        pal.setColor(grp, QPalette.Link, QColor("#0b6e74"))
        pal.setColor(grp, QPalette.BrightText, QColor("#c0392b"))
    for role in (QPalette.WindowText, QPalette.Text, QPalette.ButtonText):
        pal.setColor(QPalette.Disabled, role, QColor("#8a9590"))
    pal.setColor(QPalette.Disabled, QPalette.Base, QColor("#f0f0f0"))
    app.setPalette(pal)


def main():
    if os.environ.pop("AV_YENIDEN_BASLAT", None):
        import time
        time.sleep(1.5)  # güncellemeden sonra eski pencerenin kapanmasını bekle
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    force_light_theme(app)
    i18n.load_language()
    apply_language(app)
    app.setStyleSheet(STYLE)
    app.setWindowIcon(QIcon(logo_pixmap(128)))

    global AJAN
    if fc_agent is not None:
        try:
            AJAN = fc_agent.Agent("bereket-defter", APP_VERSION, lang=lambda: i18n._lang, sync=True)
        except Exception:
            AJAN = None
    db = DB()
    first = True
    while True:
        w = MainWindow(db, first_start=first)
        w.showFullScreen()
        if AJAN is not None:
            try:
                AJAN.start(app, w) if first else AJAN.attach_button(w)
            except Exception:
                pass
        first = False
        code = app.exec()
        w.hide()
        w.deleteLater()
        if code != RESTART:
            return code
        apply_language(app)


if __name__ == "__main__":
    sys.exit(main())
