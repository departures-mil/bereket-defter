/* Ana ekran: üst çubuk, Genel Durum, kişi listesi, kişi paneli, alt işlem çubuğu; pencere (sheet) sistemi. */
'use strict';

/* ------------------------------------------------------------------ pencereler (alt sayfa / modal) */
const Sheets = {
  stack: [],
  open({ title, body, footer, cls, onClose, refresh, dismissable }) {
    const entry = {};
    const closeBtn = h("button", { class: "icon-btn sheet-x", type: "button", "aria-label": t("Kapat"), title: t("Kapat"),
      onclick: () => this.close(entry) }, "✕");
    const bodyEl = h("div", { class: "sheet-body" }, body);
    const sheet = h("div", { class: "sheet", role: "dialog", "aria-modal": "true" },
      h("div", { class: "sheet-head" }, h("h3", { class: "sheet-title" }, title), closeBtn),
      bodyEl,
      footer ? h("div", { class: "sheet-foot" }, footer) : null);
    const wrap = h("div", { class: "sheet-wrap " + (cls || "") }, sheet);
    if (dismissable) wrap.addEventListener("click", e => { if (e.target === wrap) this.close(entry); });
    Object.assign(entry, { wrap, sheet, body: bodyEl, onClose, refresh });
    document.body.appendChild(wrap);
    document.body.classList.add("noscroll");
    this.stack.push(entry);
    requestAnimationFrame(() => wrap.classList.add("in"));
    return entry;
  },
  close(entry) {
    entry = entry || this.stack[this.stack.length - 1];
    const i = this.stack.indexOf(entry);
    if (i < 0) return;
    this.stack.splice(i, 1);
    entry.wrap.remove();
    if (!this.stack.length) document.body.classList.remove("noscroll");
    if (entry.onClose) { try { entry.onClose(); } catch (e) { console.warn(e); } }
  },
  closeAll() { while (this.stack.length) this.close(); },
  top() { return this.stack[this.stack.length - 1] || null; },
  refreshAll() { for (const s of this.stack) if (s.refresh) { try { s.refresh(); } catch (e) { console.warn(e); } } },
};

const Dlg = {
  _box(title, msg, buttons, cls) {
    return new Promise(resolve => {
      let done = false;
      const finish = v => { if (done) return; done = true; Sheets.close(entry); resolve(v); };
      const foot = buttons.map(b => h("button", { type: "button", class: "btn " + (b.cls || ""), onclick: () => finish(b.v) }, b.label));
      const entry = Sheets.open({ title: title || "", cls: "dialog " + (cls || ""), body: h("div", { class: "dlg-msg" }, msg),
        footer: foot, onClose: () => { if (!done) { done = true; resolve(buttons[0].v === true ? false : buttons[0].v); } } });
      setTimeout(() => { const last = entry.sheet.querySelector(".sheet-foot .btn:last-child"); if (last) last.focus(); }, 30);
    });
  },
  alert(msg, title) { return this._box(title || "", msg, [{ label: t("Tamam"), v: true, cls: "primary" }]); },
  confirm(msg, title, opt) {
    opt = opt || {};
    return this._box(title || "", msg, [{ label: opt.no || t("Hayır"), v: false, cls: "light" },
      { label: opt.yes || t("Evet"), v: true, cls: opt.danger ? "danger" : "primary" }]);
  },
  /** küçük işlem menüsü: [{label, icon (Node), fn, cls}] */
  menu(items, title) {
    const entry = Sheets.open({ title: title || "", cls: "dialog menu", dismissable: true,
      body: h("div", { class: "menu-list" }, items.map(it => h("button", { type: "button", class: "menu-item " + (it.cls || ""),
        onclick: () => { Sheets.close(entry); it.fn(); } }, it.icon || null, h("span", null, it.label)))) });
    return entry;
  },
};

function toast(text) {
  let el = $("#toast");
  if (!el) { el = h("div", { id: "toast", role: "status" }); document.body.appendChild(el); }
  el.textContent = text;
  el.classList.add("show");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => el.classList.remove("show"), 2600);
}

