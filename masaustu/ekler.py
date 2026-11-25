"""v1.22 ekleri — masaüstü arayüzü (PySide6). Mantık: ekler_cekirdek.py · çeviriler: ekler_ceviri.py.

Güvenlik: PIN kilidi (açılışta + boşta kalınca; Ctrl+L), tutarları gizle (Ctrl+H), günlük otomatik yedek,
önizlemeli "yedekten eksikleri geri getir". Defter: taksit planı, mesaj / mutabakat (WhatsApp · Telegram · kopyala),
borç senedi (PDF / yazdır), etiketler, gecikenler. Raporlar sayfası: özet + kur karşılığı, yaşlandırma, en büyük bakiyeler,
aylık hareket grafiği, gecikenler, CSV dışa / içe aktarma. Hızlı kayıt (Ctrl+K, internetsiz ayrıştırıcı), geri al çubuğu."""
import os
import re
import urllib.parse
from datetime import datetime

from PySide6.QtCore import QDate, QDateTime, QEvent, QObject, QRectF, QSize, Qt, QTimer, QUrl
from PySide6.QtGui import QColor, QDesktopServices, QFont, QGuiApplication, QPainter, QPen, QTextDocument
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDialog,
                               QDialogButtonBox, QDoubleSpinBox, QFileDialog, QFormLayout, QFrame, QGridLayout, QHBoxLayout,
                               QHeaderView, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QPlainTextEdit,
                               QPushButton, QRadioButton, QScrollArea, QSizePolicy, QSpinBox, QTableWidget, QTableWidgetItem,
                               QTextBrowser, QVBoxLayout, QWidget, QAbstractItemView)

import i18n
from i18n import _
import ekler_ceviri  # noqa: F401  (çevirileri i18n.T'ye ekler)
import ekler_cekirdek as E

CURRENCIES = E.CURRENCIES
SYMBOLS = E.SYMBOLS
CUR_AD = {"USD": "Dolar ($)", "TRY": "Türk Lirası (₺)", "SYP": "Suriye Lirası (£S)"}
GIZLE = [False]          # main.money() bakar: tutarlar ekranda ••••• görünür
MASKE = "•••••"
DILLER = (("tr", "Türkçe"), ("en", "English"), ("ar", "العربية"))


def fmt(x):
    s = f"{abs(x):,.2f}"
    if i18n.lang() == "tr":
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if x < 0 else "") + s


def para(x, cur, gizli=None):
    if (GIZLE[0] if gizli is None else gizli):
        return f"{MASKE} {SYMBOLS.get(cur, cur)}"
    return f"{fmt(x)} {SYMBOLS.get(cur, cur)}"


class gizlemeden:
    """Döküm / senet / mesaj gibi çıktılarda tutarlar her zaman açık yazılır."""

    def __enter__(self):
        self.eski = GIZLE[0]
        GIZLE[0] = False

    def __exit__(self, *a):
        GIZLE[0] = self.eski


def _btn(text, slot, name=None):
    b = QPushButton(text)
    if name:
        b.setObjectName(name)
    b.clicked.connect(slot)
    return b


def _kisiler_combo(db, pid=None, bos=False):
    c = QComboBox()
    if bos:
        c.addItem("—", None)
    for p in db.persons():
        c.addItem(p["name"], p["id"])
    if pid is not None:
        i = c.findData(pid)
        if i >= 0:
            c.setCurrentIndex(i)
    return c


def _cur_combo(cur=None):
    c = QComboBox()
    for k in CURRENCIES:
        c.addItem(_(CUR_AD[k]), k)
    if cur:
        c.setCurrentIndex(max(c.findData(cur), 0))
    return c


def _dil_combo():
    c = QComboBox()
    for k, ad in DILLER:
        c.addItem(ad, k)
    c.setCurrentIndex(max(c.findData(i18n.lang()), 0))
    return c


def bakiyeler(db, pid):
    return {c: b[2] for c, b in db.balances(pid).items()}


# ================================================================ güvenlik
class Guvenlik(QObject):
    """Tek nesne (db.guvenlik): ayarlar, PIN kilidi, boşta kalma sayacı, otomatik yedek."""

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.a = E.ayar_oku(db.dir)
        GIZLE[0] = bool(self.a.get("gizle"))
        self.win = None
        self.perde = None
        self.son = datetime.now()
        self.gizli_diyaloglar = []
        self.yanlis = 0
        self.bekle_bitis = None
        QApplication.instance().installEventFilter(self)
        self.t = QTimer(self, interval=15000, timeout=self._bosta_mi)
        self.t.start()

    def kaydet(self):
        E.ayar_yaz(self.db.dir, self.a)

    # --- etkinlik izleme
    def eventFilter(self, obj, ev):
        if ev.type() in (QEvent.KeyPress, QEvent.MouseButtonPress, QEvent.Wheel, QEvent.MouseMove):
            self.son = datetime.now()
        return False

    def _bosta_mi(self):
        dk = int(self.a.get("kilit_dk") or 0)
        if self.pin_var() and dk > 0 and not self.kilitli() and (datetime.now() - self.son).total_seconds() >= dk * 60:
            self.kilitle()

    # --- PIN
    def pin_var(self):
        return bool(self.a.get("pin"))

    def pin_ayarla(self, pin):
        self.a["pin"] = E.pin_kaydi(pin) if pin else None
        self.kaydet()

    def kilitli(self):
        return self.perde is not None and self.perde.isVisible()

    def kilitle(self):
        if not self.pin_var() or self.win is None or self.kilitli():
            return
        self.gizli_diyaloglar = [w for w in QApplication.topLevelWidgets() if isinstance(w, QDialog) and w.isVisible()]
        for w in self.gizli_diyaloglar:
            w.hide()
        if self.perde is None:
            self.perde = KilitPerdesi(self.win, self)
        self.perde.goster()

    def ac(self):
        self.perde.hide()
        self.son = datetime.now()
        for w in self.gizli_diyaloglar:
            try:
                w.show()
            except RuntimeError:
                pass
        self.gizli_diyaloglar = []

    # --- otomatik yedek
    def oto_yedek(self):
        if not self.a.get("oto_yedek", True):
            return None
        try:
            return E.oto_yedek(self.db, int(self.a.get("yedek_sakla") or 10))
        except Exception as e:  # pragma: no cover — yedek alınamazsa program çalışmaya devam eder
            print("otomatik yedek alınamadı:", e)
            return None


