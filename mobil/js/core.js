/* Bereket Alacak-Verecek Defteri — telefon sürümü: sabitler, dil, biçimlendirme, yardımcılar. */
'use strict';

const APP_VERSION = "1.17";
const APP_TITLE = "Bereket Alacak-Verecek Defteri";
const CURRENCIES = ["USD", "TRY", "SYP"];
const CURRENCY_NAMES = { USD: "Dolar ($)", TRY: "Türk Lirası (₺)", SYP: "Suriye Lirası (£S)" };
const CURRENCY_SYMBOLS = { USD: "$", TRY: "₺", SYP: "£S" };
const CHANNELS = ["wa", "tg", "sg", "call"];
const CH_NAMES = { wa: "WhatsApp", tg: "Telegram", sg: "Signal", call: "Telefonla arama" };
const CH_OPEN = { wa: "WhatsApp'ta mesaj yaz", tg: "Telegram'da mesaj yaz", sg: "Signal'de mesaj yaz", call: "Ara" };
const CH_COLORS = { wa: "#25D366", tg: "#229ED9", sg: "#3A76F0", call: "#0f8f6a" };
const KIND_TEXT = { TAHSIL: "Tahsil edilecek (alınacak)", ODEME: "Ödenecek (verilecek)" };
// Ana ekranda 10 saniyede bir sırayla değişen alacak-verecek, borç ve alışverişle ilgili hadisler (yalnızca Buhârî ve Müslim). Uygulamanın içinde durur, internet gerekmez.
const QUOTES = [
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
];
let QUOTE_I = Math.floor(Math.random() * QUOTES.length);
const DAY_NAMES = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"];
const GREEN = "#0f8f6a", RED = "#c0392b";
const LANGS = { tr: "Türkçe", en: "English", ar: "العربية" };

/* ------------------------------------------------------------------ dil */
let LANG = "tr";
try { const l = localStorage.getItem("bereket_lang"); if (l && LANGS[l]) LANG = l; } catch (e) { /* yok */ }

function t(s) {
  if (LANG === "tr") return s;
  const p = (window.I18N_DESKTOP && window.I18N_DESKTOP[s]) || (window.I18N_MOBILE && window.I18N_MOBILE[s]);
  if (!p) return s;
  return (LANG === "en" ? p[0] : p[1]) || s;
}
function tf(s, ...args) {
  let i = 0;
  return t(s).replace(/\{\}/g, () => (i < args.length ? String(args[i++]) : ""));
}
function isRtl() { return LANG === "ar"; }
function setLang(l) {
  LANG = LANGS[l] ? l : "tr";
  try { localStorage.setItem("bereket_lang", LANG); } catch (e) { /* yok */ }
  applyLangToDocument();
}
function applyLangToDocument() {
  document.documentElement.lang = LANG;
  document.documentElement.dir = isRtl() ? "rtl" : "ltr";
}

/* ------------------------------------------------------------------ biçim */
/** 1234567.5 -> tr "1.234.567,50", en/ar "1,234,567.50" (masaüstü fmt ile aynı) */
function fmt(x) {
  x = Number(x) || 0;
  const neg = x < 0 && Math.abs(x) >= 0.005;
  let s = Math.abs(x).toFixed(2);
  let [i, d] = s.split(".");
  i = i.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  s = i + "." + d;
  if (LANG === "tr") s = s.replace(/[,.]/g, c => (c === "," ? "." : ","));
  return (neg ? "-" : "") + s;
}
function money(x, cur) { return fmt(x) + " " + CURRENCY_SYMBOLS[cur]; }