/* ------------------------------------------------------------------ hatırlatıcılar */
function now16() { return nowStr().slice(0, 16); }
function today2359() { return nowStr().slice(0, 10) + " 23:59"; }
function reminderState(r) {
  if (r.done) return ["done", t("Tamamlandı"), "#556"];
  const n = now16();
  if (ts16(r.due) <= n) return ["late", t("Vakti geldi / gecikti"), RED];
  if (r.due.slice(0, 10) === n.slice(0, 10)) return ["today", t("Bugün"), "#d97a00"];
  return ["soon", t("Yaklaşan"), GREEN];
}
function reminderAmt(r) { return r.amount ? money(r.amount, r.currency) : r.currency; }
function reminderText(r) {
  return `${tsDisplay(r.due)} — ${Store.personName(r.person)}: ${t(KIND_TEXT[r.kind])} ${reminderAmt(r)}`;
}
const Rem = {
  notified: new Set(),
  sched() { try { return JSON.parse(localStorage.getItem("bereket_sched") || "[]"); } catch (e) { return []; } },
  saveSched(ids) { try { localStorage.setItem("bereket_sched", JSON.stringify(ids)); } catch (e) { /* yok */ } },
  /** Android bildirimleri: bekleyen her hatırlatıcı için kur, kalmayanları iptal et */
  scheduleAll() {
    const b = bridge();
    if (!b || typeof b.scheduleReminder !== "function") return;
    const now = Date.now();
    const keep = [];
    for (const r of Store.reminders({ pendingOnly: true })) {
      const when = parseTs(r.due).getTime();
      if (!(when > now)) continue;     // vakti geçmişler uygulama içinde listelenir
      const text = `${Store.personName(r.person)}: ${t(KIND_TEXT[r.kind])} ${reminderAmt(r)}` + (r.note ? " — " + r.note : "");
      try { b.scheduleReminder(String(r.id), Number(when), t("🔔 Hatırlatıcı") + " " + tsDisplay(r.due), text); keep.push(r.id); } catch (e) { console.warn(e); }
    }
    for (const id of this.sched()) if (!keep.includes(id) && typeof b.cancelReminder === "function") {
      try { b.cancelReminder(String(id)); } catch (e) { console.warn(e); }
    }
    this.saveSched(keep);
  },
  cancel(id) {
    const b = bridge();
    if (b && typeof b.cancelReminder === "function") { try { b.cancelReminder(String(id)); } catch (e) { console.warn(e); } }
  },
  due() { return Store.reminders({ until: now16() }); },
  check(notify) {
    const due = this.due();
    const fresh = due.filter(r => !this.notified.has(r.id));
    for (const r of fresh) this.notified.add(r.id);
    if (notify && fresh.length) {
      let text = fresh.slice(0, 5).map(reminderText).join("   •   ");
      if (fresh.length > 5) text += "   •   …";
      App.banner(text);
      try { if (navigator.vibrate) navigator.vibrate([180, 80, 180]); } catch (e) { /* yok */ }
    }
    App.updateBell();
  },
};