class KilitPerdesi(QWidget):
    """Pencerenin tamamını kaplayan PIN ekranı."""

    def __init__(self, win, g):
        super().__init__(win)
        self.g = g
        self.setObjectName("kilitPerdesi")
        self.setAttribute(Qt.WA_StyledBackground, True)
        from fccore import style as fcstyle
        bg = fcstyle.scheme_tokens().get("bg", "#0b1220")
        self.setStyleSheet("#kilitPerdesi { background: %s; }" % (bg[:7] if str(bg).startswith("#") else "palette(window)"))
        v = QVBoxLayout(self)
        v.addStretch(2)
        kutu = QFrame()
        kutu.setObjectName("card")
        kutu.setFixedWidth(360)
        k = QVBoxLayout(kutu)
        k.setContentsMargins(26, 24, 26, 24)
        k.setSpacing(12)
        bas = QLabel("🔒 " + _("Bereket Alacak-Verecek Defteri"))
        bas.setObjectName("h2")
        bas.setWordWrap(True)
        bas.setAlignment(Qt.AlignCenter)
        k.addWidget(bas)
        alt = QLabel(_("Devam etmek için PIN kodunuzu girin."))
        alt.setAlignment(Qt.AlignCenter)
        alt.setWordWrap(True)
        k.addWidget(alt)
        self.pin = QLineEdit()
        self.pin.setEchoMode(QLineEdit.Password)
        self.pin.setMaxLength(8)
        self.pin.setAlignment(Qt.AlignCenter)
        self.pin.setPlaceholderText("••••")
        f = self.pin.font()
        f.setPointSize(f.pointSize() + 6)
        self.pin.setFont(f)
        self.pin.returnPressed.connect(self.dene)
        k.addWidget(self.pin)
        self.msg = QLabel(" ")
        self.msg.setAlignment(Qt.AlignCenter)
        self.msg.setWordWrap(True)
        self.msg.setObjectName("muted")
        k.addWidget(self.msg)
        k.addWidget(_btn(_("Kilidi aç"), self.dene, "primary"))
        unut = QPushButton(_("PIN'i unuttum"))
        unut.setFlat(True)
        unut.clicked.connect(self.unuttum)
        k.addWidget(unut)
        h = QHBoxLayout()
        h.addStretch(1)
        h.addWidget(kutu)
        h.addStretch(1)
        v.addLayout(h)
        v.addStretch(3)
        win.installEventFilter(self)
        self.hide()

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.Resize and self.isVisible():
            self.setGeometry(self.parentWidget().rect())
        return False

    def goster(self):
        self.setGeometry(self.parentWidget().rect())
        self.pin.clear()
        self.msg.setText(" ")
        self.show()
        self.raise_()
        self.pin.setFocus()

    def dene(self):
        g = self.g
        if g.bekle_bitis and datetime.now() < g.bekle_bitis:
            self.msg.setText(_("Çok fazla hatalı deneme. {} saniye sonra tekrar deneyin.").format(
                int((g.bekle_bitis - datetime.now()).total_seconds()) + 1))
            return
        if E.pin_dogru(g.a.get("pin"), self.pin.text().strip()):
            g.yanlis = 0
            g.ac()
            return
        g.yanlis += 1
        self.pin.clear()
        if g.yanlis >= 5:
            g.yanlis = 0
            from datetime import timedelta
            g.bekle_bitis = datetime.now() + timedelta(seconds=30)
            self.msg.setText(_("Çok fazla hatalı deneme. {} saniye sonra tekrar deneyin.").format(30))
        else:
            self.msg.setText(_("PIN yanlış."))

    def unuttum(self):
        QMessageBox.information(self, _("PIN'i unuttum"), _(
            "Güvenliğiniz için PIN buradan sıfırlanamaz. Programı kapatın, veri klasöründeki “guvenlik.json” dosyasını silin ve "
            "programı yeniden açın; kayıtlarınız silinmez.\n\nVeri klasörü:\n{}").format(self.g.db.dir))


def guvenlik_karti(shell, db, W, yenile):
    """Ayarlar → Güvenlik ve yedek kartı."""
    g = db.guvenlik
    c = W.Card("bereket-guvenlik", _("Güvenlik ve otomatik yedek"), "key",
               _("PIN kilidi, tutarları gizleme ve her gün kendiliğinden alınan yedekler. Bu ayarlar yalnız bu bilgisayarda geçerlidir."))
    durum = W.label(_("PIN kilidi: açık") if g.pin_var() else _("PIN kilidi: kapalı"), "muted")
    c.add(durum)

    def pin_degistir():
        d = PinDialog(shell.defter or None, g)
        if d.exec():
            yenile()

    def pin_kaldir():
        d = PinDialog(shell.defter or None, g, kaldir=True)
        if d.exec():
            yenile()
    satir = [W.button(_("PIN belirle / değiştir"), "btn small primary", icon="key", slot=pin_degistir)]
    if g.pin_var():
        satir.append(W.button(_("PIN'i kaldır"), "btn small", slot=pin_kaldir))
        satir.append(W.button(_("Şimdi kilitle"), "btn small", slot=lambda: g.kilitle()))
    c.add(W.hbox(*satir, stretch_end=True), top=8)
    dk = QComboBox()
    for v, ad in ((0, _("Kendiliğinden kilitleme")), (1, _("1 dakika boşta kalınca")), (5, _("5 dakika boşta kalınca")),
                  (15, _("15 dakika boşta kalınca")), (30, _("30 dakika boşta kalınca"))):
        dk.addItem(ad, v)
    dk.setCurrentIndex(max(dk.findData(int(g.a.get("kilit_dk") or 0)), 0))

    def dk_degisti(_i):
        g.a["kilit_dk"] = dk.currentData()
        g.kaydet()
    dk.currentIndexChanged.connect(dk_degisti)
    dk.setEnabled(g.pin_var())
    c.add(dk, top=8)
    gz = QCheckBox(_("Tutarları gizle (ekranda ••••• görünür; Ctrl+H)"))
    gz.setChecked(GIZLE[0])
    gz.toggled.connect(lambda on: shell.defter and shell.defter.gizle_degistir(on))
    c.add(gz, top=8)
    oy = QCheckBox(_("Her gün otomatik yedek al"))
    oy.setChecked(bool(g.a.get("oto_yedek", True)))

    def oy_degisti(on):
        g.a["oto_yedek"] = bool(on)
        g.kaydet()
        if on:
            g.oto_yedek()
    oy.toggled.connect(oy_degisti)
    c.add(oy, top=6)
    son = E.yedekler(db.dir)
    c.add(W.label(_("Son yedek: {}").format(son[0][3].strftime("%d.%m.%Y %H:%M")) if son else _("Henüz yedek yok."), "muted"), top=4)
    c.add(W.hbox(W.button(_("Yedekleri gör / geri getir"), "btn small", icon="box", slot=lambda: YedekDialog(shell.defter, db).exec()),
                 W.button(_("Yedek klasörünü aç"), "btn small", icon="ext",
                          slot=lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(E.yedek_klasoru(db.dir)))),
                 stretch_end=True), top=8)
    ben = QLineEdit(g.a.get("ben") or "")
    ben.setPlaceholderText(_("Mesajların ve senetlerin altına yazılacak adınız"))

    def ben_kaydet():
        g.a["ben"] = ben.text().strip()
        g.kaydet()
    ben.editingFinished.connect(ben_kaydet)
    c.add(W.field(_("Adınız"), ben), top=4)
    return c