/** Kullanıcının yazdığı tutar: "1.234,56", "1,234.56", "12,5", "12.5" -> sayı (NaN = geçersiz) */
function parseAmount(str) {
  let s = String(str || "").replace(/[\s '$₺£S]/g, "").trim();
  if (!s) return 0;
  const lc = s.lastIndexOf(","), ld = s.lastIndexOf(".");
  if (lc >= 0 && ld >= 0) {
    const dec = lc > ld ? "," : ".";
    const grp = dec === "," ? "." : ",";
    s = s.split(grp).join("").replace(dec, ".");
  } else if (lc >= 0 || ld >= 0) {
    const sep = lc >= 0 ? "," : ".";
    const parts = s.split(sep);
    if (parts.length > 2) s = parts.join("");                 // 1.234.567 -> grup ayırıcı
    else s = parts[0] + "." + parts[1];                         // tek ayırıcı -> ondalık
  }
  if (!/^\d*\.?\d*$/.test(s) || s === ".") return NaN;
  return Number(s);
}
/** sayıyı giriş kutusu için yaz: tr "1234,5" */
function amountInput(x) {
  if (!x) return "";
  let s = String(Math.round(x * 100) / 100);
  return LANG === "tr" ? s.replace(".", ",") : s;
}

function pad(n) { return String(n).padStart(2, "0"); }
function dateToStr(d) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}
function nowStr() { return dateToStr(new Date()); }
function parseTs(ts) {
  const m = /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})(?::(\d{2}))?/.exec(ts || "");
  if (!m) return new Date(NaN);
  return new Date(+m[1], +m[2] - 1, +m[3], +m[4], +m[5], +(m[6] || 0));
}
/** "2026-10-08 14:30:00" -> "08.10.2026 14:30" */
function tsDisplay(ts) {
  if (!ts) return "";
  return `${ts.slice(8, 10)}.${ts.slice(5, 7)}.${ts.slice(0, 4)} ${ts.slice(11, 16)}`;
}
function ts16(ts) { return (ts || "").slice(0, 16).replace("T", " "); }
function toInputDT(ts) { return ts16(ts).replace(" ", "T"); }
/** tx.ts ve rem.due saniyesiz yazılır (§3): "YYYY-MM-DD HH:MM" */
function fromInputDT(v) { return v ? v.replace("T", " ").slice(0, 16) : ""; }
function dayName(d) { return t(DAY_NAMES[(d.getDay() + 6) % 7]); }
function hhmm(d) { return pad(d.getHours()) + ":" + pad(d.getMinutes()); }
function stamp(d) { d = d || new Date(); return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}`; }

function uuidHex() {
  const b = new Uint8Array(16);
  crypto.getRandomValues(b);
  b[6] = (b[6] & 0x0f) | 0x40;
  b[8] = (b[8] & 0x3f) | 0x80;
  return Array.from(b, x => x.toString(16).padStart(2, "0")).join("");
}

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function lower(s) { return String(s || "").toLocaleLowerCase("tr"); }

/* ------------------------------------------------------------------ DOM */
const PROPS = new Set(["value", "checked", "disabled", "selected", "multiple", "hidden"]);
function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  if (attrs) {
    for (const k in attrs) {
      const v = attrs[k];
      if (v == null || v === false) continue;
      if (k === "class") el.className = v;
      else if (k === "style") el.style.cssText = v;
      else if (k === "html") el.innerHTML = v;
      else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2), v);
      else if (PROPS.has(k)) el[k] = v;
      else el.setAttribute(k, v === true ? "" : v);
    }
  }
  appendKids(el, kids);
  return el;
}
function appendKids(el, kids) {
  for (const k of kids) {
    if (k == null || k === false) continue;
    if (Array.isArray(k)) appendKids(el, k);
    else if (k instanceof Node) el.appendChild(k);
    else el.appendChild(document.createTextNode(String(k)));
  }
}
/** soldan sağa yazılan parça (tarih, tutar) — Arapçada da okunaklı kalır */
function ltr(text, cls) { return h("bdi", { dir: "ltr", class: "ltr" + (cls ? " " + cls : "") }, text); }
function $(sel, root) { return (root || document).querySelector(sel); }
function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); return el; }

/* ------------------------------------------------------------------ iletişim simgeleri (masaüstü _channel_svg) */
const _HANDSET = "M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57" +
  ".55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2" +
  " 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z";
const _PLANE = "M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3" +
  "l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93" +
  "c-.23.23-.42.42-.83.42z";
function channelSvg(ch, active) {
  const color = active ? CH_COLORS[ch] : "#c3ccc9";
  let g;
  if (ch === "call") g = `<path transform="translate(10.5,10.5) scale(1.12)" d="${_HANDSET}" fill="#fff"/>`;
  else if (ch === "tg") g = `<path transform="translate(8.5,9.5) scale(1.25)" d="${_PLANE}" fill="#fff"/>`;
  else if (ch === "wa") g = '<path d="M24 10A14 14 0 0 0 12 31.2L10 38L17 36.1A14 14 0 1 0 24 10z" fill="none" stroke="#fff"' +
    ' stroke-width="2.6" stroke-linejoin="round"/>' +
    `<path transform="translate(16.5,16.5) scale(0.62)" d="${_HANDSET}" fill="#fff"/>`;
  else g = '<circle cx="24" cy="24" r="15" fill="none" stroke="#fff" stroke-width="2.4" stroke-dasharray="5 2.6"/>' +
    '<path d="M24 14.5A9.5 9.5 0 0 0 15.8 28.8L14.5 34L19.6 32.6A9.5 9.5 0 1 0 24 14.5z" fill="#fff"/>';
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" aria-hidden="true">` +
    `<circle cx="24" cy="24" r="23" fill="${color}"/>${g}</svg>`;
}
function channelIcon(ch, active, size) {
  return h("span", { class: "chi", style: `width:${size}px;height:${size}px`, html: channelSvg(ch, active) });
}
function activeChannels(p) { return CHANNELS.filter(c => p["ch_" + c]); }
function chLabel(ch) { return ch === "call" ? t("Arama") : t(CH_NAMES[ch]); }