/* ------------------------------------------------------------------ uygulama */
const App = {
  sel: null, view: "list", search: "",
  f: { cur: "", text: "", nodoc: false },
  wideMq: window.matchMedia("(min-width: 800px)"),
  isWide() { return this.wideMq.matches; },

  async init() {
    applyLangToDocument();
    try {
      await Store.open();
      await Store.load();
    } catch (e) {
      document.body.appendChild(h("div", { class: "fatal" }, t("Veritabanı açılamadı.") + " " + (e && e.message || "")));
      return;
    }
    Store.onChange.push(() => { Sync.runSoon(3000); Rem.scheduleAll(); });
    Sync.listeners.push(() => this.renderSyncBtn());
    this.build();
    this.wideMq.addEventListener ? this.wideMq.addEventListener("change", () => this.applyView())
      : this.wideMq.addListener(() => this.applyView());
    Rem.check(false);
    Rem.scheduleAll();
    setInterval(() => Rem.check(true), 30000);
    setInterval(() => { QUOTE_I = (QUOTE_I + 1) % QUOTES.length; const q = $("#quote"); if (q) q.textContent = t(QUOTES[QUOTE_I]); }, 10000);
    setInterval(() => this.renderClock(), 15000);
    setTimeout(() => {
      if (Store.reminders({ until: today2359() }).length && !Sheets.stack.length) Forms.reminders({ dueOnly: true });
    }, 600);
    if (Sync.signedIn()) { Sync.start(); Sync.runSoon(400); }
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "visible") { Rem.check(true); if (Sync.signedIn()) Sync.runSoon(200); }
    });
    window.onAndroidBack = () => this.back();
    window.onAndroidReminder = id => {
      Rem.check(false); if (Viewer.active) Viewer.close(); Sheets.closeAll(); Forms.reminders({ dueOnly: true }); };
    window.onAndroidSaved = ok => { if (ok === true || ok === "true") toast(t("Kaydedildi")); };
  },

  back() {
    if (Viewer.active) { Viewer.close(); return true; }
    if (Sheets.stack.length) { Sheets.close(); return true; }
    if (!this.isWide() && this.view === "person") { this.showList(); return true; }
    return false;
  },

  /* ---------------- iskelet */
  build() {
    const app = clear($("#app"));
    document.title = t(APP_TITLE);
    const ver = appVersion();
    this.bellBadge = h("span", { class: "badge", hidden: true });
    this.bellBtn = h("button", { class: "icon-btn top-btn bell", type: "button", "aria-label": t("🔔 Hatırlatıcılar"), title: t("🔔 Hatırlatıcılar"),
      onclick: () => Forms.reminders({}) }, h("span", { class: "emo" }, "🔔"), this.bellBadge);
    // sağ üst: ortak çekirdek üst çubuğu (Eşitle · Wi‑Fi · Güncelle · tema · dil | Tam ekran · Kapat) — js/kabuk.js bağlar
    const top = h("header", { class: "topbar" },
      h("img", { class: "logo", src: "assets/logo.svg", alt: "", width: 40, height: 40 }),
      h("div", { class: "ttl" }, h("div", { class: "ttl-main" }, t(APP_TITLE)), h("div", { class: "ttl-ver" }, ltr("v" + ver))),
      this.bellBtn,
      h("button", { class: "icon-btn top-btn", type: "button", "aria-label": t("Menü"), title: t("Menü"), onclick: () => Forms.menu() },
        h("span", { class: "emo burger" }, "☰")));
    this.topEl = top;
    this.bannerEl = h("div", { class: "banner", hidden: true, role: "alert", onclick: () => { this.bannerEl.hidden = true; Forms.reminders({ dueOnly: true }); } });
    const hero = h("div", { class: "hero" },
      h("div", { id: "quote", class: "quote" }, t(QUOTES[QUOTE_I])),
      h("div", { id: "clock", class: "clock" }));

    // sol: Genel Durum + kişiler
    this.sumEl = h("div", { class: "tiles sum-tiles" });
    this.searchEl = h("input", { type: "search", class: "inp", placeholder: t("🔍 Kişi ara…"), value: this.search, "aria-label": t("Kişi ara"),
      oninput: e => { this.search = e.target.value; this.renderPersons(); } });
    this.plistEl = h("div", { class: "plist", role: "list" });
    const listBar = h("div", { class: "bar bar-list" },
      h("button", { class: "btn danger only-phone", type: "button", onclick: () => this.addTx("VERDIM") }, t("+ Verdim (Çıktı)")),
      h("button", { class: "btn primary only-phone", type: "button", onclick: () => this.addTx("ALDIM") }, t("+ Aldım (Girdi)")),
      h("button", { class: "btn light2", type: "button", onclick: () => Forms.person(null) }, t("+ Kişi Ekle")),
      h("button", { class: "btn light2", type: "button", onclick: () => Forms.book() }, t("📒 Kişi Defteri")));
    const left = h("section", { class: "pane pane-list" },
      h("div", { class: "card summary" }, h("h2", null, t("Genel\nDurum").replace(/\n/g, " ")), this.sumEl),
      h("div", { class: "card persons" }, h("h2", null, t("Kişiler")), this.searchEl, this.plistEl),
      listBar);

    // sağ: kişi paneli
    this.pheadEl = h("div", { class: "phead" });
    this.ptilesEl = h("div", { class: "tiles p-tiles" });
    const curSel = h("select", { class: "inp", "aria-label": t("Para birimi"), onchange: e => { this.f.cur = e.target.value; this.renderRecords(); } },
      h("option", { value: "" }, t("Tüm para birimleri")),
      CURRENCIES.map(c => h("option", { value: c, selected: this.f.cur === c }, t(CURRENCY_NAMES[c]))));
    curSel.value = this.f.cur;
    const nodoc = h("label", { class: "chk" }, h("input", { type: "checkbox", checked: this.f.nodoc,
      onchange: e => { this.f.nodoc = e.target.checked; this.renderRecords(); } }), h("span", null, t("Sadece belgesiz kayıtlar")));
    const ftext = h("input", { type: "search", class: "inp", placeholder: t("Açıklamada ara…"), value: this.f.text, "aria-label": t("Açıklamada ara…"),
      oninput: e => { this.f.text = e.target.value; this.renderRecords(); } });
    this.recsEl = h("div", { class: "recs", role: "list" });
    this.recCountEl = h("div", { class: "rec-count muted" });
    const personBar = h("div", { class: "bar bar-person" },
      h("button", { class: "btn danger", type: "button", onclick: () => this.addTx("VERDIM") }, t("+ Verdim (Çıktı)")),
      h("button", { class: "btn primary", type: "button", onclick: () => this.addTx("ALDIM") }, t("+ Aldım (Girdi)")),
      h("button", { class: "btn light2", type: "button", onclick: () => this.addReminder() }, t("🔔 Hatırlatıcı Ekle")),
      h("button", { class: "btn gold", type: "button", onclick: () => Forms.statement(this.pid()) }, t("📄 Döküm Al")));
    const right = h("section", { class: "pane pane-person" },
      h("div", { class: "card person" }, this.pheadEl, this.ptilesEl,
        h("div", { class: "filters" }, h("div", { class: "frow" }, curSel, nodoc), ftext),
        this.recCountEl, this.recsEl),
      personBar);

    app.append(top, this.bannerEl, hero, h("main", { class: "main" }, left, right));
    this.renderClock();
    if (window.Kabuk) Kabuk.ustCubuk(top);
    this.renderSyncBtn();
    this.applyView();
    this.refresh();
  },
  renderClock() {
    const c = $("#clock");
    if (!c) return;
    const n = new Date();
    clear(c).append(dayName(n) + ", ", ltr(`${pad(n.getDate())}.${pad(n.getMonth() + 1)}.${n.getFullYear()}  ${hhmm(n)}`));
  },
  /** ☁ Eşitle: giriş yapılmışsa hemen eşitler, yapılmamışsa eşitleme ekranını açar. */
  async syncNow() {
    if (!Sync.signedIn()) { Forms.sync(); return; }
    if (Sync.running) { toast(t("Eşitleniyor…")); return; }
    Sync.start();
    await Sync.run();
    toast(Sync.lastErr ? Sync.lastErr : t("Eşitlendi ✓"));
  },
  renderSyncBtn() {
    if (window.Kabuk) Kabuk.esitleDurum();
    Sheets.stack.forEach(s => s.syncStatus && s.syncStatus());
  },
  applyView() {
    const wide = this.isWide();
    if (wide && !this.sel) this.sel = "ALL";
    document.body.classList.toggle("wide", wide);
    document.body.classList.toggle("view-person", !wide && this.view === "person");
    document.body.classList.toggle("view-list", wide || this.view !== "person");
    if (wide || this.view === "person") this.renderPerson();
  },
  pid() { return this.sel && this.sel !== "ALL" ? this.sel : null; },
  showList() {
    this.view = "list";
    this.applyView();
    window.scrollTo(0, this._listScroll || 0);
  },
  select(id) {
    if (!this.isWide() && this.view === "list") this._listScroll = window.scrollY;
    this.sel = id;
    this.view = "person";
    this.applyView();
    this.renderPersons();
    if (!this.isWide()) window.scrollTo(0, 0);
  },
  refresh() {
    if (!this.sumEl) return;
    if (this.sel && this.sel !== "ALL" && !Store.person(this.sel)) {
      this.sel = this.isWide() ? "ALL" : null;
      if (!this.isWide()) this.view = "list";
      this.applyView();
    }
    this.renderSummary();
    this.renderPersons();
    if (this.isWide() || this.view === "person") this.renderPerson();
    this.updateBell();
  },
  onRemoteChange() {
    this.refresh();
    Sheets.refreshAll();
    Rem.scheduleAll();
    Rem.check(true);
  },
  banner(text) {
    clear(this.bannerEl).append("🔔  " + text);
    this.bannerEl.hidden = false;
    clearTimeout(this._bt);
    this._bt = setTimeout(() => { this.bannerEl.hidden = true; }, 20000);
  },
  updateBell() {
    if (!this.bellBtn) return;
    const n = Store.reminders({ until: today2359() }).length;
    const late = Rem.due().length > 0;
    this.bellBadge.hidden = !n;
    this.bellBadge.textContent = n > 99 ? "99+" : String(n);
    this.bellBtn.classList.toggle("late", late);
  },

  /* ---------------- Genel Durum ve kişiler */
  renderSummary() {
    clear(this.sumEl);
    const tot = Store.totalsOverall();
    for (const c of CURRENCIES) {
      const [a, v] = tot[c];
      this.sumEl.append(h("div", { class: "tile" },
        h("div", { class: "tile-cur" }, t(CURRENCY_NAMES[c])),
        h("div", { class: "tile-vals" },
          h("div", { class: "tile-main pos" }, t("Alacak") + " ", ltr(money(a, c))),
          h("div", { class: "tile-sub neg" }, t("Verecek") + " ", ltr(money(v, c))))));
    }
  },
  balanceParts(pid) {
    const bal = Store.balances(pid);
    const parts = [];
    for (const c of CURRENCIES) {
      const b = bal[c][2];
      if (Math.abs(b) >= 0.005) parts.push(ltr((b > 0 ? "+" : "") + money(b, c), b > 0 ? "pos" : "neg"));
    }
    return parts;
  },
  renderPersons() {
    if (!this.plistEl) return;
    clear(this.plistEl);
    const all = h("button", { type: "button", role: "listitem", class: "prow all" + (this.sel === "ALL" ? " sel" : ""),
      onclick: () => this.select("ALL") }, h("div", { class: "prow-name" }, t("★  Tüm kişiler")),
      h("div", { class: "prow-bal muted" }, t("Bütün kişilerin kayıtları")));
    this.plistEl.append(all);
    const rows = Store.persons(this.search);
    for (const p of rows) {
      const parts = this.balanceParts(p.id);
      const chs = activeChannels(p);
      this.plistEl.append(h("button", { type: "button", role: "listitem", class: "prow" + (this.sel === p.id ? " sel" : ""), "data-id": p.id,
        onclick: () => this.select(p.id) },
        h("div", { class: "prow-top" }, h("span", { class: "prow-name" }, p.name),
          chs.length ? h("span", { class: "prow-ch" }, chs.map(c => channelIcon(c, true, 22))) : null),
        h("div", { class: "prow-bal" }, parts.length ? parts.map((x, i) => [i ? "  " : "", x]) : h("span", { class: "muted" }, t("Hesap kapalı")))));
    }
    if (!rows.length) this.plistEl.append(h("div", { class: "empty" }, this.search ? t("Kişi bulunamadı.") : t("Henüz kişi yok. “+ Kişi Ekle” ile başlayın.")));
  },

  /* ---------------- kişi paneli */
  renderPerson() {
    if (!this.pheadEl) return;
    const pid = this.pid();
    const p = pid ? Store.person(pid) : null;
    clear(this.pheadEl);
    const back = h("button", { class: "icon-btn back only-phone", type: "button", "aria-label": t("Geri"), title: t("Geri"), onclick: () => this.showList() },
      h("span", { class: "flip" }, "←"));
    let bal;
    if (!p) {
      this.pheadEl.append(h("div", { class: "phead-row" }, back,
        h("div", { class: "pname-wrap" }, h("h2", { class: "pname" }, t("Tüm kişiler")))),
        h("div", { class: "pinfo muted" }, t("Bütün kişilerin kayıtları")));
      bal = Store.balances(null);
    } else {
      const chbar = h("div", { class: "chbar" }, CHANNELS.map(ch => {
        const on = !!p["ch_" + ch];
        return h("button", { type: "button", class: "chbtn" + (on ? " on" : ""), "data-ch": ch,
          title: t(CH_NAMES[ch]) + " — " + (on ? t("açık: tıklayınca açılır") : t("kapalı: açmak için tıklayın")),
          "aria-label": t(CH_NAMES[ch]) + " — " + (on ? t("açık") : t("kapalı")),
          onclick: () => this.channelClick(p.id, ch) }, channelIcon(ch, on, 34));
      }));
      const info = [p.phone, p.phone2, p.email, p.address, p.note].filter(Boolean).map(x => /^[+\d\s()-]+$/.test(x) ? ltr(x) : x);
      const nxt = Store.reminders({ pid: p.id })[0];
      const infoEl = h("div", { class: "pinfo muted" }, info.map((x, i) => [i ? " • " : "", x]));
      this.pheadEl.append(h("div", { class: "phead-row" }, back,
        h("div", { class: "pname-wrap" }, h("h2", { class: "pname" }, p.name), chbar)), infoEl);
      if (nxt) this.pheadEl.append(h("div", { class: "pnext", onclick: () => Forms.reminders({ pid: p.id }) },
        "🔔 " + t("Sıradaki hatırlatıcı") + ": ", ltr(tsDisplay(nxt.due)), " — " + t(KIND_TEXT[nxt.kind]),
        nxt.amount ? [" ", ltr(money(nxt.amount, nxt.currency))] : null));
      this.pheadEl.append(h("div", { class: "pactions" },
        h("button", { class: "btn small light2", type: "button", onclick: () => Forms.person(Store.person(p.id)) }, "✎ " + t("Düzenle")),
        h("button", { class: "btn small light2", type: "button", onclick: () => Forms.reminders({ pid: p.id }) }, t("🔔 Hatırlatıcılar")),
        h("button", { class: "btn small danger", type: "button", onclick: () => this.deletePerson(p.id) }, t("Sil"))));
      bal = Store.balances(p.id);
    }
    clear(this.ptilesEl);
    for (const c of CURRENCIES) {
      const [v, a, b] = bal[c];
      let main;
      if (Math.abs(b) < 0.005) main = h("div", { class: "tile-main zero" }, t("Hesap kapalı") + "  ", ltr("0 " + CURRENCY_SYMBOLS[c]));
      else if (b > 0) main = h("div", { class: "tile-main pos" }, t("Alacak") + ": ", ltr(money(b, c)));
      else main = h("div", { class: "tile-main neg" }, t("Verecek") + ": ", ltr(money(-b, c)));
      this.ptilesEl.append(h("div", { class: "tile" }, h("div", { class: "tile-cur" }, t(CURRENCY_NAMES[c])), main,
        h("div", { class: "tile-sub muted" }, t("Verilen") + " ", ltr(money(v, c)), "  •  " + t("Alınan") + " ", ltr(money(a, c)))));
    }
    this.renderRecords();
  },
  renderRecords() {
    if (!this.recsEl) return;
    const pid = this.pid();
    let rows = Store.transactions({ pid, currency: this.f.cur, text: this.f.text }).reverse();
    if (this.f.nodoc) rows = rows.filter(r => !Store.docCount(r.id));
    clear(this.recsEl);
    this.recCountEl.textContent = tf("{} kayıt", rows.length);
    const LIMIT = this._recLimit || 200;
    for (const r of rows.slice(0, LIMIT)) this.recsEl.append(this.recordCard(r, !pid));
    if (rows.length > LIMIT) this.recsEl.append(h("button", { class: "btn light2 more", type: "button",
      onclick: () => { this._recLimit = LIMIT + 300; this.renderRecords(); } }, tf("Daha fazla göster ({})", rows.length - LIMIT)));
    if (!rows.length) this.recsEl.append(h("div", { class: "empty" }, t("Kayıt yok.")));
  },
  recordCard(r, showPerson) {
    const ver = r.direction === "VERDIM";
    const n = Store.docCount(r.id);
    return h("button", { type: "button", role: "listitem", class: "rec " + (ver ? "ver" : "al"), "data-id": r.id, onclick: () => Forms.txDetail(r.id) },
      h("div", { class: "rec-top" }, ltr(tsDisplay(r.ts), "rec-ts"),
        n ? h("span", { class: "doc-n", title: t("📎 Belgeler") }, "📎 " + n)
          : h("span", { class: "doc-warn", title: t("Bu kaydın dekontu / belgesi yok") }, "⚠")),
      showPerson ? h("div", { class: "rec-person" }, Store.personName(r.person)) : null,
      h("div", { class: "rec-mid" },
        h("span", { class: "rec-dir" }, (ver ? t("Verdim") : t("Aldım")) + " · " + r.currency,
          h("small", { class: "muted" }, " (" + (ver ? t("Verilen (Çıktı)") : t("Alınan (Girdi)")) + ")")),
        ltr(money(r.amount, r.currency), "rec-amt")),
      (r.description || r.updated_at) ? h("div", { class: "rec-desc" }, r.description || "", r.updated_at ? h("span", { class: "edited", title: t("Değişiklik Geçmişi") }, "  ✎") : null) : null);
  },

  /* ---------------- işlemler */
  channelClick(pid, ch) {
    const p = Store.person(pid);
    if (!p) return;
    if (!p["ch_" + ch]) { Store.setChannel(pid, ch, true); this.refresh(); return; }
    Dlg.menu([
      { icon: channelIcon(ch, true, 28), label: t(CH_OPEN[ch]), fn: () => openChannel(Store.person(pid), ch) },
      { icon: channelIcon(ch, false, 28), label: t("Bu simgeyi kapat"), fn: () => { Store.setChannel(pid, ch, false); this.refresh(); } },
      { icon: h("span", { class: "mi-emo" }, "✎"), label: t("Kişi bilgilerini düzenle…"), fn: () => Forms.person(Store.person(pid)) },
    ], t(CH_NAMES[ch]) + " — " + p.name);
  },
  async deletePerson(pid) {
    const p = Store.person(pid);
    if (!p) return;
    const n = Store.txCount(pid);
    let msg = tf("'{}' silinsin mi?", p.name);
    if (n) msg += "\n\n" + tf("DİKKAT: Bu kişiye ait {} kayıt ve belgeleri de kalıcı olarak silinecek!", n);
    if (await Dlg.confirm(msg, t("Kişiyi sil"), { danger: true, yes: t("Sil") })) {
      Store.deletePerson(pid);
      if (this.sel === pid) { this.sel = this.isWide() ? "ALL" : null; this.view = "list"; this.applyView(); }
      this.refresh();
      Sheets.refreshAll();
      return true;
    }
    return false;
  },
  addTx(direction) {
    Forms.tx({ direction, pid: this.view === "person" || this.isWide() ? this.pid() : null });
  },
  addReminder() {
    if (!Store.persons().length) { Dlg.alert(t("Önce bir kişi ekleyin."), t("Kişi yok")); return; }
    Forms.reminder({ pid: this.pid() });
  },
};

function openChannel(p, ch) {
  if (!p) return;
  const { url, err } = channelUrl(p, ch);
  if (err) { Dlg.alert(err, t(CH_NAMES[ch])); return; }
  try { openUrl(url); } catch (e) { Dlg.alert(t("Bu bağlantıyı açacak program bulunamadı.") + "\n" + url, t(CH_NAMES[ch])); }
}

document.addEventListener("DOMContentLoaded", () => App.init());