def kisayol_karti(W):
    c = W.Card("bereket-kisayol", _("Klavye kısayolları"), "type", None)
    satirlar = (("Ctrl+N", _("Yeni kayıt: Verdim")), ("Ctrl+Shift+N", _("Yeni kayıt: Aldım")), ("Ctrl+K", _("Hızlı kayıt")),
                ("Ctrl+F", _("Kişi ara")), ("Ctrl+P", _("Döküm al")), ("Ctrl+R", _("Raporlar")), ("Ctrl+M", _("Mesaj / mutabakat")),
                ("Ctrl+H", _("Tutarları gizle / göster")), ("Ctrl+L", _("Kilitle")), ("F5", _("Eşitle")), ("Delete", _("Seçili kaydı sil")))
    g = QGridLayout()
    g.setHorizontalSpacing(16)
    for i, (k, ad) in enumerate(satirlar):
        a = QLabel(f"<b>{k}</b>")
        a.setTextFormat(Qt.RichText)
        g.addWidget(a, i, 0)
        g.addWidget(QLabel(ad), i, 1)
    w = QWidget()
    w.setLayout(g)
    c.add(w)
    return c


class PinDialog(QDialog):
    def __init__(self, parent, g, kaldir=False):
        super().__init__(parent)
        self.g = g
        self.kaldir = kaldir
        self.setWindowTitle(_("PIN'i kaldır") if kaldir else _("PIN belirle / değiştir"))
        self.setMinimumWidth(380)
        f = QFormLayout(self)
        self.eski = QLineEdit()
        self.yeni = QLineEdit()
        self.yeni2 = QLineEdit()
        for e in (self.eski, self.yeni, self.yeni2):
            e.setEchoMode(QLineEdit.Password)
            e.setMaxLength(8)
        if g.pin_var():
            f.addRow(_("Şu anki PIN"), self.eski)
        if not kaldir:
            f.addRow(_("Yeni PIN (4–8 rakam)"), self.yeni)
            f.addRow(_("Yeni PIN (tekrar)"), self.yeni2)
            not_ = QLabel(_("PIN bu bilgisayarda saklanır ve eşitlenmez. Telefonda ayrı PIN belirleyebilirsiniz."))
            not_.setWordWrap(True)
            not_.setObjectName("muted")
            f.addRow(not_)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.button(QDialogButtonBox.Ok).setText(_("Kaydet"))
        bb.button(QDialogButtonBox.Cancel).setText(_("Vazgeç"))
        bb.accepted.connect(self.tamam)
        bb.rejected.connect(self.reject)
        f.addRow(bb)

    def tamam(self):
        if self.g.pin_var() and not E.pin_dogru(self.g.a.get("pin"), self.eski.text().strip()):
            QMessageBox.warning(self, _("PIN"), _("Şu anki PIN yanlış."))
            return
        if self.kaldir:
            self.g.pin_ayarla(None)
        else:
            p = self.yeni.text().strip()
            if not E.pin_gecerli(p):
                QMessageBox.warning(self, _("PIN"), _("PIN 4–8 rakamdan oluşmalı."))
                return
            if p != self.yeni2.text().strip():
                QMessageBox.warning(self, _("PIN"), _("İki PIN aynı değil."))
                return
            self.g.pin_ayarla(p)
        self.accept()


class YedekDialog(QDialog):
    """Yedekleri listeler; seçilen yedeğin içeriğini ve bu cihazda eksik olanları gösterir; eksikleri geri getirir."""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle(_("Yedekler ve geri getirme"))
        self.resize(720, 480)
        v = QVBoxLayout(self)
        acik = QLabel(_("Bir yedek seçin: içinde ne olduğu ve bu cihazda eksik olanlar görünür. “Eksikleri geri getir” yalnız eksik "
                        "kayıtları ekler; mevcut kayıtlarınıza dokunmaz, hiçbir şeyi silmez."))
        acik.setWordWrap(True)
        v.addWidget(acik)
        h = QHBoxLayout()
        self.liste = QListWidget()
        self.liste.currentItemChanged.connect(lambda *_a: self.ozet())
        h.addWidget(self.liste, 1)
        self.bilgi = QLabel()
        self.bilgi.setWordWrap(True)
        self.bilgi.setAlignment(Qt.AlignTop)
        self.bilgi.setMinimumWidth(300)
        h.addWidget(self.bilgi, 1)
        v.addLayout(h, 1)
        b = QHBoxLayout()
        b.addWidget(_btn(_("Başka bir yedek dosyası seç…"), self.dosya))
        b.addWidget(_btn(_("Şimdi yedek al"), self.simdi))
        b.addStretch(1)
        self.geri = _btn(_("Eksikleri geri getir"), self.getir, "primary")
        b.addWidget(self.geri)
        b.addWidget(_btn(_("Kapat"), self.reject))
        v.addLayout(b)
        self.doldur()

    def doldur(self, sec=None):
        self.liste.clear()
        for yol, ad, boyut, zaman in E.yedekler(self.db.dir):
            it = QListWidgetItem(f"{zaman:%d.%m.%Y %H:%M}  ·  {ad}  ·  {boyut / 1024 / 1024:.1f} MB")
            it.setData(Qt.UserRole, yol)
            self.liste.addItem(it)
            if sec and os.path.normcase(sec) == os.path.normcase(yol):
                self.liste.setCurrentItem(it)
        if self.liste.currentItem() is None and self.liste.count():
            self.liste.setCurrentRow(0)
        if not self.liste.count():
            self.bilgi.setText(_("Henüz yedek yok."))
            self.geri.setEnabled(False)

    def secili(self):
        it = self.liste.currentItem()
        return it.data(Qt.UserRole) if it else getattr(self, "_dis", None)

    def ozet(self, yol=None):
        yol = yol or self.secili()
        if not yol:
            return
        try:
            o = E.yedek_ozet(self.db, yol)
        except Exception:
            self.bilgi.setText(_("Bu dosya geçerli bir yedek değil."))
            self.geri.setEnabled(False)
            return
        satir = [f"<b>{os.path.basename(yol)}</b>", ""]
        for k, ad in (("kisi", _("Kişi")), ("kayit", _("Kayıt")), ("hatirlatici", _("Hatırlatıcı")), ("belge", _("Belge"))):
            satir.append(_("{}: {} (bu cihazda eksik: {})").format(ad, o[k], o[k + "_eksik"]))
        eksik = sum(o[k] for k in o if k.endswith("_eksik"))
        satir += ["", _("Geri getirilecek bir şey yok; bu yedekteki her şey bu cihazda var.") if not eksik else
                  _("Bu yedekte olup bu cihazda olmayan {} öğe var.").format(eksik)]
        self.bilgi.setText("<br>".join(satir))
        self.geri.setEnabled(eksik > 0)
        self._yol = yol

    def dosya(self):
        yol, _f = QFileDialog.getOpenFileName(self, _("Yedek dosyası"), "", "ZIP (*.zip)")
        if yol:
            self.liste.clearSelection()
            self.liste.setCurrentItem(None)
            self._dis = yol
            self.ozet(yol)

    def simdi(self):
        yol = os.path.join(E.yedek_klasoru(self.db.dir), f"elle_{datetime.now():%Y-%m-%d_%H%M%S}.zip")
        self.db.backup(yol)
        self.doldur(sec=yol)

    def getir(self):
        yol = getattr(self, "_yol", None)
        if not yol:
            return
        if QMessageBox.question(self, _("Eksikleri geri getir"), _("Yedekte olup bu cihazda olmayan kayıtlar eklensin mi? "
                                                                    "Mevcut kayıtlarınız değişmez.")) != QMessageBox.Yes:
            return
        s = E.yedekten_eksikleri_getir(self.db, yol)
        QMessageBox.information(self, _("Eksikleri geri getir"), _("Geri getirildi: {} kişi, {} kayıt, {} hatırlatıcı, {} belge.").format(
            s["kisi"], s["kayit"], s["hatirlatici"], s["belge"]))
        p = self.parent()
        if p is not None and hasattr(p, "load_persons"):
            p.load_persons()
        self.ozet(yol)