function _phoneDigits(num) {
  num = String(num || "").trim();
  let digits = num.replace(/\D/g, "");
  const intl = num.startsWith("+") || digits.startsWith("00");
  if (digits.startsWith("00")) digits = digits.slice(2);
  return [digits, intl];
}
/** masaüstü channel_url ile aynı: {url, err} */
function channelUrl(p, ch) {
  let num;
  if (ch === "tg") {
    const user = String(p.tg_user || "").trim().replace(/^@+/, "");
    if (user && !/^[\d+ \-()]+$/.test(user)) return { url: "https://t.me/" + user, err: null };
    num = user || p.phone || p.phone2;
  } else if (ch === "wa") num = p.wa_phone || p.phone || p.phone2;
  else if (ch === "sg") num = p.sg_phone || p.phone || p.phone2;
  else num = p.phone || p.phone2;
  const [digits, intl] = _phoneDigits(num);
  if (!digits) return { url: null, err: t("Bu kişi için numara yazılmamış. Kişi Defteri'nden ekleyin.") };
  if (ch === "call") return { url: "tel:" + (intl ? "+" : "") + digits, err: null };
  if (!intl) return { url: null, err: t("Numarayı ülke koduyla yazın (ör. +90 5xx..., +963 9xx...).") };
  return { url: { wa: `https://wa.me/${digits}`, tg: `https://t.me/+${digits}`, sg: `https://signal.me/#p/+${digits}` }[ch], err: null };
}

/* ------------------------------------------------------------------ Android köprüsü */
function bridge() { return window.AndroidBridge || null; }
function bridgeHas(name) { const b = bridge(); return !!(b && typeof b[name] === "function"); }
// Görünen sürüm = web paketinin sürümü (uygulama içi güncellemeyle değişir; APK sürümü değişmeyebilir)
function appVersion() {
  return APP_VERSION;
}
function openUrl(url) {
  if (bridgeHas("openUrl")) { bridge().openUrl(url); return; }
  const w = window.open(url, "_blank", "noopener");
  if (!w && !url.startsWith("tel:")) location.href = url;
}
function blobToBase64(blob) {
  return new Promise((res, rej) => {
    const r = new FileReader();
    r.onload = () => { const s = String(r.result); res(s.slice(s.indexOf(",") + 1)); };
    r.onerror = () => rej(r.error);
    r.readAsDataURL(blob);
  });
}
function base64ToBytes(b64) {
  const bin = atob(b64 || "");
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
function textToBlob(text, mime) { return new Blob([text], { type: mime }); }
function downloadBlob(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = h("a", { href: url, download: name, style: "display:none" });
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { a.remove(); URL.revokeObjectURL(url); }, 4000);
}
/** "Farklı kaydet…" — Android: sistem kaydet penceresi; tarayıcı: indirme */
async function saveBlobAs(blob, mime, name) {
  if (bridgeHas("saveFile")) { bridge().saveFile(await blobToBase64(blob), mime || "application/octet-stream", name); return; }
  downloadBlob(blob, name);
}
async function shareBlob(blob, mime, name) {
  if (bridgeHas("shareFile")) { bridge().shareFile(await blobToBase64(blob), mime || "application/octet-stream", name); return; }
  try {
    const f = new File([blob], name, { type: mime || blob.type });
    if (navigator.canShare && navigator.canShare({ files: [f] })) { await navigator.share({ files: [f], title: name }); return; }
  } catch (e) { if (e && e.name === "AbortError") return; }
  downloadBlob(blob, name);
}
async function openBlobExternal(blob, mime, name) {
  if (bridgeHas("openFile")) { bridge().openFile(await blobToBase64(blob), mime || "application/octet-stream", name); return; }
  const url = URL.createObjectURL(blob);
  const w = window.open(url, "_blank");
  if (!w) downloadBlob(blob, name);
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}
const MIME_BY_EXT = {
  ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp",
  ".bmp": "image/bmp", ".heic": "image/heic", ".pdf": "application/pdf", ".txt": "text/plain", ".html": "text/html",
  ".doc": "application/msword", ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ".xls": "application/vnd.ms-excel", ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ".zip": "application/zip", ".json": "application/json",
};
const EXT_BY_MIME = Object.fromEntries(Object.entries(MIME_BY_EXT).map(([e, m]) => [m, e]));
EXT_BY_MIME["image/jpeg"] = ".jpg";
function extOf(name, mime) {
  const m = /\.[A-Za-z0-9]{1,8}$/.exec(name || "");
  if (m) return m[0].toLowerCase();
  return EXT_BY_MIME[mime] || "";
}
function isImageDoc(d) {
  const m = (d.mime || MIME_BY_EXT[d.ext] || "").toLowerCase();
  return m.startsWith("image/") && !/heic|heif|tiff/.test(m);
}
function mimeOfDoc(d) { return d.mime || MIME_BY_EXT[d.ext] || "application/octet-stream"; }
function fileSizeText(n) {
  n = Number(n) || 0;
  if (n < 1024) return n + " B";
  if (n < 1024 * 1024) return (n / 1024).toFixed(0) + " KB";
  return (n / 1024 / 1024).toFixed(1).replace(".", LANG === "tr" ? "," : ".") + " MB";
}
