/* v1.22 ekleri (telefon) — masaüstü ekler.py / ekler_cekirdek.py ile aynı kurallar:
   PIN kilidi + tutarları gizle, günlük otomatik yedek (bu cihazda, son 7 gün) + önizlemeli "eksikleri geri getir" (silmez, üzerine yazmaz),
   taksit planı, mesaj / mutabakat (WhatsApp · Telegram · kopyala), borç senedi (Bakara 282), raporlar, CSV dışa / içe aktarma,
   hızlı kayıt (internetsiz ayrıştırıcı, tr/en/ar), geri al çubuğu, etiket süzgeci, gecikenler (⏰). Çeviriler: js/i18n_ekler.js. */
'use strict';

const Ekler = (() => {
  const SYM = { USD: "$", TRY: "₺", SYP: "£S" };
  const MASKE = "•••••";
  const AYAR_KEY = "bereket_guvenlik";
  const VARS = { pin: null, kilitDk: 5, gizle: false, otoYedek: true, ben: "", kurlar: { TRY: 0, SYP: 0 } };

  /* ---------------------------------------------------------------- ayarlar (yalnız bu cihaz) */
  function ayar() {
    let a = {};
    try { a = JSON.parse(localStorage.getItem(AYAR_KEY) || "{}") || {}; } catch (e) { a = {}; }
    return Object.assign({}, VARS, a, { kurlar: Object.assign({}, VARS.kurlar, a.kurlar || {}) });
  }
  function ayarYaz(a) { try { localStorage.setItem(AYAR_KEY, JSON.stringify(a)); } catch (e) { /* yok */ } }
  const A = ayar();

  /* ---------------------------------------------------------------- tutarları gizle: money() ekranda maskeler */
  let ACIK = 0;   // >0: döküm / senet / mesaj üretilirken tutarlar her zaman açık
  const moneyAsil = money;
  money = function (x, cur) { return A.gizle && !ACIK ? MASKE + " " + CURRENCY_SYMBOLS[cur] : moneyAsil(x, cur); };   // eslint-disable-line no-global-assign
  function acikla(fn) { ACIK++; try { return fn(); } finally { ACIK--; } }
  const stBuild = Statement.build.bind(Statement);
  Statement.build = o => acikla(() => stBuild(o));
  function gizleDegistir(on) {
    A.gizle = !!on; ayarYaz(A);
    App.refresh(); Sheets.refreshAll();
    const g = document.querySelector(".top-btn.goz"); if (g) g.firstChild.textContent = A.gizle ? "🙈" : "👁";
  }

  /* ---------------------------------------------------------------- SHA-256 (WebView'de crypto.subtle olmayabilir) */
  function sha256(str) {
    const K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01,
      0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f,
      0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
      0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70,
      0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
      0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2];
    const b = new TextEncoder().encode(str);
    const l = b.length, n = ((l + 9 + 63) >> 6) << 6;
    const m = new Uint8Array(n); m.set(b); m[l] = 0x80;
    const dv = new DataView(m.buffer); dv.setUint32(n - 4, l * 8); dv.setUint32(n - 8, Math.floor(l / 0x20000000));
    let H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19];
    const w = new Uint32Array(64), r = (x, k) => (x >>> k) | (x << (32 - k));
    for (let o = 0; o < n; o += 64) {
      for (let i = 0; i < 16; i++) w[i] = dv.getUint32(o + i * 4);
      for (let i = 16; i < 64; i++) {
        const s0 = r(w[i - 15], 7) ^ r(w[i - 15], 18) ^ (w[i - 15] >>> 3), s1 = r(w[i - 2], 17) ^ r(w[i - 2], 19) ^ (w[i - 2] >>> 10);
        w[i] = (w[i - 16] + s0 + w[i - 7] + s1) | 0;
      }
      let [a, bb, c, d, e, f, g, hh] = H;
      for (let i = 0; i < 64; i++) {
        const t1 = (hh + (r(e, 6) ^ r(e, 11) ^ r(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + w[i]) | 0;
        const t2 = ((r(a, 2) ^ r(a, 13) ^ r(a, 22)) + ((a & bb) ^ (a & c) ^ (bb & c))) | 0;
        hh = g; g = f; f = e; e = (d + t1) | 0; d = c; c = bb; bb = a; a = (t1 + t2) | 0;
      }
      H = H.map((x, i) => (x + [a, bb, c, d, e, f, g, hh][i]) | 0);
    }
    return H.map(x => (x >>> 0).toString(16).padStart(8, "0")).join("");
  }
  const PIN_TUR = 3000;
  function pinOzet(pin, tuz) { let x = tuz + ":" + pin; for (let i = 0; i < PIN_TUR; i++) x = sha256(x + tuz); return x; }
  function pinKaydi(pin) { const tuz = uuidHex(); return { tuz, ozet: pinOzet(pin, tuz) }; }
  function pinDogru(k, pin) { return !!(k && pin && pinOzet(pin, k.tuz) === k.ozet); }
  const pinGecerli = p => /^\d{4,8}$/.test(p || "");

  /* ---------------------------------------------------------------- kilit ekranı */
  let perde = null, yanlis = 0, bekle = 0, gizlendi = 0;
  function kilitli() { return !!(perde && perde.isConnected); }
  function kilitle() {
    if (!A.pin || kilitli()) return;
    const pin = h("input", { class: "inp kilit-pin", type: "password", inputmode: "numeric", maxlength: 8, autocomplete: "off", dir: "ltr",
      placeholder: "••••", onkeydown: e => { if (e.key === "Enter") dene(); } });
    const msg = h("div", { class: "kilit-msg muted" }, " ");
    const dene = () => {
      if (Date.now() < bekle) { msg.textContent = tf("Çok fazla hatalı deneme. {} saniye sonra tekrar deneyin.", Math.ceil((bekle - Date.now()) / 1000)); return; }
      if (pinDogru(A.pin, pin.value.trim())) { yanlis = 0; perde.remove(); perde = null; document.body.classList.remove("kilitli"); return; }
      pin.value = "";
      if (++yanlis >= 5) { yanlis = 0; bekle = Date.now() + 30000; msg.textContent = tf("Çok fazla hatalı deneme. {} saniye sonra tekrar deneyin.", 30); }
      else msg.textContent = t("PIN yanlış.");
    };
    perde = h("div", { class: "kilit", role: "dialog", "aria-modal": "true" },
      h("div", { class: "kilit-kutu" }, h("img", { src: "assets/logo.svg", alt: "", width: 72, height: 72 }),
        h("h2", null, "🔒 " + t(APP_TITLE)), h("p", null, t("Devam etmek için PIN kodunuzu girin.")), pin, msg,
        btn(t("Kilidi aç"), "primary", dene),
        btn(t("PIN'i unuttum"), "linkish small", () => Dlg.alert(t("Güvenliğiniz için PIN buradan sıfırlanamaz. Uygulamanın verilerini sıfırlamadan PIN kaldırılamaz; kayıtlarınız eşitlendiyse bulutta durur. Yardım için Ayarlar → Admin ile iletişim."), t("PIN'i unuttum")))));
    document.body.appendChild(perde);
    document.body.classList.add("kilitli");
    setTimeout(() => pin.focus(), 80);
  }
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") gizlendi = Date.now();
    else if (A.pin && A.kilitDk > 0 && gizlendi && Date.now() - gizlendi >= A.kilitDk * 60000) kilitle();
  });

  function pinForm(kaldir) {
    const eski = inp({ type: "password", inputmode: "numeric", maxlength: 8, dir: "ltr" });
    const y1 = inp({ type: "password", inputmode: "numeric", maxlength: 8, dir: "ltr" });
    const y2 = inp({ type: "password", inputmode: "numeric", maxlength: 8, dir: "ltr" });
    let entry;
    const kaydet = async () => {
      if (A.pin && !pinDogru(A.pin, eski.value.trim())) { await Dlg.alert(t("Şu anki PIN yanlış."), t("PIN")); return; }
      if (kaldir) A.pin = null;
      else {
        if (!pinGecerli(y1.value.trim())) { await Dlg.alert(t("PIN 4–8 rakamdan oluşmalı."), t("PIN")); return; }
        if (y1.value.trim() !== y2.value.trim()) { await Dlg.alert(t("İki PIN aynı değil."), t("PIN")); return; }
        A.pin = pinKaydi(y1.value.trim());
      }
      ayarYaz(A); Sheets.close(entry); toast(t("Kaydedildi")); Sheets.refreshAll();
    };
    entry = Sheets.open({ title: kaldir ? t("PIN'i kaldır") : t("PIN belirle / değiştir"), cls: "form",
      body: h("div", { class: "form-grid" }, A.pin ? field(t("Şu anki PIN"), eski) : null,
        kaldir ? null : [field(t("Yeni PIN (4–8 rakam)"), y1), field(t("Yeni PIN (tekrar)"), y2),
          h("p", { class: "muted" }, t("PIN bu telefonda saklanır ve eşitlenmez. Bilgisayarda ayrı PIN belirleyebilirsiniz."))]),
      footer: [btn(t("Vazgeç"), "light", () => Sheets.close(entry)), btn(t("Kaydet"), "primary", kaydet)] });
  }

  /* ---------------------------------------------------------------- otomatik yedek (IndexedDB meta: otoYedek:YYYY-MM-DD) */
  const YEDEK_SAKLA = 7;
  function anlik() {
    const out = { app: "bereket-alacak-verecek", format: 1, version: appVersion(), created: nowStr(), files: {} };
    for (const c of COLS) out[c] = [...Store.data[c].values()].filter(r => !r.del).map(r => { const o = Object.assign({}, r); delete o.dirty; delete o.bu; return o; });
    return out;
  }
  function otoYedekler() {
    return Object.keys(Store.meta).filter(k => /^otoYedek:\d{4}-\d\d-\d\d$/.test(k)).sort().reverse();
  }
  function otoYedek() {
    if (!A.otoYedek || !Store.idb) return null;
    const gun = nowStr().slice(0, 10), k = "otoYedek:" + gun;
    if (Store.meta[k]) return null;
    if (!Store.live("persons").length) return null;
    Store.setMeta(k, JSON.stringify(anlik()));
    for (const eski of otoYedekler().slice(YEDEK_SAKLA)) { delete Store.meta[eski]; Store._del("meta", eski).catch(() => {}); }
    return k;
  }
  /** yedekteki satırlardan bu cihazda olmayanları sayar / ekler (var olanlara dokunmaz, silmez) */
  async function eksikler(yedek, yaz) {
    const say = { persons: [0, 0], tx: [0, 0], rem: [0, 0], docs: [0, 0] };
    const var_ = (c, id) => !!Store.get(c, id);
    const kisiVar = new Set(Store.live("persons").map(p => p.id));
    const kayitVar = new Set(Store.live("tx").map(x => x.id));
    for (const c of ["persons", "tx", "rem", "docs"]) {
      for (const r of (yedek[c] || [])) {
        if (!r || r.del || !r.id) continue;
        say[c][0]++;
        if (var_(c, r.id)) continue;
        if ((c === "tx" || c === "rem") && !kisiVar.has(r.person)) continue;
        if (c === "docs" && (!kayitVar.has(r.tx) || !(yedek.files || {})[r.id] && !Store.blobIds.has(r.id))) continue;
        say[c][1]++;
        if (!yaz) { if (c === "persons") kisiVar.add(r.id); if (c === "tx") kayitVar.add(r.id); continue; }
        const row = Object.assign({}, r); delete row.dirty; delete row.bu;
        if (c === "docs") {
          if ((yedek.files || {})[r.id] && !Store.blobIds.has(r.id)) await Store.putBlob(r.id, new Blob([base64ToBytes(yedek.files[r.id])], { type: mimeOfDoc(r) }));
          row.bu = 0;
        }
        Store.save(c, row, true);
        if (c === "persons") kisiVar.add(r.id);
        if (c === "tx") kayitVar.add(r.id);
      }
    }
    if (yaz) Store.changed();
    return say;
  }
  function yedekler() {
    const body = h("div");
    let secili = null;
    const ciz = async () => {
      clear(body);
      body.append(h("p", { class: "muted" }, t("Bir yedek seçin: içinde ne olduğu ve bu cihazda eksik olanlar görünür. “Eksikleri geri getir” yalnız eksik kayıtları ekler; mevcut kayıtlarınıza dokunmaz, hiçbir şeyi silmez.")));
      const liste = otoYedekler();
      if (!liste.length) body.append(h("div", { class: "empty" }, t("Henüz yedek yok.")));
      for (const k of liste) {
        body.append(h("button", { type: "button", class: "prow" + (secili && secili.k === k ? " sel" : ""), onclick: () => sec(k, JSON.parse(Store.meta[k])) },
          h("div", { class: "prow-name" }, "🗂 " + k.slice(9).split("-").reverse().join(".")), h("div", { class: "prow-bal muted" }, t("Otomatik yedek (bu telefonda)"))));
      }
      if (secili) {
        const s = await eksikler(secili.v, false);
        const ad = { persons: t("Kişi"), tx: t("Kayıt"), rem: t("Hatırlatıcı"), docs: t("Belge") };
        const top = Object.values(s).reduce((a, x) => a + x[1], 0);
        body.append(h("div", { class: "card ozet-kart" }, h("b", null, secili.k.startsWith("otoYedek:") ? secili.k.slice(9) : secili.k),
          Object.keys(s).map(c => h("div", null, tf("{}: {} (bu cihazda eksik: {})", ad[c], s[c][0], s[c][1]))),
          h("p", null, top ? tf("Bu yedekte olup bu cihazda olmayan {} öğe var.", top) : t("Geri getirilecek bir şey yok; bu yedekteki her şey bu cihazda var.")),
          top ? btn(t("Eksikleri geri getir"), "primary", async () => {
            if (!(await Dlg.confirm(t("Yedekte olup bu cihazda olmayan kayıtlar eklensin mi? Mevcut kayıtlarınız değişmez."), t("Eksikleri geri getir")))) return;
            const r = await eksikler(secili.v, true);
            await Dlg.alert(tf("Geri getirildi: {} kişi, {} kayıt, {} hatırlatıcı, {} belge.", r.persons[1], r.tx[1], r.rem[1], r.docs[1]), t("Eksikleri geri getir"));
            App.refresh(); Rem.scheduleAll(); ciz();
          }) : null));
      }
    };
    const sec = (k, v) => { secili = { k, v }; ciz(); };
    const dosya = () => {
      const fi = h("input", { type: "file", hidden: true, accept: ".json,application/json", onchange: async e => {
        const f = e.target.files[0]; fi.remove(); if (!f) return;
        try { const v = JSON.parse(await f.text()); if (v.app !== "bereket-alacak-verecek") throw new Error("format"); sec(f.name, v); }
        catch (err) { Dlg.alert(t("Bu dosya geçerli bir yedek değil."), t("Hata")); }
      } });
      document.body.appendChild(fi); fi.click();
    };
    const entry = Sheets.open({ title: t("Yedekler ve geri getirme"), cls: "form", body,
      footer: [btn(t("Başka bir yedek dosyası seç…"), "light2", dosya), btn(t("Kapat"), "light", () => Sheets.close(entry))], refresh: ciz });
    ciz();
  }

  /* ---------------------------------------------------------------- yardımcılar */
  const fmtDil = (x, dil) => { let s = Math.abs(x).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ","); if (dil === "tr") s = s.replace(/[,.]/g, c => (c === "," ? "." : ",")); return s; };
  const tutarDil = (x, c, dil) => (dil === "ar" ? "⁦" + fmtDil(x, dil) + " " + SYM[c] + "⁩" : fmtDil(x, dil) + " " + SYM[c]);
  const bakiyeler = pid => { const b = Store.balances(pid), o = {}; for (const c of CURRENCIES) o[c] = b[c][2]; return o; };
  const bugunTR = () => { const d = new Date(); return pad(d.getDate()) + "." + pad(d.getMonth() + 1) + "." + d.getFullYear(); };
  const dilSec = () => h("select", { class: "inp", "aria-label": t("Dil") }, Object.entries(LANGS).map(([k, v]) => h("option", { value: k, selected: k === LANG }, v)));
  const curSel = c => h("select", { class: "inp", "aria-label": t("Para birimi") }, CURRENCIES.map(k => h("option", { value: k, selected: k === c }, t(CURRENCY_NAMES[k]))));
  function kopyala(text) {
    if (bridgeHas("copyText")) { bridge().copyText(text); return true; }
    try { navigator.clipboard.writeText(text); return true; } catch (e) { /* aşağıda */ }
    const ta = h("textarea", { style: "position:fixed;opacity:0" }); ta.value = text; document.body.appendChild(ta); ta.select();
    let ok = false; try { ok = document.execCommand("copy"); } catch (e) { ok = false; } ta.remove(); return ok;
  }
  const rakam = no => { let d = String(no || "").replace(/\D/g, ""); if (String(no || "").trim().startsWith("00")) d = d.slice(2); return d; };

  /* ---------------------------------------------------------------- mesajlar (masaüstü ekler_cekirdek.MESAJ ile aynı) */
  const MESAJ = {
    tr: { selam: "Merhaba {ad},", selamYok: "Merhaba,", bakiyeBas: "{tarih} itibarıyla kayıtlarıma göre aramızdaki hesap durumu şöyledir:",
      sizin: "• Bana olan borcunuz: {t}", benim: "• Size olan borcum: {t}",
      mutabakat: "Kayıtlarınız bununla uyuşuyorsa \"Onaylıyorum\" yazmanız yeterlidir; bir farklılık varsa lütfen bildirin. Teşekkür ederim.",
      hatirlat: "Umarım iyisinizdir. Kayıtlarıma göre {t} tutarındaki ödemeniz beklemededir. Uygun olduğunuz bir zamanda ödeyebilirseniz memnun olurum. Bir aksilik varsa haber vermeniz yeterli; birlikte kolaylık sağlarız.",
      kapandi: "{tarih} itibarıyla aramızdaki hesap kapanmıştır; kayıtlarıma göre karşılıklı borç kalmamıştır. Güzel muameleniz için teşekkür ederim, Allah bereket versin.",
      acikYok: "Kayıtlarıma göre aramızda açık bir hesap bulunmuyor.", selamlar: "Selamlarımla.", ve: " ve " },
    en: { selam: "Hello {ad},", selamYok: "Hello,", bakiyeBas: "According to my records, the balance between us as of {tarih} is as follows:",
      sizin: "• Amount you owe me: {t}", benim: "• Amount I owe you: {t}",
      mutabakat: "If this matches your records, simply reply \"Confirmed\"; if there is any difference, please let me know. Thank you.",
      hatirlat: "I hope you are well. According to my records, a payment of {t} is outstanding. I would appreciate it if you could settle it at your earliest convenience. If there is any difficulty, just let me know and we will find an arrangement together.",
      kapandi: "As of {tarih}, the account between us is settled; according to my records, neither of us owes the other anything. Thank you for the fair dealing; may God bless it.",
      acikYok: "According to my records, there is no open balance between us.", selamlar: "Kind regards.", ve: " and " },
    ar: { selam: "السلام عليكم {ad}،", selamYok: "السلام عليكم،", bakiyeBas: "وفقاً لسجلاتي، فإن الحساب بيننا حتى تاريخ {tarih} كما يلي:",
      sizin: "• المبلغ المستحق لي عليكم: {t}", benim: "• المبلغ المستحق لكم عليّ: {t}",
      mutabakat: "إذا كان ذلك مطابقاً لسجلاتكم فيكفي أن تكتبوا «أوافق»، وإن كان هناك أي اختلاف فأرجو إعلامي. وشكراً لكم.",
      hatirlat: "أرجو أن تكونوا بخير. وفقاً لسجلاتي، هناك دفعة مستحقة بمبلغ {t}. أكون شاكراً لو تفضلتم بسدادها في الوقت الذي يناسبكم. وإن كان هناك أي ظرف فيكفي إعلامي، ونتفق معاً على ما ييسّر الأمر.",
      kapandi: "اعتباراً من {tarih} أُغلق الحساب بيننا، ووفقاً لسجلاتي لم يبقَ لأيٍّ منا دين على الآخر. أشكركم على حسن المعاملة، بارك الله لكم.",
      acikYok: "وفقاً لسجلاتي، لا يوجد رصيد مفتوح بيننا.", selamlar: "مع خالص التحيات.", ve: " و" },
  };
  function mesajMetni(tur, dil, ad, bak, ben, tarih) {
    const L = MESAJ[dil] || MESAJ.tr;
    tarih = tarih || bugunTR();
    const acik = Object.entries(bak || {}).filter(([, b]) => Math.abs(b) >= 0.005);
    const s = [ad ? L.selam.replace("{ad}", ad) : L.selamYok, ""];
    if (tur === "hatirlat") {
      const borc = acik.filter(([, b]) => b > 0);
      if (borc.length) s.push(L.hatirlat.replace("{t}", borc.map(([c, b]) => tutarDil(b, c, dil)).join(L.ve)));
      else tur = "bakiye";
    }
    if (tur === "kapandi" || (tur === "bakiye" && !acik.length)) s.push(tur === "kapandi" ? L.kapandi.replace("{tarih}", tarih) : L.acikYok);
    else if (tur === "bakiye") {
      s.push(L.bakiyeBas.replace("{tarih}", tarih));
      for (const [c, b] of acik) s.push((b > 0 ? L.sizin : L.benim).replace("{t}", tutarDil(b, c, dil)));
      s.push("", L.mutabakat);
    }
    s.push("", L.selamlar);
    if (ben) s.push(ben);
    return s.join("\n");
  }
  function mesaj(pid) {
    const p = Store.person(pid); if (!p) return;
    const bal = bakiyeler(pid);
    const acikVar = Object.values(bal).some(b => Math.abs(b) >= 0.005);
    const tur = h("select", { class: "inp", "aria-label": t("Mesaj") },
      [["bakiye", "Bakiye bildirimi ve mutabakat"], ["hatirlat", "Kibar ödeme hatırlatması"], ["kapandi", "Hesap kapandı / teşekkür"]]
        .map(([k, l]) => h("option", { value: k, selected: k === (acikVar ? "bakiye" : "kapandi") }, t(l))));
    const dil = dilSec();
    const metin = h("textarea", { class: "inp mesaj-metin", rows: 12 });
    const yaz = () => { metin.value = mesajMetni(tur.value, dil.value, p.name, bal, A.ben); metin.dir = dil.value === "ar" ? "rtl" : "ltr"; };
    tur.onchange = yaz; dil.onchange = yaz; yaz();
    const wa = () => { const no = rakam(p.wa_phone || p.phone); const q = encodeURIComponent(metin.value); openUrl(no ? `https://wa.me/${no}?text=${q}` : `https://wa.me/?text=${q}`); };
    const tg = () => {
      kopyala(metin.value);
      const u = String(p.tg_user || "").trim();
      const url = u && (u.startsWith("@") || /[A-Za-z_]/.test(u)) ? "https://t.me/" + u.replace(/^@/, "") : (rakam(u || p.phone) ? "https://t.me/+" + rakam(u || p.phone) : "https://t.me/");
      toast(t("Mesaj panoya kopyalandı; Telegram'da sohbete yapıştırın (Ctrl+V)."));
      openUrl(url);
    };
    const entry = Sheets.open({ title: t("Mesaj / mutabakat") + " — " + p.name, cls: "form",
      body: h("div", { class: "form-grid" }, field(t("Mesaj"), tur), field(t("Dil"), dil), metin,
        h("small", { class: "muted" }, t("Metni dilediğiniz gibi düzeltebilirsiniz. Mutabakat mesajına karşı taraf “Onaylıyorum” diye cevap verirse hesaplarınız uyuşuyor demektir."))),
      footer: [btn("WhatsApp", "primary", wa), btn("Telegram", "light2", tg), btn(t("Kopyala"), "light2", () => toast(kopyala(metin.value) ? t("Kopyalandı") : t("Kopyalanamadı"))),
        btn(t("Kapat"), "light", () => Sheets.close(entry))] });
  }

  /* ---------------------------------------------------------------- borç senedi (masaüstü ekler_cekirdek.SENET ile aynı) */
  const SENET = {
    tr: { baslik: "BORÇ SENEDİ", ayet: "“Ey iman edenler! Belirli bir vadeye kadar birbirinize borçlandığınız zaman onu yazın…” (Bakara, 2/282)",
      metin: "Aşağıda imzası bulunan <b>{borclu}</b>, <b>{alacakli}</b> adlı kişiye <b>{tutar}</b>{yazi} borçlu olduğunu ve bu borcu <b>{vade}</b> tarihinde{yer} eksiksiz ödeyeceğini kabul ve beyan eder.",
      yazi: " (yazıyla: {y})", yer: ", {y} yoluyla", tarih: "Düzenlenme tarihi", vade: "Vade", tutar: "Tutar", aciklama: "Açıklama",
      borclu: "Borçlu", alacakli: "Alacaklı", katip: "Yazan (kâtip)", sahit: "Şahit", imza: "İmza", ad: "Ad Soyad", alt: "Bu senet iki nüsha düzenlenmiş, taraflarca okunup imzalanmıştır." },
    en: { baslik: "PROMISSORY NOTE (DEBT ACKNOWLEDGEMENT)", ayet: "“O you who believe! When you contract a debt for a fixed term, write it down…” (al-Baqarah, 2:282)",
      metin: "I, the undersigned <b>{borclu}</b>, acknowledge and declare that I owe <b>{alacakli}</b> the sum of <b>{tutar}</b>{yazi}, and that I will repay this debt in full on <b>{vade}</b>{yer}.",
      yazi: " (in words: {y})", yer: ", by {y}", tarih: "Date of issue", vade: "Due date", tutar: "Amount", aciklama: "Description",
      borclu: "Debtor", alacakli: "Creditor", katip: "Scribe (written by)", sahit: "Witness", imza: "Signature", ad: "Full name", alt: "This note has been drawn up in two copies, read and signed by the parties." },
    ar: { baslik: "سند دين", ayet: "﴿يَا أَيُّهَا الَّذِينَ آمَنُوا إِذَا تَدَايَنْتُمْ بِدَيْنٍ إِلَىٰ أَجَلٍ مُسَمًّى فَاكْتُبُوهُ﴾ (البقرة: 282)",
      metin: "يقرّ الموقّع أدناه <b>{borclu}</b> بأن في ذمته للسيد/ة <b>{alacakli}</b> مبلغاً قدره <b>{tutar}</b>{yazi}، ويتعهد بسداده كاملاً بتاريخ <b>{vade}</b>{yer}.",
      yazi: " (كتابةً: {y})", yer: "، عن طريق {y}", tarih: "تاريخ التحرير", vade: "تاريخ الاستحقاق", tutar: "المبلغ", aciklama: "البيان",
      borclu: "المدين", alacakli: "الدائن", katip: "الكاتب", sahit: "الشاهد", imza: "التوقيع", ad: "الاسم الكامل", alt: "حُرّر هذا السند من نسختين، وقرأه الطرفان ووقّعا عليه." },
  };
  function senetHtml(v, dil) {
    const L = SENET[dil] || SENET.tr, e = esc;
    const tutar = tutarDil(Number(v.tutar) || 0, v.cur || "USD", dil);
    const metin = L.metin.replace("{borclu}", e(v.borclu) || "…………").replace("{alacakli}", e(v.alacakli) || "…………").replace("{tutar}", e(tutar))
      .replace("{yazi}", v.yazi ? L.yazi.replace("{y}", e(v.yazi)) : "").replace("{vade}", e(v.vade) || "…………").replace("{yer}", v.yer ? L.yer.replace("{y}", e(v.yer)) : "");
    const dir = dil === "ar" ? "rtl" : "ltr";
    const kutu = (b, ad) => `<td><b>${e(b)}</b><br>${e(L.ad)}: ${e(ad)}<br><br>${e(L.imza)}:</td>`;
    return `<!DOCTYPE html><html dir="${dir}" lang="${dil}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">` +
      `<meta name="color-scheme" content="light"><title>${e(L.baslik)}</title><style>body{font-family:"Noto Sans Arabic","Segoe UI",Roboto,Arial,sans-serif;color:#111;background:#fff;margin:24px;line-height:1.6}` +
      `h1{text-align:center;letter-spacing:2px;font-size:20pt;margin:0 0 6px}.ayet{text-align:center;color:#06513f;font-size:11pt;margin-bottom:16px}` +
      `.metin{font-size:13pt;text-align:justify}table{width:100%;border-collapse:collapse;margin-top:12px}td{border:1px solid #888;padding:8px;vertical-align:top}` +
      `.imza td{width:33%;height:90px}.alt{color:#555;font-size:9.5pt;text-align:center;margin-top:14px}bdi{unicode-bidi:isolate}</style></head><body>` +
      `<h1>${e(L.baslik)}</h1><div class="ayet">${e(L.ayet)}</div><p class="metin">${metin}</p>` +
      `<table><tr><td><b>${e(L.tutar)}</b></td><td>${e(tutar)}</td><td><b>${e(L.tarih)}</b></td><td>${e(v.tarih)}</td></tr>` +
      `<tr><td><b>${e(L.vade)}</b></td><td>${e(v.vade)}</td><td><b>${e(L.aciklama)}</b></td><td>${e(v.aciklama)}</td></tr></table>` +
      `<table class="imza"><tr>${kutu(L.borclu, v.borclu)}${kutu(L.alacakli, v.alacakli)}${kutu(L.katip, v.katip)}</tr>` +
      `<tr>${kutu(L.sahit + " 1", v.sahit1)}${kutu(L.sahit + " 2", v.sahit2)}<td style="border:0"></td></tr></table>` +
      `<p class="alt">${e(L.alt)}</p></body></html>`;
  }
  const gTR = iso => (iso ? iso.slice(8, 10) + "." + iso.slice(5, 7) + "." + iso.slice(0, 4) : "");
  function senet(pid) {
    const p = pid ? Store.person(pid) : null;
    const bal = pid ? bakiyeler(pid) : {};
    const [c0, b0] = Object.entries(bal).find(([, b]) => Math.abs(b) >= 0.005) || ["USD", 0];
    const borclu = inp({ value: b0 >= 0 ? (p ? p.name : "") : A.ben });
    const alacakli = inp({ value: b0 >= 0 ? A.ben : (p ? p.name : "") });
    const tutar = inp({ inputmode: "decimal", dir: "ltr", value: amountInput(Math.abs(b0)) });
    const cur = curSel(c0);
    const yazi = inp({ placeholder: t("ör. bin beş yüz dolar") });
    const d = new Date(), ymd = x => `${x.getFullYear()}-${pad(x.getMonth() + 1)}-${pad(x.getDate())}`;
    const tarih = inp({ type: "date", dir: "ltr", value: ymd(d) });
    const v2 = new Date(d); v2.setMonth(v2.getMonth() + 1);
    const vade = inp({ type: "date", dir: "ltr", value: ymd(v2) });
    const yer = inp({ placeholder: t("ör. elden nakit, banka havalesi") });
    const katip = inp({}), s1 = inp({}), s2 = inp({}), aciklama = inp({});
    const dil = dilSec();
    const degis = btn("⇅", "light2 small", () => { const a = borclu.value; borclu.value = alacakli.value; alacakli.value = a; }, { title: t("Borçlu ile alacaklıyı yer değiştir") });
    const html = () => senetHtml({ borclu: borclu.value.trim(), alacakli: alacakli.value.trim(), tutar: parseAmount(tutar.value) || 0, cur: cur.value,
      yazi: yazi.value.trim(), tarih: gTR(tarih.value), vade: gTR(vade.value), yer: yer.value.trim(), katip: katip.value.trim(),
      sahit1: s1.value.trim(), sahit2: s2.value.trim(), aciklama: aciklama.value.trim() }, dil.value);
    const entry = Sheets.open({ title: t("Borç senedi"), cls: "form",
      body: h("div", { class: "form-grid" }, h("p", { class: "muted" }, t("Bakara 282'deki gibi: borç, vadesiyle birlikte yazılır; bir kâtip yazar ve iki şahit bulunur. Senedi yazdırıp taraflara imzalatın.")),
        field(t("Borçlu"), h("div", { class: "frow" }, borclu, degis)), field(t("Alacaklı"), alacakli),
        field(t("Tutar"), h("div", { class: "frow" }, tutar, cur)), field(t("Yazıyla (isteğe bağlı)"), yazi),
        h("div", { class: "two" }, field(t("Düzenlenme tarihi"), tarih), field(t("Vade"), vade)), field(t("Ödeme şekli (isteğe bağlı)"), yer),
        field(t("Yazan (kâtip)"), katip), h("div", { class: "two" }, field(t("1. şahit"), s1), field(t("2. şahit"), s2)),
        field(t("Açıklama"), aciklama), field(t("Senedin dili"), dil)),
      footer: [btn(t("PDF / Yazdır"), "gold", () => Statement.print(html(), "senet_" + stamp())),
        btn(t("Paylaş"), "primary", () => shareBlob(textToBlob(html(), "text/html"), "text/html", "senet_" + stamp() + ".html")),
        btn(t("Kapat"), "light", () => Sheets.close(entry))] });
  }

  /* ---------------------------------------------------------------- taksit planı */
  function taksitler(toplam, adet, ilk, aralik) {
    adet = Math.max(1, adet | 0);
    const pay = Math.round(toplam / adet * 100) / 100, out = [];
    for (let i = 0; i < adet; i++) {
      let d;
      if (aralik === "hafta") { d = new Date(ilk); d.setDate(d.getDate() + 7 * i); }
      else if (aralik === "15") { d = new Date(ilk); d.setDate(d.getDate() + 15 * i); }
      else { const y = ilk.getFullYear(), m = ilk.getMonth() + i; const son = new Date(y, m + 1, 0).getDate(); d = new Date(y, m, Math.min(ilk.getDate(), son), ilk.getHours(), ilk.getMinutes()); }
      out.push([dateToStr(d).slice(0, 16), i < adet - 1 ? pay : Math.round((toplam - pay * (adet - 1)) * 100) / 100]);
    }
    return out;
  }
  function taksit(pid) {
    if (!Store.persons().length) { Dlg.alert(t("Önce bir kişi ekleyin."), t("Kişi yok")); return; }
    const kisi = personSelect(pid, false);
    const bal = pid ? bakiyeler(pid) : {};
    const [c0, b0] = Object.entries(bal).find(([, b]) => Math.abs(b) >= 0.005) || ["USD", 0];
    const tur = seg([{ v: "TAHSIL", label: t("Tahsil edilecek (alınacak)") }, { v: "ODEME", label: t("Ödenecek (verilecek)") }], b0 < 0 ? "ODEME" : "TAHSIL", () => onizle(), "seg2");
    const cur = curSel(c0);
    const toplam = inp({ inputmode: "decimal", dir: "ltr", value: amountInput(Math.abs(b0)) });
    const adet = inp({ type: "number", min: 2, max: 120, value: 6, dir: "ltr" });
    const aralik = h("select", { class: "inp" }, [["ay", "Her ay"], ["15", "15 günde bir"], ["hafta", "Her hafta"]].map(([k, l]) => h("option", { value: k }, t(l))));
    const n = new Date(); n.setMonth(n.getMonth() + 1);
    const ilk = inp({ type: "datetime-local", step: 60, dir: "ltr", value: toInputDT(dateToStr(n)) });
    const notu = inp({});
    const on = h("div", { class: "hint" });
    const plan = () => taksitler(parseAmount(toplam.value) || 0, Number(adet.value) || 1, parseTs(fromInputDT(ilk.value)), aralik.value);
    const onizle = () => {
      const p = plan();
      ACIK++;
      try { clear(on).append(tf("{} taksit × {}", p.length, money(p[0][1], cur.value)), h("br"), p.slice(0, 3).map(([d, x]) => tsDisplay(d).slice(0, 10) + ": " + money(x, cur.value)).join("  ·  ") + (p.length > 3 ? "  …" : "")); }
      finally { ACIK--; }
    };
    [toplam, adet, aralik, ilk, cur].forEach(x => x.addEventListener("input", onizle));
    cur.addEventListener("change", onizle); aralik.addEventListener("change", onizle);
    let entry;
    const kaydet = async () => {
      const top = parseAmount(toplam.value);
      if (!(top > 0)) { await Dlg.alert(t("Toplam tutarı yazın."), t("Eksik")); return; }
      const p = plan();
      p.forEach(([due, x], i) => Store.addReminder({ person: kisi.value, kind: tur.get(), currency: cur.value, amount: x, due,
        note: tf("Taksit {}/{}", i + 1, p.length) + (notu.value.trim() ? " — " + notu.value.trim() : "") }));
      Sheets.close(entry); App.refresh(); Rem.scheduleAll(); toast(t("Kaydedildi"));
    };
    entry = Sheets.open({ title: t("Taksit / ödeme planı"), cls: "form",
      body: h("div", { class: "form-grid" }, h("p", { class: "muted" }, t("Toplam tutarı eşit taksitlere böler ve her taksit için bir hatırlatıcı kurar. Ödeme geldikçe “Aldım” / “Verdim” kaydını girip hatırlatıcıyı tamamlandı yapın.")),
        field(t("Kişi"), kisi), field(t("Tür"), tur.el), field(t("Para birimi"), cur), field(t("Toplam tutar"), toplam),
        h("div", { class: "two" }, field(t("Taksit sayısı"), adet), field(t("Sıklık"), aralik)), field(t("İlk taksit"), ilk), field(t("Not"), notu), on),
      footer: [btn(t("Vazgeç"), "light", () => Sheets.close(entry)), btn(t("Planı kaydet"), "primary", kaydet)] });
    onizle();
  }

  /* ---------------------------------------------------------------- hızlı kayıt (masaüstü hizli_ayristir ile aynı kurallar) */
  const L_ = "\\p{L}\\p{N}";
  const kucuk = s => String(s || "").replace(/I/g, "ı").replace(/İ/g, "i").toLowerCase();
  function sayiOku(s) {
    s = String(s || "").replace(/[\s'$₺£S]/g, "").replace(/٫/g, ".").replace(/٬/g, ",").replace(/[٠-٩]/g, d => "٠١٢٣٤٥٦٧٨٩".indexOf(d));
    if (!s) return null;
    const neg = s.startsWith("-"); s = s.replace(/^[+-]+/, "");
    const lc = s.lastIndexOf(","), ld = s.lastIndexOf(".");
    if (lc >= 0 && ld >= 0) { const dec = lc > ld ? "," : "."; s = s.split(dec === "," ? "." : ",").join("").replace(dec, "."); }
    else if (lc >= 0 || ld >= 0) {
      const p = s.split(lc >= 0 ? "," : ".");
      s = p.length > 2 || (p[1].length === 3 && p[0].length <= 3 && p[0] !== "" && p[0] !== "0") ? p.join("") : p[0] + "." + p[1];
    }
    if (!/^\d*\.?\d*$/.test(s) || s === "" || s === ".") return null;
    return neg ? -Number(s) : Number(s);
  }
  const CUR_K = [["SYP", /(suriye\s*lira|syrian\s*pound|ل\.?\s?س|ليرة\s*سورية|ليرات\s*سورية|(?<![\p{L}])syp(?![\p{L}])|£s)/u],
    ["TRY", /(türk\s*lira|turkish\s*lira|ليرة\s*تركية|ليرات\s*تركية|(?<![\p{L}])(tl|try)(?![\p{L}])|₺|(?<![\p{L}])lira)/u],
    ["USD", /(dolar|dollar|دولار|(?<![\p{L}])usd(?![\p{L}])|\$)/u], ["SYP", /(ليرة|ليرات)/u]];
  const TERS = [/(?<![\p{L}])paid me(?![\p{L}])/u, /(?<![\p{L}])gave me(?![\p{L}])/u, /(?<![\p{L}])returned(?![\p{L}])/u, /أعطاني/u, /دفع لي/u, /ردّ لي/u, /رد لي/u, /سدد/u];
  const YON = [["ALDIM", /(?<![\p{L}])(received|got|collected|borrowed|took)(?![\p{L}])/u], ["ALDIM", /(أخذت|استلمت|قبضت|استلفت|استدنت|اقترضت)/u],
    ["ALDIM", /(aldım|aldim|tahsil ettim|geri aldım|ödedi|ödemiş|verdi(?![\p{L}])|getirdi|borç aldım)/u],
    ["VERDIM", /(verdim|ödedim|odedim|borç verdim|gönderdim|yolladım)/u], ["VERDIM", /(?<![\p{L}])(gave|lent|paid|sent|loaned)(?![\p{L}])/u],
    ["VERDIM", /(أعطيت|دفعت|أقرضت|أرسلت|سلّمت|سلمت)/u]];
  const kelimeVar = (k, a) => new RegExp("(?<![" + L_ + "])" + a.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![" + L_ + "])", "u").test(k);
  function hizliAyristir(metin, kisiler) {
    const s = String(metin || "").trim();
    const k = kucuk(s.replace(/[٠-٩]/g, d => "٠١٢٣٤٥٦٧٨٩".indexOf(d)));
    const r = { ad: "", kisiId: null, direction: null, currency: null, amount: null, description: "" };
    const m = /(?<![\p{L}\p{N}])(\d{1,3}(?:[.,\s]\d{3})+(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?)(\s*(bin|k|thousand|ألف|الف))?/u.exec(k);
    if (m) { let v = sayiOku(m[1].replace(/\s/g, "")); if (v != null && m[3]) v *= 1000; r.amount = v ? Math.round(v * 100) / 100 : null; }
    for (const [c, re] of CUR_K) if (re.test(k)) { r.currency = c; break; }
    if (TERS.some(re => re.test(k))) r.direction = "ALDIM";
    else for (const [y, re] of YON) if (re.test(k)) { r.direction = y; break; }
    let en = null;
    for (const p of kisiler) { const a = kucuk(p.name).trim(); if (a && kelimeVar(k.replace(/’/g, "'"), a) && (!en || a.length > en.name.length)) en = p; }
    if (!en) for (const p of kisiler) { const ilk = kucuk(p.name).split(/\s+/)[0] || ""; if (ilk.length >= 3 && kelimeVar(k, ilk)) { en = p; break; } }
    if (en) { r.kisiId = en.id; r.ad = en.name; }
    else {
      let mm = /([A-ZÇĞİÖŞÜ][\p{L}]+(?:\s+[A-ZÇĞİÖŞÜ][\p{L}]+)?)\s*['’](?:y?[ea]|[dt][ea]n|n?[ıiuü]n)(?![\p{L}])/u.exec(s)
        || /(?<![\p{L}])(?:to|from|gave|lent|paid|pay)\s+([A-Z][\p{L}]+(?:\s+[A-Z][\p{L}]+)?)/u.exec(s)
        || /(?:^|\s)(?:من|إلى|الى|لـ)\s*([؀-ۿ]{2,})/u.exec(s)
        || /(?:أعطيت|دفعت|أقرضت|أرسلت|سلمت|سلّمت)\s+(?:ل)?([؀-ۿ]{2,})/u.exec(s)
        || /^([؀-ۿ]{2,})\s+(?:أعطاني|دفع|رد|ردّ|سدد)/u.exec(s);
      if (mm && /^(دولار|ليرة|ليرات|من|إلى)$/u.test(mm[1])) mm = null;
      if (mm) r.ad = mm[1].trim();
    }
    const d = /((?:[\p{L}]+\s+){0,1}[\p{L}]+)\s+için(?![\p{L}])/iu.exec(s) || /(?<![\p{L}])for\s+([\p{L}\s]{2,40})$/iu.exec(s) || /(?:ثمن|مقابل|لأجل|من أجل)\s+([؀-ۿ\s]{2,40})/u.exec(s);
    if (d) {
      let desc = d[1].split(/\s+/).filter(w => !/^(\d[\d.,]*|tl|usd|try|dolar\p{L}*|lira\p{L}*|verdim|aldım|aldim|ödedim|verdi|ödedi|aldı|borç|bin)$/u.test(kucuk(w))).join(" ");
      if (r.ad) desc = desc.split(/\s+/).filter(w => !kucuk(w).startsWith(kucuk(r.ad))).join(" ");
      r.description = desc.replace(/^[\s,.-]+|[\s,.-]+$/g, "");
    }
    return r;
  }
  function hizliKayit(metin) {
    const cumle = inp({ value: metin || "", placeholder: t("ör. Ahmet'e 500 TL verdim kira için"), autocomplete: "off" });
    const kisiler = Store.persons();
    const ad = inp({ autocomplete: "off", list: "hk-kisiler" });
    const dl = h("datalist", { id: "hk-kisiler" }, kisiler.map(p => h("option", { value: p.name })));
    const yon = seg([{ v: "VERDIM", label: t("Verdim (Çıktı)"), cls: "ver" }, { v: "ALDIM", label: t("Aldım (Girdi)"), cls: "al" }], "VERDIM", null, "seg2");
    const tutar = inp({ inputmode: "decimal", dir: "ltr" });
    const cur = curSel("USD");
    const aciklama = inp({});
    const uyari = h("div", { class: "hint", hidden: true });
    const kisiUyari = () => { const a = ad.value.trim(); const yeni = a && !kisiler.some(p => kucuk(p.name) === kucuk(a)); uyari.hidden = !yeni; uyari.textContent = tf("“{}” kayıtlı değil; kaydedince yeni kişi olarak eklenir.", a); };
    const ayr = () => {
      const r = hizliAyristir(cumle.value, kisiler);
      if (r.ad) ad.value = r.ad;
      if (r.direction) yon.set(r.direction);
      if (r.amount) tutar.value = amountInput(r.amount);
      if (r.currency) cur.value = r.currency;
      if (r.description) aciklama.value = r.description;
      kisiUyari();
    };
    cumle.addEventListener("input", ayr); ad.addEventListener("input", kisiUyari);
    let entry;
    const kaydet = async () => {
      const a = ad.value.trim();
      if (!a) { await Dlg.alert(t("Kişi adını yazın."), t("Eksik")); return; }
      const v = parseAmount(tutar.value);
      if (!(v > 0)) { await Dlg.alert(t("Tutarı yazın."), t("Eksik")); return; }
      let p = kisiler.find(x => kucuk(x.name) === kucuk(a));
      const pid = p ? p.id : Store.addPerson({ name: a });
      Store.addTx({ person: pid, ts: nowStr(), direction: yon.get(), currency: cur.value, amount: Math.round(v * 100) / 100, description: aciklama.value });
      Store.changed();
      Sheets.close(entry);
      const q = $("#hizli-inp"); if (q) q.value = "";
      App.select(pid); toast(t("Kaydedildi"));
    };
    entry = Sheets.open({ title: t("Hızlı kayıt"), cls: "form",
      body: h("div", { class: "form-grid" }, field(t("Yazın"), cumle, t("Örnekler: “Ali'den 200 dolar aldım” · “received 50$ from John” · “أعطيت محمد 100 دولار”. İnternet gerekmez; aşağıdaki alanları kontrol edip kaydedin.")),
        field(t("Kişi"), ad), dl, field(t("İşlem"), yon.el), field(t("Tutar"), h("div", { class: "frow" }, tutar, cur)), field(t("Açıklama"), aciklama), uyari),
      footer: [btn(t("Vazgeç"), "light", () => Sheets.close(entry)), btn(t("Kaydet"), "primary", kaydet)] });
    ayr();
    if (!metin) setTimeout(() => cumle.focus(), 60);
  }

  /* ---------------------------------------------------------------- raporlar */
  function rapor(kurlar, bugun) {
    bugun = bugun || new Date();
    const bak = new Map(), son = new Map(), aylik = { USD: {}, TRY: {}, SYP: {} };
    for (const r of Store.data.tx.values()) {
      if (r.del || !Store.person(r.person) || !CURRENCIES.includes(r.currency)) continue;
      const k = r.person + "|" + r.currency, a = Number(r.amount) || 0;
      bak.set(k, (bak.get(k) || 0) + (r.direction === "VERDIM" ? a : -a));
      if ((r.ts || "") > (son.get(k) || "")) son.set(k, r.ts || "");
      const ay = (r.ts || "").slice(0, 7), x = aylik[r.currency][ay] || (aylik[r.currency][ay] = [0, 0]);
      x[r.direction === "VERDIM" ? 0 : 1] += a;
    }
    const usd = (x, c) => (c === "USD" ? x : (Number(kurlar[c]) > 0 ? x / Number(kurlar[c]) : null));
    const ozet = {}, yas = {}, KOVA = ["0-30", "31-90", "91-180", "180+"];
    for (const c of CURRENCIES) { ozet[c] = { alacak: 0, verecek: 0, net: 0, ka: 0, kv: 0 }; yas[c] = { alacak: [0, 0, 0, 0], verecek: [0, 0, 0, 0] }; }
    const sat = [];
    for (const [k, b] of bak) {
      if (Math.abs(b) < 0.005) continue;
      const [pid, c] = k.split("|"), o = ozet[c];
      if (b > 0) { o.alacak += b; o.ka++; } else { o.verecek -= b; o.kv++; }
      const sd = parseTs((son.get(k) || "").slice(0, 10) + " 00:00"), gun = isNaN(sd) ? 0 : Math.floor((bugun - sd) / 864e5);
      yas[c][b > 0 ? "alacak" : "verecek"][gun <= 30 ? 0 : gun <= 90 ? 1 : gun <= 180 ? 2 : 3] += Math.abs(b);
      sat.push({ pid, ad: Store.personName(pid), cur: c, bakiye: b, gun, son: son.get(k) || "", usd: usd(b, c) });
    }
    for (const c of CURRENCIES) ozet[c].net = ozet[c].alacak - ozet[c].verecek;
    const sira = l => l.sort((a, b) => (b.usd != null ? Math.abs(b.usd) : Math.abs(b.bakiye) / 1e9) - (a.usd != null ? Math.abs(a.usd) : Math.abs(a.bakiye) / 1e9));
    let toplam = 0; const eksikKur = [];
    for (const c of CURRENCIES) { const u = usd(ozet[c].net, c); if (u == null) { if (Math.abs(ozet[c].net) >= 0.005) eksikKur.push(c); } else toplam += u; }
    const aylar = []; let y = bugun.getFullYear(), mo = bugun.getMonth() + 1;
    for (let i = 0; i < 12; i++) { aylar.unshift(`${y}-${pad(mo)}`); if (--mo === 0) { mo = 12; y--; } }
    const hareket = {}; for (const c of CURRENCIES) hareket[c] = aylar.map(a => [a, ...(aylik[c][a] || [0, 0])]);
    return { ozet, yas, KOVA, enAlacak: sira(sat.filter(s => s.bakiye > 0)).slice(0, 10), enVerecek: sira(sat.filter(s => s.bakiye < 0)).slice(0, 10),
      toplam, eksikKur, hareket, geciken: Store.reminders({ until: now16() }) };
  }
  function tablo(bas, satir, sag) {
    sag = sag || [];
    return h("div", { class: "rp-tablo-wrap" }, h("table", { class: "rp-tablo" }, h("thead", null, h("tr", null, bas.map(b => h("th", null, b)))),
      h("tbody", null, satir.map(s => h("tr", null, s.map((v, j) => h("td", { class: sag.includes(j) ? "n" : null, "data-l": bas[j] }, v)))))));
  }
  function raporlar() {
    const body = h("div", { class: "rapor" });
    const g = curSel("USD");
    const kur = {};
    const ciz = () => {
      clear(body);
      const r = rapor(A.kurlar);
      const kart = (bas, ...x) => body.appendChild(h("div", { class: "card rp-kart" }, h("h3", null, bas), x));
      kart(t("Genel durum"), tablo([t("Para birimi"), t("Alacak"), t("Verecek"), t("Net")], CURRENCIES.map(c => [t(CURRENCY_NAMES[c]), ltr(money(r.ozet[c].alacak, c)),
        ltr(money(r.ozet[c].verecek, c)), ltr(money(r.ozet[c].net, c))]), [1, 2, 3]),
      h("div", { class: "rp-kur" }, h("span", null, t("Kurlar (elle):")), ["TRY", "SYP"].map(c => {
        kur[c] = kur[c] || inp({ inputmode: "decimal", dir: "ltr", value: A.kurlar[c] ? amountInput(A.kurlar[c]) : "", placeholder: "0",
          onchange: e => { A.kurlar[c] = parseAmount(e.target.value) || 0; ayarYaz(A); ciz(); } });
        return h("label", { class: "rp-kur-l" }, ltr("1 $ = "), kur[c], ltr(" " + SYM[c]));
      })),
      h("p", { class: "rp-net" }, tf("Net durum (dolar karşılığı): {}", money(r.toplam, "USD")) + (r.eksikKur.length ? "  —  " + tf("{} için kur girilmediğinden hesaba katılmadı.", r.eksikKur.join(", ")) : "")));
      const ys = [];
      for (const c of CURRENCIES) for (const [k, ad] of [["alacak", t("Alacak")], ["verecek", t("Verecek")]]) {
        const d = r.yas[c][k]; if (d.some(x => Math.abs(x) >= 0.005)) ys.push([c, ad, ...d.map(x => (Math.abs(x) >= 0.005 ? ltr(money(x, c)) : "—"))]);
      }
      kart(t("Yaşlandırma (son hareketten bu yana geçen gün)"), h("p", { class: "muted" }, t("Açık bakiyeler, kişiyle o para biriminde yapılan son işlemden bu yana geçen süreye göre gruplanır. Uzun süredir hareketsiz alacaklar takip gerektirir.")),
        tablo([t("Para birimi"), t("Tür"), "0–30", "31–90", "91–180", "180+"], ys.length ? ys : [["—", "", "", "", "", ""]], [2, 3, 4, 5]));
      const bs = l => (l.length ? l.map(s => [s.ad, ltr(money(s.bakiye, s.cur)), (s.son || "").slice(0, 10) + " (" + tf("{} gün", s.gun) + ")"]) : [["—", "", ""]]);
      kart(t("En büyük bakiyeler"), h("h4", null, t("Alacaklı olduğum kişiler")), tablo([t("Kişi"), t("Bakiye"), t("Son işlem")], bs(r.enAlacak), [1]),
        h("h4", null, t("Borçlu olduğum kişiler")), tablo([t("Kişi"), t("Bakiye"), t("Son işlem")], bs(r.enVerecek), [1]));
      const hr = r.hareket[g.value], enb = Math.max(1, ...hr.map(x => Math.max(x[1], x[2])));
      kart(t("Aylık hareket (son 12 ay)"), g, h("div", { class: "rp-grafik", dir: "ltr" }, hr.map(([ay, v, a]) => h("div", { class: "rp-sut", title: ay + "  " + money(v, g.value) + " / " + money(a, g.value) },
        h("div", { class: "rp-bar" }, h("i", { class: "v", style: `height:${(v / enb) * 100}%` }), h("i", { class: "a", style: `height:${(a / enb) * 100}%` })),
        h("small", null, ay.slice(5, 7) + "." + ay.slice(2, 4))))),
      h("div", { class: "rp-lej" }, h("span", { class: "neg" }, "■ " + t("Verilen (Çıktı)")), "   ", h("span", { class: "pos" }, "■ " + t("Alınan (Girdi)"))));
      kart(t("Vadesi geçmiş hatırlatıcılar"), r.geciken.length ? tablo([t("Vade"), t("Kişi"), t("Tutar"), t("Not")],
        r.geciken.slice(0, 30).map(x => [ltr(tsDisplay(x.due)), Store.personName(x.person), x.amount ? ltr(money(x.amount, x.currency)) : x.currency, x.note || ""]), [2])
        : h("p", { class: "muted" }, t("Vadesi geçmiş hatırlatıcı yok.")));
    };
    g.onchange = ciz;
    const entry = Sheets.open({ title: t("Raporlar"), cls: "form wide-sheet", body, refresh: ciz,
      footer: [btn(t("Kayıtları CSV olarak dışa aktar"), "light2", () => csvKaydet("kayit")), btn(t("Bakiyeleri CSV olarak dışa aktar"), "light2", () => csvKaydet("bakiye")),
        btn(t("CSV'den içe aktar…"), "primary", csvIce), btn(t("Kapat"), "light", () => Sheets.close(entry))] });
    ciz();
  }

  /* ---------------------------------------------------------------- CSV */
  const CSV_BAS = { tr: ["Tarih", "Kişi", "İşlem", "Birim", "Tutar", "Açıklama"], en: ["Date", "Person", "Type", "Currency", "Amount", "Description"],
    ar: ["التاريخ", "الشخص", "العملية", "العملة", "المبلغ", "البيان"] };
  const ISLEM = { tr: { VERDIM: "Verdim", ALDIM: "Aldım" }, en: { VERDIM: "Gave", ALDIM: "Received" }, ar: { VERDIM: "أعطيت", ALDIM: "استلمت" } };
  const hucre = v => { v = String(v == null ? "" : v); return /[;"\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
  const sayiYaz = x => { const s = (Number(x) || 0).toFixed(2); return LANG === "tr" ? s.replace(".", ",") : s; };
  function csvDisa() {
    const out = [CSV_BAS[LANG] || CSV_BAS.tr];
    for (const r of Store.transactions({})) out.push([ts16(r.ts), Store.personName(r.person), (ISLEM[LANG] || ISLEM.tr)[r.direction], r.currency, sayiYaz(r.amount), r.description || ""]);
    return "﻿" + out.map(s => s.map(hucre).join(";")).join("\r\n") + "\r\n";
  }
  function csvBakiye() {
    const bas = { tr: ["Kişi", "Birim", "Verilen", "Alınan", "Bakiye"], en: ["Person", "Currency", "Given", "Received", "Balance"], ar: ["الشخص", "العملة", "المُعطى", "المأخوذ", "الرصيد"] };
    const out = [bas[LANG] || bas.tr];
    for (const p of Store.persons()) { const b = Store.balances(p.id); for (const c of CURRENCIES) if (b[c][0] || b[c][1]) out.push([p.name, c, sayiYaz(b[c][0]), sayiYaz(b[c][1]), sayiYaz(b[c][2])]); }
    return "﻿" + out.map(s => s.map(hucre).join(";")).join("\r\n") + "\r\n";
  }
  function csvKaydet(tur) {
    const ad = `bereket_${tur === "kayit" ? "kayitlar" : "bakiyeler"}_${stamp()}.csv`;
    saveBlobAs(textToBlob(tur === "kayit" ? csvDisa() : csvBakiye(), "text/csv"), "text/csv", ad);
    if (!bridgeHas("saveFile")) toast(tf("Kaydedildi: {}", ad));
  }
  function csvSatirlar(metin, ayrac) {
    const out = []; let s = [], v = "", q = false;
    for (let i = 0; i < metin.length; i++) {
      const ch = metin[i];
      if (q) { if (ch === '"') { if (metin[i + 1] === '"') { v += '"'; i++; } else q = false; } else v += ch; }
      else if (ch === '"') q = true;
      else if (ch === ayrac) { s.push(v); v = ""; }
      else if (ch === "\n" || ch === "\r") { if (ch === "\r" && metin[i + 1] === "\n") i++; s.push(v); out.push(s); s = []; v = ""; }
      else v += ch;
    }
    if (v || s.length) { s.push(v); out.push(s); }
    return out;
  }
  const ESLES = { tarih: ["tarih", "date", "التاريخ", "zaman", "time"], kisi: ["kişi", "kisi", "person", "name", "ad", "الشخص", "الاسم"],
    islem: ["işlem", "islem", "type", "direction", "العملية", "yön"], birim: ["birim", "currency", "para birimi", "العملة", "cur"],
    tutar: ["tutar", "amount", "miktar", "المبلغ"], aciklama: ["açıklama", "aciklama", "description", "note", "not", "البيان", "ملاحظة"] };
  const VER_K = ["verdim", "verilen", "çıktı", "cikti", "given", "gave", "out", "lent", "paid", "أعطيت", "دفعت", "صادر"];
  const AL_K = ["aldım", "aldim", "alınan", "alinan", "girdi", "received", "got", "in", "أخذت", "استلمت", "وارد", "قبضت"];
  const BIRIM = { USD: ["usd", "$", "dolar", "dollar", "دولار"], TRY: ["try", "tl", "₺", "türk lirası", "turkish lira", "ليرة تركية"], SYP: ["syp", "£s", "suriye lirası", "syrian pound", "ليرة سورية", "ل.س"] };
  function tarihOku(s) {
    s = String(s || "").trim();
    let m = /^(\d{4})[-/](\d{1,2})[-/](\d{1,2})(?:[ T](\d{1,2}):(\d{2}))?/.exec(s);
    if (m) return `${m[1]}-${pad(+m[2])}-${pad(+m[3])} ${pad(+(m[4] || 0))}:${m[5] || "00"}`;
    m = /^(\d{1,2})[./](\d{1,2})[./](\d{4})(?:\s+(\d{1,2}):(\d{2}))?/.exec(s);
    if (m) return `${m[3]}-${pad(+m[2])}-${pad(+m[1])} ${pad(+(m[4] || 0))}:${m[5] || "00"}`;
    return null;
  }
  function csvCozumle(metin) {
    metin = String(metin || "").replace(/^﻿/, "");
    const ilk = metin.split(/\r?\n/)[0] || "";
    const cnt = c => ilk.split(c).length - 1;
    const ayrac = ilk.includes(";") && cnt(";") >= Math.max(cnt(","), cnt("\t")) ? ";" : ilk.includes("\t") ? "\t" : ",";
    const r = csvSatirlar(metin, ayrac);
    const out = { satirlar: [], hatalar: [], yeniKisiler: new Set() };
    if (!r.length) return out;
    const bas = r[0].map(x => x.trim().toLowerCase());
    let idx = {};
    for (const k in ESLES) { const i = bas.findIndex(b => ESLES[k].includes(b)); if (i >= 0) idx[k] = i; }
    const basVar = Object.keys(idx).length >= 3;
    if (!basVar) idx = { tarih: 0, kisi: 1, islem: 2, birim: 3, tutar: 4, aciklama: 5 };
    const veri = basVar ? r.slice(1) : r;
    const mevcut = new Map(Store.persons().map(p => [kucuk(p.name.trim()), p.id]));
    const varOlan = new Set(Store.transactions({}).map(x => [kucuk(Store.personName(x.person).trim()), ts16(x.ts), x.direction, x.currency, (Math.round(x.amount * 100) / 100).toFixed(2)].join("|")));
    veri.forEach((sat, i) => {
      const no = i + (basVar ? 2 : 1);
      if (!sat.some(x => x.trim())) return;
      const al = k => (idx[k] != null && idx[k] < sat.length ? sat[idx[k]].trim() : "");
      const ts = tarihOku(al("tarih")), ad = al("kisi"), tutar = sayiOku(al("tutar")), b = kucuk(al("birim"));
      const cur = Object.keys(BIRIM).find(c => BIRIM[c].includes(b) || b.toUpperCase() === c) || null;
      const isl = kucuk(al("islem"));
      const yon = VER_K.includes(isl) || isl === "verdim" ? "VERDIM" : AL_K.includes(isl) ? "ALDIM" : (tutar != null && tutar < 0 ? "ALDIM" : (tutar != null && !isl ? "VERDIM" : null));
      const neden = !ts ? "tarih" : !ad ? "kisi" : (tutar == null || Math.abs(tutar) < 0.005) ? "tutar" : !cur ? "birim" : !yon ? "islem" : null;
      if (neden) { out.hatalar.push([no, neden]); return; }
      const amt = Math.round(Math.abs(tutar) * 100) / 100;
      const key = [kucuk(ad), ts, yon, cur, amt.toFixed(2)].join("|");
      const yin = varOlan.has(key); varOlan.add(key);
      if (!mevcut.has(kucuk(ad))) out.yeniKisiler.add(ad);
      out.satirlar.push({ ts, ad, direction: yon, currency: cur, amount: amt, description: al("aciklama"), yinelenen: yin });
    });
    return out;
  }
  function csvIceAl(coz) {
    const kisi = new Map(Store.persons().map(p => [kucuk(p.name.trim()), p.id]));
    let n = 0, yeni = 0;
    for (const s of coz.satirlar) {
      if (s.yinelenen) continue;
      const k = kucuk(s.ad.trim());
      if (!kisi.has(k)) { kisi.set(k, Store.addPerson({ name: s.ad.trim() })); yeni++; }
      Store.addTx({ person: kisi.get(k), ts: s.ts, direction: s.direction, currency: s.currency, amount: s.amount, description: s.description });
      n++;
    }
    Store.changed();
    return [n, yeni];
  }
  function csvIce() {
    const fi = h("input", { type: "file", hidden: true, accept: ".csv,.txt,text/csv,text/plain", onchange: async e => {
      const f = e.target.files[0]; fi.remove(); if (!f) return;
      const coz = csvCozumle(await f.text());
      const yeni = coz.satirlar.filter(s => !s.yinelenen), yin = coz.satirlar.length - yeni.length;
      let msg = tf("{} kayıt bulundu.", coz.satirlar.length) + "\n" + tf("Eklenecek: {} kayıt, {} yeni kişi.", yeni.length, coz.yeniKisiler.size);
      if (yin) msg += "\n" + tf("Zaten var olduğu için atlanacak: {}", yin);
      if (coz.hatalar.length) {
        const ned = { tarih: t("tarih okunamadı"), kisi: t("kişi boş"), tutar: t("tutar okunamadı"), birim: t("para birimi bilinmiyor"), islem: t("işlem (Verdim/Aldım) bilinmiyor") };
        msg += "\n\n" + t("Okunamayan satırlar:") + "\n" + coz.hatalar.slice(0, 12).map(([n, k]) => tf("Satır {}: {}", n, ned[k])).join("\n") + (coz.hatalar.length > 12 ? "\n…" : "");
      }
      msg += "\n\n" + t("Beklenen sütunlar: Tarih; Kişi; İşlem (Verdim/Aldım); Birim (USD/TRY/SYP); Tutar; Açıklama");
      if (!yeni.length) { Dlg.alert(msg, t("CSV'den içe aktar…")); return; }
      if (!(await Dlg.confirm(msg + "\n\n" + t("İçe aktarılsın mı?"), t("CSV'den içe aktar…")))) return;
      const [n, k] = csvIceAl(coz);
      await Dlg.alert(tf("{} kayıt ve {} yeni kişi eklendi.", n, k), t("CSV'den içe aktar…"));
      App.refresh(); Sheets.refreshAll();
    } });
    document.body.appendChild(fi); fi.click();
  }

  /* ---------------------------------------------------------------- geri al çubuğu */
  let geriT = 0;
  function geriAlGoster(metin, n) {
    let el = $("#geri-al");
    if (el) el.remove();
    const arsiv = (Store.meta.arsiv || []).length;
    el = h("div", { id: "geri-al", role: "status" }, h("span", null, metin), btn(t("Geri al"), "primary small", () => {
      let ok = true;
      for (let i = 0; i < n; i++) ok = Store.restore(0) && ok;
      el.remove(); App.refresh(); Sheets.refreshAll(); toast(ok ? t("Geri alındı") : t("Ayarlar → Arşiv'de de durur."));
    }), h("button", { type: "button", class: "icon-btn", "aria-label": t("Kapat"), onclick: () => el.remove() }, "✕"));
    el.dataset.n = arsiv;
    document.body.appendChild(el);
    clearTimeout(geriT); geriT = setTimeout(() => el.remove(), 10000);
  }
  const arsivN = () => (Store.meta.arsiv || []).length;
  const delTx = Store.deleteTx.bind(Store);
  Store.deleteTx = function (id) { const a = arsivN(); delTx(id); const n = Math.max(arsivN() - a, 0); if (n) setTimeout(() => geriAlGoster(t("Kayıt silindi"), n), 50); };
  const delP = Store.deletePerson.bind(Store);
  Store.deletePerson = function (pid) { const ad = Store.personName(pid), a = arsivN(); delP(pid); const n = Math.max(arsivN() - a, 0); if (n) setTimeout(() => geriAlGoster(tf("“{}” silindi", ad), n), 50); };

  /* ---------------------------------------------------------------- etiketler, gecikenler, boş durum (ana ekrana ekler) */
  const etiketler = p => String((p && p.tags) || "").split(/[,;،]/).map(x => x.trim()).filter(Boolean);
  let ETIKET = "";
  const personsAsil = Store.persons.bind(Store);
  Store.persons = function (search) {
    let r = personsAsil(search);
    const q = lower(search).trim();
    if (q) { const ids = new Set(r.map(p => p.id)); for (const p of personsAsil("")) if (!ids.has(p.id) && lower(p.tags).includes(q)) r.push(p); }
    if (this._etiketSuz && ETIKET) r = r.filter(p => etiketler(p).includes(ETIKET));
    return r;
  };
  const renderPersonsAsil = App.renderPersons.bind(App);
  App.renderPersons = function () {
    Store._etiketSuz = true;
    try { renderPersonsAsil(); } finally { Store._etiketSuz = false; }
    if (!this.plistEl) return;
    const hepsi = [...new Set(personsAsil("").flatMap(etiketler))].sort((a, b) => a.localeCompare(b, LANG));
    let bar = $("#etiket-bar");
    if (!hepsi.length) { if (bar) bar.remove(); ETIKET = ""; }
    else {
      if (!bar) { bar = h("div", { id: "etiket-bar", class: "etiket-bar" }); this.plistEl.parentNode.insertBefore(bar, this.plistEl); }
      if (ETIKET && !hepsi.includes(ETIKET)) ETIKET = "";
      clear(bar).append(...[["", t("🏷 Bütün etiketler")], ...hepsi.map(x => [x, "🏷 " + x])].map(([v, l]) =>
        h("button", { type: "button", class: "chip" + (ETIKET === v ? " on" : ""), onclick: () => { ETIKET = v; this.renderPersons(); } }, l)));
    }
    const gec = new Set(Store.reminders({ until: now16() }).map(r => r.person));
    this.plistEl.querySelectorAll(".prow[data-id]").forEach(el => {
      if (gec.has(el.dataset.id)) { const n = el.querySelector(".prow-name"); if (n && !n.textContent.startsWith("⏰")) { n.prepend("⏰ "); el.title = t("Vadesi geçmiş hatırlatıcı var"); } }
    });
  };
  const renderRecordsAsil = App.renderRecords.bind(App);
  App.renderRecords = function () {
    renderRecordsAsil();
    const e = this.recsEl && this.recsEl.querySelector(".empty");
    if (!e) return;
    const filtre = !!(this.f.text || this.f.cur || this.f.nodoc);
    e.textContent = !Store.persons().length ? t("Hoş geldiniz! Başlamak için “+ Kişi Ekle”ye basın ya da üstteki hızlı kayıt kutusuna “Ahmet'e 500 TL verdim” gibi yazın.")
      : filtre ? t("Süzgece uyan kayıt yok. Arama kutusunu ya da para birimi seçimini temizleyin.")
        : t("Bu sayfada henüz kayıt yok. “+ Verdim (Çıktı)” ya da “+ Aldım (Girdi)” ile ilk kaydı ekleyin.");
  };
  const buildAsil = App.build.bind(App);
  App.build = function () {
    buildAsil();
    // üst çubuk: tutarları gizle
    if (this.bellBtn && !$(".top-btn.goz")) this.bellBtn.after(h("button", { class: "icon-btn top-btn goz", type: "button", title: t("Tutarları gizle / göster"),
      "aria-label": t("Tutarları gizle / göster"), onclick: () => gizleDegistir(!A.gizle) }, h("span", { class: "emo" }, A.gizle ? "🙈" : "👁")));
    // hızlı kayıt kutusu
    const hero = $(".hero");
    if (hero && !$("#hizli-inp")) {
      const q = h("input", { id: "hizli-inp", class: "inp", type: "text", autocomplete: "off", placeholder: t("✦ Hızlı kayıt: ör. Ahmet'e 500 TL verdim"),
        "aria-label": t("Hızlı kayıt"), onkeydown: e => { if (e.key === "Enter") hizliKayit(q.value); } });
      hero.after(h("div", { class: "hizli-bar" }, q, btn(t("✦ Hızlı kayıt"), "primary", () => hizliKayit(q.value))));
    }
  };

  /* ---------------------------------------------------------------- ayarlar kartı */
  function ayarKarti(yenile) {
    const ui = FC.ui;
    const c = ui.card({ key: "bereket-guvenlik", title: t("Güvenlik ve otomatik yedek"), icon: "key",
      desc: t("PIN kilidi, tutarları gizleme ve her gün kendiliğinden alınan yedekler. Bu ayarlar yalnız bu telefonda geçerlidir.") });
    c.appendChild(h("p", { class: "card-desc" }, A.pin ? t("PIN kilidi: açık") : t("PIN kilidi: kapalı")));
    c.appendChild(ui.el("div.fc-row", null, [
      ui.el("button.btn.small.primary", { type: "button", html: ui.icon("key") + ui.esc(t("PIN belirle / değiştir")), onclick: () => pinForm(false) }),
      A.pin ? ui.el("button.btn.small", { type: "button", text: t("PIN'i kaldır"), onclick: () => pinForm(true) }) : null,
      A.pin ? ui.el("button.btn.small", { type: "button", text: t("Şimdi kilitle"), onclick: () => { Sheets.closeAll(); kilitle(); } }) : null].filter(Boolean)));
    const dk = h("select", { class: "inp", disabled: !A.pin, onchange: e => { A.kilitDk = Number(e.target.value); ayarYaz(A); } },
      [[0, "Yalnız açılışta kilitle"], [1, "1 dakika arka planda kalınca"], [5, "5 dakika arka planda kalınca"], [15, "15 dakika arka planda kalınca"], [30, "30 dakika arka planda kalınca"]]
        .map(([v, l]) => h("option", { value: v, selected: Number(A.kilitDk) === v }, t(l))));
    const chk = (label, on, fn) => h("label", { class: "chk" }, h("input", { type: "checkbox", checked: on, onchange: e => fn(e.target.checked) }), h("span", null, label));
    const son = otoYedekler()[0];
    const ben = inp({ value: A.ben || "", placeholder: t("Mesajların ve senetlerin altına yazılacak adınız"), onchange: e => { A.ben = e.target.value.trim(); ayarYaz(A); } });
    c.append(dk, chk(t("Tutarları gizle (ekranda ••••• görünür)"), A.gizle, v => gizleDegistir(v)),
      chk(t("Her gün otomatik yedek al"), A.otoYedek, v => { A.otoYedek = v; ayarYaz(A); if (v) otoYedek(); }),
      h("p", { class: "card-desc" }, son ? tf("Son yedek: {}", son.slice(9).split("-").reverse().join(".")) : t("Henüz yedek yok.")),
      ui.el("div.fc-row", null, [ui.el("button.btn.small", { type: "button", html: ui.icon("box") + ui.esc(t("Yedekleri gör / geri getir")), onclick: yedekler })]),
      field(t("Adınız"), ben));
    return c;
  }

  /* ---------------------------------------------------------------- başlangıç */
  document.addEventListener("DOMContentLoaded", () => setTimeout(() => { kilitle(); try { otoYedek(); } catch (e) { console.warn(e); } }, 0));
  // App.init depoyu açtıktan sonra yedek (Store.idb hazır olunca)
  const iv = setInterval(() => { if (Store.idb) { clearInterval(iv); try { otoYedek(); } catch (e) { console.warn(e); } } }, 1500);

  return { A, kilitle, mesaj, senet, taksit, raporlar, hizliKayit, yedekler, ayarKarti, otoYedek, gizleDegistir,
    // testler için
    _: { hizliAyristir, mesajMetni, senetHtml, taksitler, csvCozumle, csvDisa, rapor, sayiOku, pinKaydi, pinDogru, sha256, eksikler, anlik } };
})();