# ================================================================ taksit planı
class TaksitDialog(QDialog):
    def __init__(self, parent, db, pid=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle(_("Taksit / ödeme planı"))
        self.setMinimumWidth(460)
        f = QFormLayout(self)
        acik = QLabel(_("Toplam tutarı eşit taksitlere böler ve her taksit için bir hatırlatıcı kurar. "
                        "Ödeme geldikçe “Aldım” / “Verdim” kaydını girip hatırlatıcıyı tamamlandı yapın."))
        acik.setWordWrap(True)
        acik.setObjectName("muted")
        f.addRow(acik)
        self.kisi = _kisiler_combo(db, pid)
        f.addRow(_("Kişi"), self.kisi)
        self.r_tahsil = QRadioButton(_("Tahsil edilecek (alınacak)"))
        self.r_odeme = QRadioButton(_("Ödenecek (verilecek)"))
        bal = bakiyeler(db, pid) if pid else {}
        (self.r_odeme if bal and min(bal.values()) < -0.005 and max(bal.values()) <= 0.005 else self.r_tahsil).setChecked(True)
        y = QVBoxLayout()
        y.addWidget(self.r_tahsil)
        y.addWidget(self.r_odeme)
        f.addRow(_("Tür"), y)
        self.cur = _cur_combo(next((c for c, b in bal.items() if abs(b) >= 0.005), None))
        f.addRow(_("Para birimi"), self.cur)
        self.toplam = QDoubleSpinBox()
        self.toplam.setRange(0, 1e12)
        self.toplam.setDecimals(2)
        self.toplam.setGroupSeparatorShown(True)
        b = next((abs(b) for c, b in bal.items() if abs(b) >= 0.005), 0)
        self.toplam.setValue(round(b, 2))
        f.addRow(_("Toplam tutar"), self.toplam)
        self.adet = QSpinBox()
        self.adet.setRange(2, 120)
        self.adet.setValue(6)
        f.addRow(_("Taksit sayısı"), self.adet)
        self.aralik = QComboBox()
        for k, ad in (("ay", _("Her ay")), ("15", _("15 günde bir")), ("hafta", _("Her hafta"))):
            self.aralik.addItem(ad, k)
        f.addRow(_("Sıklık"), self.aralik)
        self.ilk = QDateTimeEdit(QDateTime.currentDateTime().addMonths(1))
        self.ilk.setCalendarPopup(True)
        self.ilk.setDisplayFormat("dd.MM.yyyy HH:mm")
        f.addRow(_("İlk taksit"), self.ilk)
        self.notu = QLineEdit()
        f.addRow(_("Not"), self.notu)
        self.onizle = QLabel()
        self.onizle.setObjectName("hint")
        self.onizle.setWordWrap(True)
        f.addRow(self.onizle)
        for w in (self.toplam, self.adet):
            w.valueChanged.connect(self.guncelle)
        self.cur.currentIndexChanged.connect(self.guncelle)
        self.aralik.currentIndexChanged.connect(self.guncelle)
        self.ilk.dateTimeChanged.connect(self.guncelle)
        bb = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        bb.button(QDialogButtonBox.Save).setText(_("Planı kaydet"))
        bb.button(QDialogButtonBox.Cancel).setText(_("Vazgeç"))
        bb.accepted.connect(self.kaydet)
        bb.rejected.connect(self.reject)
        f.addRow(bb)
        self.guncelle()

    def plan(self):
        ilk = self.ilk.dateTime().toPython()
        return E.taksitler(self.toplam.value(), self.adet.value(), ilk, self.aralik.currentData())

    def guncelle(self, *_a):
        p = self.plan()
        cur = self.cur.currentData()
        with gizlemeden():
            ilk3 = "  ·  ".join(f"{datetime.strptime(d, '%Y-%m-%d %H:%M'):%d.%m.%Y}: {para(t, cur)}" for d, t in p[:3])
        self.onizle.setText(_("{} taksit × {}").format(len(p), para(p[0][1], cur, False)) + "\n" + ilk3 + ("  …" if len(p) > 3 else ""))

    def kaydet(self):
        pid = self.kisi.currentData()
        if pid is None:
            QMessageBox.warning(self, _("Eksik"), _("Önce bir kişi ekleyin."))
            return
        if self.toplam.value() <= 0:
            QMessageBox.warning(self, _("Eksik"), _("Toplam tutarı yazın."))
            return
        p = self.plan()
        tur = "ODEME" if self.r_odeme.isChecked() else "TAHSIL"
        for i, (due, tutar) in enumerate(p, start=1):
            notu = _("Taksit {}/{}").format(i, len(p)) + (" — " + self.notu.text().strip() if self.notu.text().strip() else "")
            self.db.add_reminder(pid, tur, self.cur.currentData(), tutar, due, notu)
        self.accept()


# ================================================================ mesaj / mutabakat
def _rakamlar(no):
    d = re.sub(r"\D", "", no or "")
    if (no or "").strip().startswith("00"):
        d = d[2:]
    return d


class MesajDialog(QDialog):
    def __init__(self, parent, db, pid):
        super().__init__(parent)
        self.db = db
        self.p = db.person(pid)
        self.pid = pid
        self.setWindowTitle(_("Mesaj / mutabakat") + " — " + self.p["name"])
        self.resize(620, 520)
        v = QVBoxLayout(self)
        ust = QHBoxLayout()
        self.tur = QComboBox()
        for k, ad in (("bakiye", _("Bakiye bildirimi ve mutabakat")), ("hatirlat", _("Kibar ödeme hatırlatması")),
                      ("kapandi", _("Hesap kapandı / teşekkür"))):
            self.tur.addItem(ad, k)
        bal = bakiyeler(db, pid)
        if not any(abs(b) >= 0.005 for b in bal.values()):
            self.tur.setCurrentIndex(2)
        elif any(b > 0.005 for b in bal.values()):
            self.tur.setCurrentIndex(0)
        self.dil = _dil_combo()
        ust.addWidget(QLabel(_("Mesaj")))
        ust.addWidget(self.tur, 1)
        ust.addWidget(QLabel(_("Dil")))
        ust.addWidget(self.dil)
        v.addLayout(ust)
        self.metin = QPlainTextEdit()
        v.addWidget(self.metin, 1)
        ip = QLabel(_("Metni dilediğiniz gibi düzeltebilirsiniz. Mutabakat mesajına karşı taraf “Onaylıyorum” diye cevap verirse "
                      "hesaplarınız uyuşuyor demektir."))
        ip.setWordWrap(True)
        ip.setObjectName("muted")
        v.addWidget(ip)
        b = QHBoxLayout()
        b.addWidget(_btn("WhatsApp", self.whatsapp, "primary"))
        b.addWidget(_btn("Telegram", self.telegram))
        b.addWidget(_btn(_("Kopyala"), self.kopyala))
        b.addStretch(1)
        b.addWidget(_btn(_("Kapat"), self.reject))
        v.addLayout(b)
        self.tur.currentIndexChanged.connect(self.yaz)
        self.dil.currentIndexChanged.connect(self.yaz)
        self.yaz()

    def yaz(self, *_a):
        ben = getattr(self.db, "guvenlik", None)
        ben = ben.a.get("ben", "") if ben else ""
        dil = self.dil.currentData()
        self.metin.setPlainText(E.mesaj_metni(self.tur.currentData(), dil, self.p["name"], bakiyeler(self.db, self.pid), ben))
        self.metin.document().setDefaultTextOption(self.metin.document().defaultTextOption())
        self.metin.setLayoutDirection(Qt.RightToLeft if dil == "ar" else Qt.LeftToRight)

    def kopyala(self):
        QGuiApplication.clipboard().setText(self.metin.toPlainText())
        from fccore.widgets import toast
        toast(_("Kopyalandı"), "ok", parent=self)

    def whatsapp(self):
        no = _rakamlar(self.p["wa_phone"] or self.p["phone"])
        q = urllib.parse.quote(self.metin.toPlainText())
        QDesktopServices.openUrl(QUrl(f"https://wa.me/{no}?text={q}" if no else f"https://wa.me/?text={q}"))

    def telegram(self):
        QGuiApplication.clipboard().setText(self.metin.toPlainText())
        u = (self.p["tg_user"] or "").strip()
        if u and (u.startswith("@") or re.search(r"[A-Za-z_]", u)):
            url = "https://t.me/" + u.lstrip("@")
        else:
            no = _rakamlar(u or self.p["phone"])
            url = f"https://t.me/+{no}" if no else "https://t.me/"
        QDesktopServices.openUrl(QUrl(url))
        QMessageBox.information(self, "Telegram", _("Mesaj panoya kopyalandı; Telegram'da sohbete yapıştırın (Ctrl+V)."))


# ================================================================ borç senedi
class SenetDialog(QDialog):
    def __init__(self, parent, db, pid=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle(_("Borç senedi"))
        self.setMinimumWidth(560)
        f = QFormLayout(self)
        acik = QLabel(_("Bakara 282'deki gibi: borç, vadesiyle birlikte yazılır; bir kâtip yazar ve iki şahit bulunur. "
                        "Senedi yazdırıp taraflara imzalatın."))
        acik.setWordWrap(True)
        acik.setObjectName("muted")
        f.addRow(acik)
        g = getattr(db, "guvenlik", None)
        ben = g.a.get("ben", "") if g else ""
        p = db.person(pid) if pid else None
        bal = bakiyeler(db, pid) if pid else {}
        c, b = next(((c, b) for c, b in bal.items() if abs(b) >= 0.005), ("USD", 0.0))
        self.borclu = QLineEdit((p["name"] if p else "") if b >= 0 else ben)
        self.alacakli = QLineEdit(ben if b >= 0 else (p["name"] if p else ""))
        degis = QPushButton("⇅")
        degis.setToolTip(_("Borçlu ile alacaklıyı yer değiştir"))
        degis.clicked.connect(lambda: (lambda a, b2: (self.borclu.setText(b2), self.alacakli.setText(a)))(self.borclu.text(), self.alacakli.text()))
        h = QHBoxLayout()
        h.addWidget(self.borclu, 1)
        h.addWidget(degis)
        f.addRow(_("Borçlu"), h)
        f.addRow(_("Alacaklı"), self.alacakli)
        self.tutar = QDoubleSpinBox()
        self.tutar.setRange(0, 1e12)
        self.tutar.setDecimals(2)
        self.tutar.setGroupSeparatorShown(True)
        self.tutar.setValue(round(abs(b), 2))
        self.cur = _cur_combo(c)
        h2 = QHBoxLayout()
        h2.addWidget(self.tutar, 1)
        h2.addWidget(self.cur)
        f.addRow(_("Tutar"), h2)
        self.yazi = QLineEdit()
        self.yazi.setPlaceholderText(_("ör. bin beş yüz dolar"))
        f.addRow(_("Yazıyla (isteğe bağlı)"), self.yazi)
        self.tarih = QDateEdit(QDate.currentDate())
        self.vade = QDateEdit(QDate.currentDate().addMonths(1))
        for d in (self.tarih, self.vade):
            d.setCalendarPopup(True)
            d.setDisplayFormat("dd.MM.yyyy")
        f.addRow(_("Düzenlenme tarihi"), self.tarih)
        f.addRow(_("Vade"), self.vade)
        self.yer = QLineEdit()
        self.yer.setPlaceholderText(_("ör. elden nakit, banka havalesi"))
        f.addRow(_("Ödeme şekli (isteğe bağlı)"), self.yer)
        self.katip = QLineEdit()
        self.s1 = QLineEdit()
        self.s2 = QLineEdit()
        f.addRow(_("Yazan (kâtip)"), self.katip)
        f.addRow(_("1. şahit"), self.s1)
        f.addRow(_("2. şahit"), self.s2)
        self.aciklama = QLineEdit()
        f.addRow(_("Açıklama"), self.aciklama)
        self.dil = _dil_combo()
        f.addRow(_("Senedin dili"), self.dil)
        b3 = QHBoxLayout()
        b3.addWidget(_btn(_("Önizle"), self.onizle))
        b3.addWidget(_btn(_("PDF kaydet"), self.pdf, "gold"))
        b3.addWidget(_btn(_("Yazdır"), self.yazdir))
        b3.addStretch(1)
        b3.addWidget(_btn(_("Kapat"), self.reject))
        f.addRow(b3)

    def html(self):
        return E.senet_html({"borclu": self.borclu.text().strip(), "alacakli": self.alacakli.text().strip(),
                             "tutar": self.tutar.value(), "cur": self.cur.currentData(), "yazi": self.yazi.text().strip(),
                             "tarih": self.tarih.date().toString("dd.MM.yyyy"), "vade": self.vade.date().toString("dd.MM.yyyy"),
                             "yer": self.yer.text().strip(), "katip": self.katip.text().strip(), "sahit1": self.s1.text().strip(),
                             "sahit2": self.s2.text().strip(), "aciklama": self.aciklama.text().strip()}, self.dil.currentData())

    def _doc(self):
        d = QTextDocument()
        d.setHtml(self.html())
        if self.dil.currentData() == "ar":
            o = d.defaultTextOption()
            o.setTextDirection(Qt.RightToLeft)
            d.setDefaultTextOption(o)
        return d

    def onizle(self):
        d = QDialog(self)
        d.setWindowTitle(_("Önizle"))
        d.resize(760, 820)
        v = QVBoxLayout(d)
        t = QTextBrowser()
        t.setHtml(self.html())
        v.addWidget(t)
        d.exec()

    def pdf(self):
        yol, _f = QFileDialog.getSaveFileName(self, _("PDF kaydet"), f"senet_{datetime.now():%Y%m%d}.pdf", "PDF (*.pdf)")
        if not yol:
            return
        pr = QPrinter(QPrinter.HighResolution)
        pr.setOutputFormat(QPrinter.PdfFormat)
        pr.setOutputFileName(yol)
        self._doc().print_(pr)
        QDesktopServices.openUrl(QUrl.fromLocalFile(yol))

    def yazdir(self):
        pr = QPrinter(QPrinter.HighResolution)
        if QPrintDialog(pr, self).exec():
            self._doc().print_(pr)


# ================================================================ hızlı kayıt
class HizliKayitDialog(QDialog):
    """Yazılan cümleden (internetsiz) kayıt taslağı çıkarır; kullanıcı onaylayınca kaydeder."""

    def __init__(self, parent, db, metin=""):
        super().__init__(parent)
        self.db = db
        self.created_pid = None
        self.setWindowTitle(_("Hızlı kayıt"))
        self.setMinimumWidth(520)
        f = QFormLayout(self)
        self.cumle = QLineEdit(metin)
        self.cumle.setPlaceholderText(_("ör. Ahmet'e 500 TL verdim kira için"))
        self.cumle.textChanged.connect(self.ayristir)
        f.addRow(_("Yazın"), self.cumle)
        ip = QLabel(_("Örnekler: “Ali'den 200 dolar aldım” · “received 50$ from John” · “أعطيت محمد 100 دولار”. "
                      "İnternet gerekmez; aşağıdaki alanları kontrol edip kaydedin."))
        ip.setWordWrap(True)
        ip.setObjectName("muted")
        f.addRow(ip)
        self.kisi = QComboBox()
        self.kisi.setEditable(True)
        for p in db.persons():
            self.kisi.addItem(p["name"], p["id"])
        f.addRow(_("Kişi"), self.kisi)
        self.r_ver = QRadioButton(_("Verdim (Çıktı)"))
        self.r_al = QRadioButton(_("Aldım (Girdi)"))
        self.r_ver.setChecked(True)
        y = QHBoxLayout()
        y.addWidget(self.r_ver)
        y.addWidget(self.r_al)
        y.addStretch(1)
        f.addRow(_("İşlem"), y)
        self.tutar = QDoubleSpinBox()
        self.tutar.setRange(0, 1e12)
        self.tutar.setDecimals(2)
        self.tutar.setGroupSeparatorShown(True)
        self.cur = _cur_combo()
        h = QHBoxLayout()
        h.addWidget(self.tutar, 1)
        h.addWidget(self.cur)
        f.addRow(_("Tutar"), h)
        self.aciklama = QLineEdit()
        f.addRow(_("Açıklama"), self.aciklama)
        self.uyari = QLabel()
        self.uyari.setObjectName("hint")
        self.uyari.setWordWrap(True)
        self.uyari.hide()
        f.addRow(self.uyari)
        bb = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        bb.button(QDialogButtonBox.Save).setText(_("Kaydet"))
        bb.button(QDialogButtonBox.Cancel).setText(_("Vazgeç"))
        bb.accepted.connect(self.kaydet)
        bb.rejected.connect(self.reject)
        f.addRow(bb)
        self.kisi.editTextChanged.connect(self.kisi_uyari)
        self.ayristir()

    def ayristir(self, *_a):
        s = E.hizli_ayristir(self.cumle.text(), [(p["id"], p["name"]) for p in self.db.persons()])
        if s["kisi_id"] is not None:
            self.kisi.setCurrentIndex(self.kisi.findData(s["kisi_id"]))
        elif s["ad"]:
            self.kisi.setEditText(s["ad"])
        if s["direction"]:
            (self.r_al if s["direction"] == "ALDIM" else self.r_ver).setChecked(True)
        if s["amount"]:
            self.tutar.setValue(s["amount"])
        if s["currency"]:
            self.cur.setCurrentIndex(self.cur.findData(s["currency"]))
        if s["description"]:
            self.aciklama.setText(s["description"])
        self.kisi_uyari()

    def kisi_uyari(self, *_a):
        ad = self.kisi.currentText().strip()
        yeni = bool(ad) and self.kisi.findText(ad, Qt.MatchFixedString) < 0
        self.uyari.setText(_("“{}” kayıtlı değil; kaydedince yeni kişi olarak eklenir.").format(ad))
        self.uyari.setVisible(yeni)

    def kaydet(self):
        ad = self.kisi.currentText().strip()
        if not ad:
            QMessageBox.warning(self, _("Eksik"), _("Kişi adını yazın."))
            return
        if self.tutar.value() <= 0:
            QMessageBox.warning(self, _("Eksik"), _("Tutarı yazın."))
            return
        i = self.kisi.findText(ad, Qt.MatchFixedString)
        pid = self.kisi.itemData(i) if i >= 0 else None
        if pid is None:
            pid = self.db.add_person(ad)
            self.created_pid = pid
        self.db.add_tx(pid, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ALDIM" if self.r_al.isChecked() else "VERDIM",
                       self.cur.currentData(), round(self.tutar.value(), 2), self.aciklama.text().strip())
        self.pid = pid
        self.accept()


# ================================================================ geri al çubuğu
class GeriAlCubugu(QFrame):
    """Silmeden sonra birkaç saniye görünen “… silindi · Geri al” çubuğu (arşivden geri koyar)."""

    def __init__(self, parent, db, yenile):
        super().__init__(parent)
        self.db = db
        self.yenile = yenile
        self.aid = None
        self.setObjectName("card")
        h = QHBoxLayout(self)
        h.setContentsMargins(14, 8, 10, 8)
        self.yazi = QLabel()
        h.addWidget(self.yazi, 1)
        h.addWidget(_btn(_("Geri al"), self.geri_al, "primary"))
        x = QPushButton("✕")
        x.setFlat(True)
        x.clicked.connect(self.hide)
        h.addWidget(x)
        self.t = QTimer(self, singleShot=True, timeout=self.hide)
        self.hide()

    def goster(self, metin):
        a = self.db.archived(1)
        if not a:
            return
        self.aid = a[0]["id"]
        self.yazi.setText(metin + "  ·  " + _("Ayarlar → Arşiv'de de durur."))
        self.show()
        self.t.start(10000)

    def geri_al(self):
        if self.aid and self.db.restore(self.aid):
            from fccore.widgets import toast
            toast(_("Geri alındı"), "ok")
            self.yenile()
        self.hide()


# ================================================================ raporlar
class AylikGrafik(QWidget):
    """Son 12 ay: verilen (kırmızı) ve alınan (yeşil) sütunlar."""

    def __init__(self):
        super().__init__()
        self.veri = []
        self.cur = "USD"
        self.setMinimumHeight(240)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def ayarla(self, veri, cur):
        self.veri, self.cur = veri, cur
        self.update()

    def paintEvent(self, _e):
        from fccore import style as fcstyle
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        tk = fcstyle.scheme_tokens()
        kirmizi, yesil = fcstyle.qcolor(tk.get("danger", "#c0392b")), fcstyle.qcolor(tk.get("ok", "#0f8f6a"))
        yazi = fcstyle.qcolor(tk.get("muted", "#667777"))
        cizgi = fcstyle.qcolor(tk.get("border", "#c9d3d0"))
        r = self.rect().adjusted(46, 12, -10, -40)
        enb = max([max(v, a) for _ay, v, a in self.veri] + [1])
        p.setPen(QPen(cizgi, 1))
        for i in range(5):
            y = r.bottom() - r.height() * i / 4
            p.drawLine(r.left(), int(y), r.right(), int(y))
            p.setPen(yazi)
            deger = enb * i / 4
            p.drawText(QRectF(0, y - 8, 42, 16), Qt.AlignRight | Qt.AlignVCenter,
                       MASKE[:2] if GIZLE[0] else (f"{deger / 1000:.0f}k" if enb >= 10000 else f"{deger:.0f}"))
            p.setPen(QPen(cizgi, 1))
        n = max(len(self.veri), 1)
        gen = r.width() / n
        for i, (ay, v, a) in enumerate(self.veri):
            x = r.left() + i * gen
            w = max(gen * 0.32, 3)
            for j, (deger, renk) in enumerate(((v, kirmizi), (a, yesil))):
                hgt = r.height() * deger / enb
                p.fillRect(QRectF(x + gen * 0.15 + j * (w + 2), r.bottom() - hgt, w, hgt), renk)
            p.setPen(yazi)
            p.drawText(QRectF(x, r.bottom() + 4, gen, 16), Qt.AlignCenter, f"{ay[5:7]}.{ay[2:4]}")
        p.setPen(kirmizi)
        p.drawText(QRectF(r.left(), r.bottom() + 20, 160, 16), Qt.AlignLeft, "■ " + _("Verilen (Çıktı)"))
        p.setPen(yesil)
        p.drawText(QRectF(r.left() + 170, r.bottom() + 20, 160, 16), Qt.AlignLeft, "■ " + _("Alınan (Girdi)"))
        p.end()


def _tablo(basliklar):
    t = QTableWidget(0, len(basliklar))
    t.setHorizontalHeaderLabels(basliklar)
    t.setEditTriggers(QAbstractItemView.NoEditTriggers)
    t.setSelectionMode(QAbstractItemView.NoSelection)
    t.verticalHeader().setVisible(False)
    t.setAlternatingRowColors(True)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.setSizeAdjustPolicy(QAbstractItemView.AdjustToContents)
    t.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    return t


def _doldur(t, satirlar, sag=()):
    t.setRowCount(len(satirlar))
    for i, s in enumerate(satirlar):
        for j, v in enumerate(s):
            it = QTableWidgetItem(str(v))
            if j in sag:
                it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, j, it)
    t.setFixedHeight(t.horizontalHeader().height() + sum(t.rowHeight(i) for i in range(t.rowCount())) + 6)


class RaporSayfasi(QWidget):
    def __init__(self, db, shell=None):
        super().__init__()
        self.db = db
        self.shell = shell
        self.dis = QVBoxLayout(self)
        self.dis.setContentsMargins(0, 0, 0, 0)
        self.sc = None
        self.kur()

    def kur(self):
        """Sayfayı (yeniden) kurar — dil değişince de çağrılır."""
        db = self.db
        if self.sc is not None:
            self.sc.setParent(None)
            self.sc.deleteLater()
        dis = self.dis
        sc = self.sc = QScrollArea()
        sc.setWidgetResizable(True)
        sc.setFrameShape(QFrame.NoFrame)
        sc.setObjectName("raporScroll")
        sc.setStyleSheet("QScrollArea#raporScroll, QWidget#raporIc { background: transparent; }")
        sc.viewport().setAutoFillBackground(False)
        dis.addWidget(sc)
        ic = QWidget()
        ic.setObjectName("raporIc")
        ic.setAutoFillBackground(False)
        sc.setWidget(ic)
        v = QVBoxLayout(ic)
        v.setContentsMargins(24, 16, 24, 20)
        v.setSpacing(14)
        ust = QHBoxLayout()
        ust.addWidget(_btn("⟳ " + _("Yenile"), self.yenile))
        ust.addStretch(1)
        ust.addWidget(_btn(_("Kayıtları CSV olarak dışa aktar"), lambda: self.csv_kaydet("kayit")))
        ust.addWidget(_btn(_("Bakiyeleri CSV olarak dışa aktar"), lambda: self.csv_kaydet("bakiye")))
        ust.addWidget(_btn(_("CSV'den içe aktar…"), self.csv_ice, "primary"))
        v.addLayout(ust)

        def kart(baslik):
            c = QFrame()
            c.setObjectName("card")
            l = QVBoxLayout(c)
            l.setContentsMargins(16, 14, 16, 14)
            b = QLabel(baslik)
            b.setObjectName("h2")
            l.addWidget(b)
            v.addWidget(c)
            return l
        # özet + kur
        l = kart(_("Genel durum"))
        self.t_ozet = _tablo([_("Para birimi"), _("Alacak"), _("Verecek"), _("Net"), _("Kişi (alacak / verecek)")])
        l.addWidget(self.t_ozet)
        kh = QHBoxLayout()
        kh.addWidget(QLabel(_("Kurlar (elle):")))
        g = getattr(db, "guvenlik", None)
        kur = (g.a.get("kurlar") if g else None) or {}
        self.kur = {}
        for c in ("TRY", "SYP"):
            s = QDoubleSpinBox()
            s.setRange(0, 1e9)
            s.setDecimals(4)
            s.setGroupSeparatorShown(True)
            s.setValue(float(kur.get(c) or 0))
            s.setPrefix("1 $ = ")
            s.setMinimumWidth(230)
            s.setMinimumHeight(34)
            s.setSuffix(" " + SYMBOLS[c])
            s.valueChanged.connect(self.kur_kaydet)
            self.kur[c] = s
            kh.addWidget(s)
        kh.addStretch(1)
        l.addLayout(kh)
        self.l_usd = QLabel()
        self.l_usd.setStyleSheet("font-size:16px;font-weight:700;")
        self.l_usd.setWordWrap(True)
        l.addWidget(self.l_usd)
        # yaşlandırma
        l = kart(_("Yaşlandırma (son hareketten bu yana geçen gün)"))
        ip = QLabel(_("Açık bakiyeler, kişiyle o para biriminde yapılan son işlemden bu yana geçen süreye göre gruplanır. "
                      "Uzun süredir hareketsiz alacaklar takip gerektirir."))
        ip.setWordWrap(True)
        ip.setObjectName("muted")
        l.addWidget(ip)
        self.t_yas = _tablo([_("Para birimi"), _("Tür"), "0–30", "31–90", "91–180", "180+"])
        l.addWidget(self.t_yas)
        # en büyükler
        l = kart(_("En büyük bakiyeler"))
        iki = QHBoxLayout()
        sol = QVBoxLayout()
        sol.addWidget(QLabel("<b>" + _("Alacaklı olduğum kişiler") + "</b>"))
        self.t_alacak = _tablo([_("Kişi"), _("Bakiye"), _("Son işlem")])
        sol.addWidget(self.t_alacak)
        sol.addStretch(1)
        sag = QVBoxLayout()
        sag.addWidget(QLabel("<b>" + _("Borçlu olduğum kişiler") + "</b>"))
        self.t_verecek = _tablo([_("Kişi"), _("Bakiye"), _("Son işlem")])
        sag.addWidget(self.t_verecek)
        sag.addStretch(1)
        iki.addLayout(sol, 1)
        iki.addSpacing(12)
        iki.addLayout(sag, 1)
        l.addLayout(iki)
        # aylık
        l = kart(_("Aylık hareket (son 12 ay)"))
        self.g_cur = _cur_combo()
        self.g_cur.currentIndexChanged.connect(self.grafik)
        gh = QHBoxLayout()
        gh.addWidget(self.g_cur)
        gh.addStretch(1)
        l.addLayout(gh)
        self.g = AylikGrafik()
        l.addWidget(self.g)
        # gecikenler
        l = kart(_("Vadesi geçmiş hatırlatıcılar"))
        self.t_gec = _tablo([_("Vade"), _("Kişi"), _("Tür"), _("Tutar"), _("Not")])
        l.addWidget(self.t_gec)
        self.l_gec = QLabel()
        self.l_gec.setObjectName("muted")
        l.addWidget(self.l_gec)
        v.addStretch(1)
        self.r = None

    def showEvent(self, e):
        super().showEvent(e)
        self.yenile()

    def kur_kaydet(self, *_a):
        g = getattr(self.db, "guvenlik", None)
        if g:
            g.a["kurlar"] = {c: s.value() for c, s in self.kur.items()}
            g.kaydet()
        self.yenile()

    def yenile(self):
        kur = {c: s.value() for c, s in self.kur.items()}
        r = self.r = E.rapor(self.db, kur)
        o = r["ozet"]
        _doldur(self.t_ozet, [[_(CUR_AD[c]), para(o[c]["alacak"], c), para(o[c]["verecek"], c), para(o[c]["net"], c),
                               f'{o[c]["kisi_alacak"]} / {o[c]["kisi_verecek"]}'] for c in CURRENCIES], sag=(1, 2, 3))
        t = _("Net durum (dolar karşılığı): {}").format(para(r["toplam_usd"], "USD"))
        if r["eksik_kur"]:
            t += "  —  " + _("{} için kur girilmediğinden hesaba katılmadı.").format(", ".join(r["eksik_kur"]))
        self.l_usd.setText(t)
        satir = []
        for c in CURRENCIES:
            for tur, ad in (("alacak", _("Alacak")), ("verecek", _("Verecek"))):
                d = r["yas"][c][tur]
                if any(abs(x) >= 0.005 for x in d.values()):
                    satir.append([c, ad] + [para(d[k], c) if abs(d[k]) >= 0.005 else "—" for k in r["kovalar"]])
        _doldur(self.t_yas, satir or [["—", "", "", "", "", ""]], sag=(2, 3, 4, 5))

        def bs(liste):
            return [[s["ad"], para(s["bakiye"], s["cur"]), (s["son"] or "")[:10] + "  (" + _("{} gün").format(s["gun"]) + ")"]
                    for s in liste] or [["—", "", ""]]
        _doldur(self.t_alacak, bs(r["en_alacak"]), sag=(1,))
        _doldur(self.t_verecek, bs(r["en_verecek"]), sag=(1,))
        self.grafik()
        kind = {"TAHSIL": _("Tahsil edilecek (alınacak)"), "ODEME": _("Ödenecek (verilecek)")}
        _doldur(self.t_gec, [[x["due"][:16], x["person_name"], kind.get(x["kind"], x["kind"]),
                              para(x["amount"], x["currency"]) if x["amount"] else x["currency"], x["note"] or ""]
                             for x in r["geciken"][:30]] or [["—", "", "", "", ""]], sag=(3,))
        self.l_gec.setText(_("Toplam {} hatırlatıcının vadesi geçti.").format(len(r["geciken"])) if r["geciken"] else
                           _("Vadesi geçmiş hatırlatıcı yok."))

    def grafik(self, *_a):
        if self.r:
            c = self.g_cur.currentData()
            self.g.ayarla(self.r["hareket"][c], c)

    def csv_kaydet(self, tur):
        ad = f"bereket_{'kayitlar' if tur == 'kayit' else 'bakiyeler'}_{datetime.now():%Y%m%d}.csv"
        yol, _f = QFileDialog.getSaveFileName(self, _("CSV kaydet"), ad, "CSV (*.csv)")
        if not yol:
            return
        metin = E.csv_disa(self.db, i18n.lang()) if tur == "kayit" else E.csv_bakiyeler(self.db, i18n.lang())
        with open(yol, "w", encoding="utf-8", newline="") as f:
            f.write(metin)
        from fccore.widgets import toast
        toast(_("Kaydedildi: {}").format(os.path.basename(yol)), "ok")

    def csv_ice(self):
        yol, _f = QFileDialog.getOpenFileName(self, _("CSV'den içe aktar…"), "", "CSV (*.csv *.txt)")
        if not yol:
            return
        metin = None
        for kod in ("utf-8-sig", "cp1254", "cp1256", "latin-1"):
            try:
                with open(yol, encoding=kod) as f:
                    metin = f.read()
                break
            except UnicodeDecodeError:
                continue
        coz = E.csv_cozumle(metin or "", self.db)
        yeni = [s for s in coz["satirlar"] if not s["yinelenen"]]
        yin = len(coz["satirlar"]) - len(yeni)
        msg = _("{} kayıt bulundu.").format(len(coz["satirlar"]))
        msg += "\n" + _("Eklenecek: {} kayıt, {} yeni kişi.").format(len(yeni), len(coz["yeni_kisiler"]))
        if yin:
            msg += "\n" + _("Zaten var olduğu için atlanacak: {}").format(yin)
        if coz["hatalar"]:
            ned = {"tarih": _("tarih okunamadı"), "kisi": _("kişi boş"), "tutar": _("tutar okunamadı"), "birim": _("para birimi bilinmiyor"),
                   "islem": _("işlem (Verdim/Aldım) bilinmiyor")}
            msg += "\n\n" + _("Okunamayan satırlar:") + "\n" + "\n".join(
                _("Satır {}: {}").format(n, ned.get(k, k)) for n, k in coz["hatalar"][:12])
            if len(coz["hatalar"]) > 12:
                msg += "\n…"
        msg += "\n\n" + _("Beklenen sütunlar: Tarih; Kişi; İşlem (Verdim/Aldım); Birim (USD/TRY/SYP); Tutar; Açıklama")
        if not yeni:
            QMessageBox.information(self, _("CSV'den içe aktar…"), msg)
            return
        if QMessageBox.question(self, _("CSV'den içe aktar…"), msg + "\n\n" + _("İçe aktarılsın mı?")) != QMessageBox.Yes:
            return
        n, k = E.csv_ice_al(self.db, coz)
        QMessageBox.information(self, _("CSV'den içe aktar…"), _("{} kayıt ve {} yeni kişi eklendi.").format(n, k))
        if self.shell is not None and self.shell.defter is not None:
            self.shell.defter.load_persons()
        self.yenile()
