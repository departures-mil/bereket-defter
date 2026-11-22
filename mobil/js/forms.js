/* Formlar ve pencereler: kişi, Kişi Defteri, kayıt, belge, geçmiş, hatırlatıcılar, döküm, eşitleme, menü, yedek. */
'use strict';

function field(label, input, hint) {
  return h("label", { class: "field" }, h("span", { class: "flabel" }, label), input, hint ? h("small", { class: "fhint muted" }, hint) : null);
}
function inp(attrs) { return h("input", Object.assign({ class: "inp", type: "text" }, attrs)); }
function txt(attrs) { return h("textarea", Object.assign({ class: "inp", rows: 3 }, attrs)); }
/** düğmeli seçim: opts [{v, label, cls}] */
function seg(opts, value, onchange, cls) {
  let cur = value;
  const btns = opts.map(o => h("button", { type: "button", class: "seg-b " + (o.cls || ""), "data-v": o.v, "aria-pressed": String(o.v === value),
    onclick: () => { set(o.v); if (onchange) onchange(o.v); } }, o.label));
  const el = h("div", { class: "seg " + (cls || ""), role: "group" }, btns);
  function set(v) { cur = v; btns.forEach(b => b.setAttribute("aria-pressed", String(b.dataset.v === String(v)))); }
  return { el, get: () => cur, set };
}
const NEW_PERSON = "__yeni__";
/** withNew: listenin sonuna "+ Yeni kişi ekle" seçeneği konur (değeri NEW_PERSON) */
function personSelect(pid, withNew) {
  const s = h("select", { class: "inp", "aria-label": t("Kişi") }, Store.persons().map(p => h("option", { value: p.id }, p.name)),
    withNew ? h("option", { value: NEW_PERSON }, t("➕ Yeni kişi ekle")) : null);
  if (pid && Store.person(pid)) s.value = pid;
  else if (withNew && !Store.persons().length) s.value = NEW_PERSON;
  return s;
}
function curSeg(value, onchange) {
  return seg(CURRENCIES.map(c => ({ v: c, label: t(CURRENCY_NAMES[c]) })), value, onchange, "cur3");
}
function btn(label, cls, fn, attrs) { return h("button", Object.assign({ type: "button", class: "btn " + (cls || ""), onclick: fn }, attrs || {}), label); }

const PERSON_EXTRA = [["phone2", "2. Telefon", ""], ["wa_phone", "WhatsApp no", "Boşsa Telefon kullanılır"],
  ["tg_user", "Telegram kullanıcı adı / no", "@kullanici veya +90…"], ["sg_phone", "Signal no", "Boşsa Telefon kullanılır"],
  ["email", "E-posta", ""], ["address", "Adres", ""]];
const BOOK_COLS = [["name", "Ad Soyad"], ["phone", "Telefon"], ["phone2", "2. Telefon"], ["wa_phone", "WhatsApp no"],
  ["tg_user", "Telegram kullanıcı adı / no"], ["sg_phone", "Signal no"], ["email", "E-posta"], ["address", "Adres"], ["note", "Not"]];
const PHONE_KEYS = new Set(["phone", "phone2", "wa_phone", "sg_phone"]);

function chToggle(ch, on, onchange) {
  const b = h("button", { type: "button", class: "chtoggle", "aria-pressed": String(!!on), "data-ch": ch,
    onclick: () => { on = !on; paint(); onchange(on); } });
  function paint() {
    clear(b).append(channelIcon(ch, on, 30), h("span", null, chLabel(ch)));
    b.setAttribute("aria-pressed", String(!!on));
  }
  paint();
  return b;
}

const Forms = {
  /* ================================================================ kişi */
  person(row) {
    const val = k => (row ? row[k] || "" : "");
    const name = inp({ value: val("name"), autocomplete: "off" });
    const phone = inp({ type: "tel", value: val("phone"), placeholder: "+90 5xx xxx xx xx", dir: "ltr" });
    const extra = {};
    const extraFields = PERSON_EXTRA.map(([k, label, ph]) => {
      extra[k] = inp({ type: k === "email" ? "email" : PHONE_KEYS.has(k) ? "tel" : "text", value: val(k), placeholder: ph ? t(ph) : null,
        dir: k === "address" ? null : "ltr" });
      return field(t(label), extra[k]);
    });
    const ch = {};
    const toggles = h("div", { class: "chgrid" }, CHANNELS.map(c => { ch[c] = !!(row && row["ch_" + c]); return chToggle(c, ch[c], v => { ch[c] = v; }); }));
    const note = txt({ value: val("note") });
    let entry;
    const save = async () => {
      if (!name.value.trim()) { await Dlg.alert(t("Ad Soyad boş olamaz."), t("Eksik")); name.focus(); return; }
      const fields = { name: name.value, phone: phone.value, note: note.value };
      for (const k in extra) fields[k] = extra[k].value;
      for (const c of CHANNELS) fields["ch_" + c] = ch[c];
      if (row) Store.updateContact(row.id, fields);
      else {
        const id = Store.addPerson(fields);
        App.search = ""; if (App.searchEl) App.searchEl.value = "";
        Sheets.close(entry);
        if (!Sheets.stack.length) App.select(id); else App.refresh();
        Sheets.refreshAll();
        toast(t("Kaydedildi"));
        return;
      }
      Sheets.close(entry);
      App.refresh();
      Sheets.refreshAll();
      toast(t("Kaydedildi"));
    };
    entry = Sheets.open({ title: row ? t("Kişi Düzenle") : t("Yeni Kişi"), cls: "form",
      body: h("div", { class: "form-grid" }, field(t("Ad Soyad *"), name), field(t("Telefon"), phone), extraFields,
        h("div", { class: "field" }, h("span", { class: "flabel" }, t("Ulaşma yolları")), toggles), field(t("Not"), note)),
      footer: [btn(t("Vazgeç"), "light", () => Sheets.close(entry)), btn(t("Kaydet"), "primary", save)] });
    if (!row) setTimeout(() => name.focus(), 60);
  },

  /* ================================================================ Kişi Defteri */
  book() {
    let q = "";
    const open = new Set();
    const listEl = h("div", { class: "book-list" });
    const search = h("input", { type: "search", class: "inp", placeholder: t("🔍 Kişi ara…"), "aria-label": t("Kişi ara"),
      oninput: e => { q = e.target.value; render(); } });
    const card = p => {
      const isOpen = open.has(p.id);
      const toggles = h("div", { class: "book-ch" }, CHANNELS.map(c => h("button", { type: "button", class: "chbtn" + (p["ch_" + c] ? " on" : ""),
        title: t(CH_NAMES[c]) + " — " + (p["ch_" + c] ? t("açık") : t("kapalı")) + " (" + t("tıklayınca değişir") + ")",
        "aria-label": t(CH_NAMES[c]) + " — " + (p["ch_" + c] ? t("açık") : t("kapalı")), "aria-pressed": String(!!p["ch_" + c]),
        onclick: () => { Store.setChannel(p.id, c, !p["ch_" + c]); replace(p.id); App.refresh(); } }, channelIcon(c, !!p["ch_" + c], 32))));
      const head = h("div", { class: "book-head" },
        h("button", { type: "button", class: "book-name", "aria-expanded": String(isOpen), onclick: () => { isOpen ? open.delete(p.id) : open.add(p.id); replace(p.id); } },
          h("span", { class: "bn" }, p.name), h("span", { class: "chev" }, isOpen ? "▲" : "▼")), toggles);
      const el = h("div", { class: "book-card" + (isOpen ? " open" : ""), "data-id": p.id }, head);
      if (!isOpen) {
        const sum = BOOK_COLS.slice(1).map(([k, label]) => p[k] ? h("div", { class: "bk-line" }, h("span", { class: "muted" }, t(label) + ": "),
          PHONE_KEYS.has(k) ? ltr(p[k]) : p[k]) : null).filter(Boolean);
        el.append(h("div", { class: "book-sum", onclick: () => { open.add(p.id); replace(p.id); } },
          sum.length ? sum : h("span", { class: "muted" }, t("Bilgi yok — düzenlemek için dokunun"))));
      } else {
        const edits = BOOK_COLS.map(([k, label]) => {
          const e = k === "note" || k === "address" ? txt({ value: p[k] || "", rows: 2 })
            : inp({ type: PHONE_KEYS.has(k) ? "tel" : k === "email" ? "email" : "text", value: p[k] || "", dir: PHONE_KEYS.has(k) || k === "tg_user" || k === "email" ? "ltr" : null });
          e.addEventListener("change", async () => {
            const cur = Store.person(p.id);
            if (!cur) return;
            if (k === "name" && !e.value.trim()) { await Dlg.alert(t("Ad Soyad boş olamaz."), t("Eksik")); e.value = cur.name; return; }
            Store.updateContact(p.id, { [k]: e.value });
            e.classList.add("saved");
            setTimeout(() => e.classList.remove("saved"), 900);
            App.refresh();
            if (k === "name") { const bn = el.querySelector(".bn"); if (bn) bn.textContent = e.value.trim(); }
          });
          return field(t(label), e);
        });
        el.append(h("div", { class: "book-edit form-grid" }, edits,
          h("div", { class: "row-btns" }, btn(t("Sil"), "danger", async () => { if (await App.deletePerson(p.id)) render(); }),
            btn(t("Kapat"), "light", () => { open.delete(p.id); replace(p.id); }))));
      }
      return el;
    };
    const replace = id => {
      const old = listEl.querySelector(`.book-card[data-id="${id}"]`);
      const p = Store.person(id);
      if (old && p) old.replaceWith(card(p)); else render();
    };
    const render = () => {
      clear(listEl);
      const rows = Store.persons(q);
      for (const p of rows) listEl.append(card(p));
      if (!rows.length) listEl.append(h("div", { class: "empty" }, q ? t("Kişi bulunamadı.") : t("Henüz kişi yok. “+ Kişi Ekle” ile başlayın.")));
    };
    render();
    const entry = Sheets.open({ title: t("Kişi Defteri"), cls: "form book",
      body: h("div", null, h("div", { class: "book-top" }, search),
        h("p", { class: "muted tip" }, t("Simgelere dokunarak açıp kapatabilirsiniz. Diğer bilgileri düzenlemek için kişiye dokunun; değişiklikler hemen kaydedilir.")),
        listEl),
      footer: [btn(t("+ Yeni Kişi"), "primary", () => Forms.person(null)), btn(t("Kapat"), "light", () => Sheets.close(entry))],
      refresh: () => { if (!listEl.contains(document.activeElement)) render(); },
      onClose: () => App.refresh() });
  },

  /* ================================================================ kayıt (işlem) */
  tx({ tx, direction, pid }) {
    const person = personSelect(tx ? tx.person : pid, !tx);
    // yeni kişi: yalnızca ad sorulur; kayıt bitince kişi defterine geçilir
    const newName = inp({ autocomplete: "off", enterkeyhint: "next", placeholder: t("Ad Soyad"), "aria-label": t("Yeni kişinin adı") });
    const newField = field(t("Yeni kişinin adı *"), newName);
    const isNew = () => person.value === NEW_PERSON;
    const syncNew = () => { newField.hidden = !isNew(); };
    person.addEventListener("change", () => { syncNew(); if (isNew()) newName.focus(); });
    syncNew();
    const when = h("input", { class: "inp", type: "datetime-local", step: 60, dir: "ltr", value: toInputDT(tx ? tx.ts : nowStr()), "aria-label": t("Tarih / Saat") });
    const dir = seg([{ v: "VERDIM", label: t("Verdim (Çıktı)"), cls: "s-ver" }, { v: "ALDIM", label: t("Aldım (Girdi)"), cls: "s-al" }],
      tx ? tx.direction : direction || "VERDIM", () => hint(), "dir2");
    const cur = curSeg(tx ? tx.currency : "USD", () => hint());
    const amount = inp({ inputmode: "decimal", class: "inp amount", dir: "ltr", value: tx ? amountInput(tx.amount) : "", placeholder: LANG === "tr" ? "0,00" : "0.00",
      autocomplete: "off", enterkeyhint: "done", "aria-label": t("Tutar") });
    const desc = txt({ value: tx ? tx.description || "" : "", rows: 2 });
    const hintEl = h("div", { class: "hint-gold" }, t("💵 Nakit dolar aldıysanız banknotların fotoğrafını eklemeyi unutmayın (sahte çıkma ihtimaline karşı)."));
    const hint = () => { hintEl.hidden = !(dir.get() === "ALDIM" && cur.get() === "USD"); };
    hint();
    // belgeler
    const items = tx ? Store.docsOf(tx.id).map(d => Object.assign({}, d)) : [];
    const removed = [];
    const grid = h("div", { class: "dgrid" });
    const renderDocs = () => {
      clear(grid);
      for (const d of items) grid.append(docTile(d, { onRemove: x => { items.splice(items.indexOf(x), 1); if (x.id && !x.blob) removed.push(x.id); renderDocs(); } }));
      if (!items.length) grid.append(h("div", { class: "doc-none" }, "⚠ " + t("Bu kaydın dekontu / belgesi yok")));
    };
    const addFiles = files => {
      for (const f of files) items.push({ name: f.name || ("foto_" + stamp() + extOf("", f.type)), ext: extOf(f.name, f.type), mime: f.type || "", size: f.size, blob: f });
      renderDocs();
    };
    const fileIn = h("input", { type: "file", multiple: true, hidden: true, onchange: e => { addFiles([...e.target.files]); e.target.value = ""; } });
    const camIn = h("input", { type: "file", accept: "image/*", capture: "environment", hidden: true, onchange: e => { addFiles([...e.target.files]); e.target.value = ""; } });
    renderDocs();
    let entry;
    const save = async () => {
      let pidv = person.value;
      const creating = isNew();
      if (creating) {
        if (!newName.value.trim()) { await Dlg.alert(t("Ad Soyad boş olamaz."), t("Eksik")); newName.focus(); return; }
      } else if (!pidv || !Store.person(pidv)) { await Dlg.alert(t("Önce bir kişi ekleyin."), t("Eksik")); return; }
      let amt = parseAmount(amount.value);
      if (!(amt > 0)) { await Dlg.alert(t("Tutar sıfırdan büyük olmalı."), t("Eksik")); amount.focus(); return; }
      amt = Math.round(amt * 100) / 100;
      if (!items.length && !(await Dlg.confirm(t("Bu kayda dekont / belge eklenmedi. Belgesiz kaydedilsin mi?\n\n(Hayır derseniz belge ekleyebilirsiniz.)"), t("Belge yok")))) return;
      if (creating) {
        // aynı adda kişi varsa yenisi açılmaz, o kişiye yazılır
        const nm = newName.value.trim(), key = lower(nm);
        const same = Store.persons().find(p => lower(p.name).trim() === key);
        pidv = same ? same.id : Store.addPerson({ name: nm });
      }
      const ts = fromInputDT(when.value) || nowStr().slice(0, 16);
      const v = { person: pidv, ts, direction: dir.get(), currency: cur.get(), amount: amt, description: desc.value };
      const newOnes = items.filter(d => d.blob);
      let id;
      if (tx) {
        id = tx.id;
        const same = tx.person === v.person && ts16(tx.ts) === ts16(v.ts) && tx.direction === v.direction && tx.currency === v.currency &&
          Math.abs(tx.amount - v.amount) < 0.001 && (tx.description || "") === v.description.trim();
        if (!same || newOnes.length || removed.length) Store.updateTx(id, same ? Object.assign({}, v, { ts: tx.ts }) : v);
      } else id = Store.addTx(v);
      for (const did of removed) Store.deleteDoc(did);
      for (const d of newOnes) {
        try { await Store.addDoc(id, d.blob); } catch (e) { await Dlg.alert(tf("{} kopyalanamadı: {}", d.name, e && e.message || e), t("Belge")); }
      }
      Store.changed();
      Sheets.close(entry);
      if (creating) {
        App.search = ""; if (App.searchEl) App.searchEl.value = "";
        Sheets.closeAll();
        App.select(pidv);
        App.refresh();
      } else App.refresh();
      Sheets.refreshAll();
      toast(t("Kaydedildi"));
    };
    entry = Sheets.open({ title: tx ? t("Kaydı Düzenle") : t("Yeni Kayıt"), cls: "form",
      body: h("div", { class: "form-grid" },
        field(t("Kişi"), person), newField, field(t("Tarih / Saat"), when),
        h("div", { class: "field" }, h("span", { class: "flabel" }, t("İşlem")), dir.el),
        h("div", { class: "field" }, h("span", { class: "flabel" }, t("Para birimi")), cur.el),
        field(t("Tutar"), amount), field(t("Açıklama"), desc), hintEl,
        h("div", { class: "field docs-field" }, h("span", { class: "flabel" }, t("Dekont / Belgeler")),
          h("small", { class: "muted" }, t("PDF, resim veya her türlü dosya. Açmak için dokunun.")), grid,
          h("div", { class: "row-btns" }, btn(t("📎 Dekont / belge ekle"), "light2", () => fileIn.click()), btn(t("📷 Fotoğraf çek"), "light2", () => camIn.click())),
          fileIn, camIn)),
      footer: [btn(t("Vazgeç"), "light", () => Sheets.close(entry)), btn(t("Kaydet"), dir.get() === "VERDIM" ? "danger" : "primary", save, { "data-save": "1" })],
      onClose: () => { for (const d of items) if (d._url) URL.revokeObjectURL(d._url); } });
    // kaydet düğmesinin rengi işlem türünü izler
    dir.el.addEventListener("click", () => { const s = entry.sheet.querySelector("[data-save]"); if (s) s.className = "btn " + (dir.get() === "VERDIM" ? "danger" : "primary"); });
    if (!tx) setTimeout(() => (isNew() ? newName : amount).focus(), 80);
  },

  txDetail(id) {
    const r = Store.tx(id);
    if (!r) return;
    let entry;
    const body = h("div");
    const render = () => {
      const x = Store.tx(id);
      if (!x) { Sheets.close(entry); return; }
      const ver = x.direction === "VERDIM";
      const docs = Store.docsOf(id);
      const kv = (k, v) => h("div", { class: "kv" }, h("span", { class: "k muted" }, k), h("span", { class: "v" }, v));
      clear(body).append(
        h("div", { class: "det-amt " + (ver ? "ver" : "al") }, h("div", { class: "det-dir" }, ver ? t("Verdim (Çıktı)") : t("Aldım (Girdi)")), ltr(money(x.amount, x.currency))),
        h("div", { class: "kvs" },
          kv(t("Kişi"), Store.personName(x.person)), kv(t("Tarih / Saat"), ltr(tsDisplay(x.ts))), kv(t("Para birimi"), t(CURRENCY_NAMES[x.currency])),
          kv(t("Açıklama"), x.description || "—"),
          x.updated_at ? kv("✎", [t("Değiştirildi") + ": ", ltr(tsDisplay(x.updated_at))]) : null),
        h("h4", { class: "sec" }, t("📎 Belgeler") + (docs.length ? ` (${docs.length})` : "")),
        docs.length ? h("div", { class: "dgrid" }, docs.map(d => docTile(d))) :
          h("div", { class: "doc-none" }, "⚠ " + t("Bu kayıtta dekont / belge yok. Şimdi eklemek ister misiniz?"),
            h("div", null, btn(t("📎 Dekont / belge ekle"), "light2", () => { Sheets.close(entry); Forms.tx({ tx: Store.tx(id) }); }))));
    };
    render();
    entry = Sheets.open({ title: tsDisplay(r.ts), cls: "form", body,
      footer: [btn(t("Düzenle"), "primary", () => { Sheets.close(entry); Forms.tx({ tx: Store.tx(id) }); }),
        btn(t("Değişiklik Geçmişi"), "light", () => Forms.history(id)),
        btn(t("Sil"), "danger", async () => {
          const x = Store.tx(id);
          if (x && await Dlg.confirm(tf("{} tarihli {} kaydı ve belgeleri silinsin mi?", tsDisplay(x.ts), money(x.amount, x.currency)), t("Kaydı sil"), { danger: true, yes: t("Sil") })) {
            Store.deleteTx(id); Sheets.close(entry); App.refresh(); Sheets.refreshAll(); toast(t("Silindi"));
          }
        })],
      refresh: render });
  },

  history(id) {
    const hist = Store.history(id);
    if (!hist.length) { Dlg.alert(t("Bu kayıt hiç değiştirilmemiş."), t("Geçmiş")); return; }
    const items = hist.map(x => {
      let o = {};
      try { o = JSON.parse(x.old || "{}"); } catch (e) { o = {}; }
      const ver = o.direction === "VERDIM";
      return h("div", { class: "hist" },
        h("div", { class: "hist-at" }, x.action === "SILINDI" ? "🗑 " + t("Silindi") : "✎ " + t("Değiştirildi"), " — ", ltr(tsDisplay(x.at))),
        h("div", null, h("span", { class: "muted" }, t("önceki hali") + ": "), ltr(tsDisplay(o.ts || "")), ", ",
          h("b", { class: ver ? "neg" : "pos" }, ver ? t("Verdim") : t("Aldım")), " ", ltr(money(o.amount || 0, o.currency || "USD")),
          o.person_name ? " — " + o.person_name : "", o.description ? h("div", { class: "muted" }, o.description) : null));
    });
    const entry = Sheets.open({ title: t("Değişiklik Geçmişi"), cls: "form", body: h("div", { class: "hist-list" }, items),
      footer: [btn(t("Kapat"), "light", () => Sheets.close(entry))] });
  },

  /* ================================================================ hatırlatıcılar */
  reminder({ rem, pid }) {
    if (!Store.persons().length) { Dlg.alert(t("Önce bir kişi ekleyin."), t("Kişi yok")); return; }
    const person = personSelect(rem ? rem.person : pid);
    const kind = seg([{ v: "TAHSIL", label: t(KIND_TEXT.TAHSIL), cls: "s-al" }, { v: "ODEME", label: t(KIND_TEXT.ODEME), cls: "s-ver" }],
      rem ? rem.kind : "TAHSIL", null, "dir2");
    const cur = curSeg(rem ? rem.currency : "USD");
    const amount = inp({ inputmode: "decimal", class: "inp amount", dir: "ltr", value: rem && rem.amount ? amountInput(rem.amount) : "",
      placeholder: t("(tutar belirtilmedi)"), autocomplete: "off", "aria-label": t("Tutar") });
    let dueDefault;
    if (rem) dueDefault = toInputDT(rem.due);
    else { const d = new Date(Date.now() + 86400000); dueDefault = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T10:00`; }
    const due = h("input", { class: "inp", type: "datetime-local", step: 60, dir: "ltr", value: dueDefault, "aria-label": t("Hatırlatma zamanı") });
    const addDays = n => { const d = parseTs(fromInputDT(due.value) || nowStr()); d.setDate(d.getDate() + n); due.value = toInputDT(dateToStr(d)); };
    const note = txt({ value: rem ? rem.note || "" : "", rows: 2 });
    const fill = () => {
      const b = Store.balances(person.value)[cur.get()][2];
      if (b > 0) kind.set("TAHSIL"); else if (b < 0) kind.set("ODEME");
      amount.value = amountInput(Math.abs(b));
    };
    let entry;
    const save = async () => {
      if (!person.value) { await Dlg.alert(t("Önce bir kişi ekleyin."), t("Eksik")); return; }
      let amt = parseAmount(amount.value);
      if (isNaN(amt) || amt < 0) { await Dlg.alert(t("Tutar geçersiz."), t("Eksik")); return; }
      amt = Math.round(amt * 100) / 100;
      const v = { person: person.value, kind: kind.get(), currency: cur.get(), amount: amt, due: fromInputDT(due.value) || nowStr().slice(0, 16), note: note.value };
      if (rem) {
        if (ts16(rem.due) !== ts16(v.due)) { v.done = false; Rem.notified.delete(rem.id); }
        Store.updateReminder(rem.id, v);
      } else Store.addReminder(v);
      Sheets.close(entry);
      Rem.check(false);
      App.refresh();
      Sheets.refreshAll();
      toast(t("Kaydedildi"));
    };
    entry = Sheets.open({ title: rem ? t("Hatırlatıcıyı Düzenle") : t("Yeni Hatırlatıcı"), cls: "form",
      body: h("div", { class: "form-grid" }, field(t("Kişi"), person),
        h("div", { class: "field" }, h("span", { class: "flabel" }, t("Tür")), kind.el),
        h("div", { class: "field" }, h("span", { class: "flabel" }, t("Para birimi")), cur.el),
        h("div", { class: "field" }, h("span", { class: "flabel" }, t("Tutar")), h("div", { class: "inline" }, amount, btn(t("Bakiyeyi kullan"), "light2", fill))),
        h("div", { class: "field" }, h("span", { class: "flabel" }, t("Hatırlatma zamanı")), due,
          h("div", { class: "row-btns" }, btn(t("+1 gün"), "light2 small", () => addDays(1)), btn(t("+1 hafta"), "light2 small", () => addDays(7)),
            btn(t("+1 ay"), "light2 small", () => addDays(30)))),
        field(t("Not"), note)),
      footer: [btn(t("Vazgeç"), "light", () => Sheets.close(entry)), btn(t("Kaydet"), "primary", save)] });
  },

  reminders({ dueOnly, pid }) {
    let mode = dueOnly ? "due" : "pending";
    const head = h("div", { class: "rem-head" });
    const list = h("div", { class: "rem-list" });
    const filter = seg([{ v: "due", label: t("Vakti gelenler") }, { v: "pending", label: t("Bekleyenler") }, { v: "all", label: t("Tümü") }],
      mode, v => { mode = v; render(); }, "seg3");
    const render = () => {
      const rows = Store.reminders({ pid, pendingOnly: mode !== "all", until: mode === "due" ? today2359() : null });
      head.textContent = (pid ? Store.personName(pid) + " — " : "") +
        (mode === "due" ? tf("Bugün ve geçmişte vakti gelen {} hatırlatıcı", rows.length) : tf("{} hatırlatıcı", rows.length));
      clear(list);
      for (const r of rows) {
        const [, label, color] = reminderState(r);
        list.append(h("div", { class: "rem-card" + (r.done ? " done" : "") },
          h("div", { class: "rem-top" }, h("b", { style: `color:${color}` }, label), ltr(tsDisplay(r.due), "rem-due")),
          h("div", { class: "rem-who" }, h("b", null, Store.personName(r.person)), " — ",
            h("span", { class: r.kind === "TAHSIL" ? "pos" : "neg" }, t(KIND_TEXT[r.kind])), " ", ltr(reminderAmt(r), "rem-amt")),
          r.note ? h("div", { class: "muted rem-note" }, r.note) : null,
          h("div", { class: "row-btns rem-acts" },
            btn(r.done ? t("Geri al") : t("✓ Tamamlandı"), "gold small", () => { Store.setReminderDone(r.id, !r.done); if (!r.done) Rem.cancel(r.id); after(); }),
            btn(t("Ertele (+1 gün)"), "light2 small", () => {
              const base = new Date(Math.max(parseTs(r.due).getTime(), Date.now()));
              base.setDate(base.getDate() + 1);
              Store.updateReminder(r.id, { due: dateToStr(base).slice(0, 16), done: false });
              Rem.notified.delete(r.id);
              after();
            }),
            btn(t("Düzenle"), "light2 small", () => Forms.reminder({ rem: Store.reminder(r.id) })),
            btn(t("Sil"), "danger small", async () => {
              if (await Dlg.confirm(t("Hatırlatıcı silinsin mi?"), t("Sil"), { danger: true, yes: t("Sil") })) { Store.deleteReminder(r.id); Rem.cancel(r.id); after(); }
            }))));
      }
      if (!rows.length) list.append(h("div", { class: "empty" }, t("Hatırlatıcı yok.")));
    };
    const after = () => { Rem.check(false); render(); App.refresh(); };
    render();
    const entry = Sheets.open({ title: t("🔔 Hatırlatıcılar"), cls: "form",
      body: h("div", null, head, filter.el, list),
      footer: [btn(t("+ Yeni Hatırlatıcı"), "primary", () => {
        if (!Store.persons().length) { Dlg.alert(t("Önce bir kişi ekleyin."), t("Kişi yok")); return; }
        Forms.reminder({ pid: pid || App.pid() });
      }), btn(t("Kapat"), "light", () => Sheets.close(entry))],
      refresh: render, onClose: () => App.refresh() });
  },

  /* ================================================================ döküm */
  statement(pid) {
    Statement.injectCss();
    const all = Store.transactions({ pid });
    const first = all.length ? all[0].ts.slice(0, 10) : nowStr().slice(0, 10);
    const today = nowStr().slice(0, 10);
    const d1 = h("input", { class: "inp", type: "datetime-local", step: 60, dir: "ltr", value: first + "T00:00", "aria-label": t("Başlangıç"), onchange: () => render() });
    const d2 = h("input", { class: "inp", type: "datetime-local", step: 60, dir: "ltr", value: today + "T23:59", "aria-label": t("Bitiş"), onchange: () => render() });
    const group = seg([{ v: "day", label: t("Günlük gruplama") }, { v: "hour", label: t("Saatlik gruplama") }], "day", () => render(), "seg2");
    const cur = h("select", { class: "inp", "aria-label": t("Para birimi"), onchange: () => render() }, h("option", { value: "" }, t("Tüm para birimleri")),
      CURRENCIES.map(c => h("option", { value: c }, t(CURRENCY_NAMES[c]))));
    const ymd = d => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
    const quick = i => {
      const n = new Date();
      let s;
      if (i === 1) s = new Date(n);
      else if (i === 2) { s = new Date(n); s.setDate(s.getDate() - 6); }
      else if (i === 3) s = new Date(n.getFullYear(), n.getMonth(), 1);
      else { s = new Date(n); s.setFullYear(s.getFullYear() - 50); }
      d1.value = ymd(s) + "T00:00";
      d2.value = ymd(n) + "T23:59";
      render();
    };
    const view = h("div", { class: "st", dir: isRtl() ? "rtl" : "ltr" });
    let last = null;
    const render = () => {
      last = Statement.build({ pid, start: fromInputDT(d1.value).slice(0, 16) || "1970-01-01 00:00", end: fromInputDT(d2.value).slice(0, 16) || "2999-12-31 23:59",
        cur: cur.value, hourly: group.get() === "hour" });
      view.innerHTML = last.body;
      requestAnimationFrame(() => view.classList.toggle("narrow", view.clientWidth < 720));
    };
    const controls = h("div", { class: "st-ctl" },
      h("div", { class: "two" }, field(t("Başlangıç"), d1), field(t("Bitiş"), d2)),
      h("div", { class: "row-btns quick" }, btn(t("Bugün"), "light2 small", () => quick(1)), btn(t("Son 7 gün"), "light2 small", () => quick(2)),
        btn(t("Bu ay"), "light2 small", () => quick(3)), btn(t("Tümü"), "light2 small", () => quick(4))),
      group.el, cur);
    const entry = Sheets.open({ title: t("Hesap Dökümü"), cls: "form wide-sheet", body: h("div", null, controls, h("div", { class: "st-wrap" }, view)),
      footer: [btn(t("PDF / Yazdır"), "gold", () => { render(); Statement.print(last.full, last.fileBase); }),
        btn(t("Paylaş"), "primary", () => { render(); shareBlob(textToBlob(last.full, "text/html"), "text/html", last.fileBase + ".html"); }),
        btn(t("Kapat"), "light", () => Sheets.close(entry))],
      refresh: render });
    render();
    window.addEventListener("resize", render, { passive: true });
    entry.onClose = () => window.removeEventListener("resize", render);
  },

  /* ================================================================ güncelleme */
  update(opt) {
    opt = opt || {};
    const msg = h("div", { class: "upd-msg", role: "status" });
    const notes = h("div", { class: "upd-notes muted" });
    // indirme: çubuk + her bilgi ayrı parça (parça ortadan bölünmez, sığmazsa bütün olarak alt satıra geçer)
    const bar = h("i");
    const stats = h("div", { class: "upd-stats" });
    const progBox = h("div", { class: "upd-prog", hidden: true }, h("div", { class: "upd-bar" }, bar), stats);
    const stat = (label, val) => h("span", { class: "upd-stat" }, label ? h("b", null, label + " ") : null, ltr(val));
    const goBtn = btn(t("⬆ Güncelle"), "primary", () => Upd.install());
    const checkBtn = btn(t("Tekrar denetle"), "light", () => Upd.check());
    const paint = () => {
      const st = Upd.state, info = Upd.info || {};
      goBtn.hidden = !(st === "available" || (st === "apk" && Upd.err === "IZIN") || (st === "error" && info.surum && versionNewer(info.surum, APP_VERSION)));
      checkBtn.disabled = ["checking", "downloading", "installed"].includes(st);
      notes.textContent = info.surum && versionNewer(info.surum, APP_VERSION) ? String(info.notlar || "") : "";
      let text = "";
      if (st === "checking") text = t("Yeni sürüm denetleniyor…");
      else if (st === "none") text = t("Uygulama güncel. Yeni sürüm yok.");
      else if (st === "available") text = tf("Yeni sürüm hazır: {}", "v" + info.surum);
      else if (st === "downloading") {
        const p = Upd.progInfo();
        text = p ? tf("Güncelleme indiriliyor… %{}", p.pct) : t("Güncelleme indiriliyor…");
        bar.style.width = (p ? p.pct : 0) + "%";
        clear(stats);
        if (p) {
          stats.append(stat("", p.size), stat(t("Kalan:"), p.left));
          if (p.speed) stats.append(stat(t("Hız:"), p.speed));
          if (p.eta) stats.append(stat(t("Kalan süre:"), p.eta));
        }
      }
      else if (st === "installed") text = t("Güncelleme kuruldu. Uygulama yeniden açılıyor…");
      else if (st === "apk") text = Upd.err === "IZIN"
        ? t("Android, bu uygulamanın güncelleme kurmasına izin istiyor: açılan ekranda 'Bu kaynaktan izin ver'i açın, geri dönüp tekrar ⬆ Güncelle'ye dokunun.")
        : t("Android kurulum ekranı açıldı: 'Güncelle'ye dokunun. Kayıtlarınız silinmez.");
      else if (st === "error") text = Upd.errText();
      msg.textContent = text;
      msg.dataset.kind = st;
      progBox.hidden = st !== "downloading";
    };
    const entry = Sheets.open({ title: t("⬆ Güncelleme"), cls: "dialog",
      body: h("div", { class: "about" },
        h("div", null, tf("Kullandığınız sürüm: {}", "v" + APP_VERSION)), msg, progBox, notes,
        h("p", { class: "muted" }, t("Güncelleme sadece uygulamayı yeniler; kayıtlarınız, kişileriniz ve belgeleriniz olduğu gibi kalır."))),
      footer: [checkBtn, btn(t("⚙ Ayarlar"), "light", () => Forms.settings()), btn(t("Kapat"), "light", () => Sheets.close(entry)), goBtn] });
    entry.isUpdate = true;
    Upd.popupWanted = false;
    Upd.listeners.push(paint);
    entry.onClose = () => { const i = Upd.listeners.indexOf(paint); if (i >= 0) Upd.listeners.splice(i, 1); };
    if (opt.autoInstall && Upd.state === "available") Upd.install();
    else if (["idle", "none", "error"].includes(Upd.state)) Upd.check();
    paint();
  },

  /* ================================================================ ayarlar */
  settings() {
    const c = Upd.cfg();
    const i = h("input", { type: "checkbox", checked: !!c.notify });
    let entry;
    const save = () => { Upd.setCfg({ notify: i.checked }); Sheets.close(entry); toast(t("Kaydedildi")); };
    entry = Sheets.open({ title: t("⚙ Ayarlar"), cls: "dialog",
      body: h("div", { class: "settings" },
        h("h3", null, t("⬆ Güncelleme denetimi")),
        h("p", null, t("Uygulama her açıldığında yeni sürüm denetlenir.")),
        h("label", { class: "chk set-chk" }, i, h("span", null, t("Yeni sürüm bulununca bildirim göster"))),
        Forms.contactBox()),
      footer: [btn(t("Vazgeç"), "light", () => Sheets.close(entry)), btn(t("Kaydet"), "primary", save)] });
  },

  /* admin ile iletişim: mesaj FormSubmit üzerinden yöneticinin e-postasına gider; adres programda görünmez */
  contactBox() {
    const name = inp({ maxlength: 80, dir: "auto", placeholder: t("Adınız (isteğe bağlı)") });
    const mail = inp({ type: "email", maxlength: 120, dir: "ltr", placeholder: t("E-posta (yanıt için, isteğe bağlı)") });
    const msg = h("textarea", { class: "inp", maxlength: 5000, dir: "auto", rows: 5, placeholder: t("Mesajınız"), style: "width:100%;box-sizing:border-box" });
    let busy = false;
    const send = btn(t("✉ Gönder"), "primary", async () => {
      if (busy) return;
      const m = msg.value.trim(), e = mail.value.trim();
      if (!m) { toast(t("Lütfen mesajınızı yazın.")); return; }
      if (e && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e)) { toast(t("E-posta adresi geçerli değil.")); return; }
      const to = atob("bW9jLmxpYW1ub3RvcnBANDMyMWxkaW50bWxkYmE=").split("").reverse().join("");
      const body = { _subject: "Bereket Defter: yeni mesaj", _template: "table", _captcha: "false", Ad: name.value.trim() || "-", Mesaj: m, Surum: APP_VERSION, Cihaz: "Android", Dil: document.documentElement.lang || "" };
      if (e) { body.email = e; body._replyto = e; }
      busy = true; send.disabled = true;
      try {
        const r = await fetch("https://formsubmit.co/ajax/" + to, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(body) });
        const j = await r.json().catch(() => ({}));
        if ((r.ok && String(j.success) !== "false") || /activat/i.test(j.message || "")) { msg.value = ""; toast(t("Mesajınız yöneticiye iletildi. Teşekkürler!")); }
        else toast(t("Mesaj gönderilemedi. İnternet bağlantınızı kontrol edip tekrar deneyin."));
      } catch (x) { toast(t("Mesaj gönderilemedi. İnternet bağlantınızı kontrol edip tekrar deneyin.")); }
      busy = false; send.disabled = false;
    });
    return h("div", { class: "contact-box" },
      h("h3", null, t("✉ Admin ile iletişime geç")),
      h("p", null, t("Programı geliştirmemiz için öneri, istek ve hata bildirimlerinizi yazın; mesajınız doğrudan yöneticiye ulaşır.")),
      name, mail, msg, send);
  },

  /* ================================================================ eşitleme */
  sync() {
    const c = Sync.cfg();
    const apiKey = inp({ value: c.apiKey || "", dir: "ltr", autocomplete: "off", spellcheck: "false", placeholder: "AIza…" });
    const projectId = inp({ value: c.projectId || "", dir: "ltr", autocomplete: "off", spellcheck: "false", placeholder: "bereket-defter" });
    const emulator = inp({ value: c.emulator || "", dir: "ltr", autocomplete: "off", placeholder: "127.0.0.1" });
    const email = inp({ type: "email", value: c.email || "", dir: "ltr", autocomplete: "username" });
    const password = inp({ type: "password", dir: "ltr", autocomplete: "current-password" });
    const status = h("div", { class: "sync-status", role: "status" });
    const who = h("div", { class: "sync-who" });
    const adv = h("div", { class: "adv", hidden: !c.emulator }, field(t("Emülatör (yalnızca test)"), emulator, t("Boş bırakın. Yalnızca geliştirici testleri içindir.")));
    const advBtn = btn(t("Gelişmiş"), "linkish small", () => { adv.hidden = !adv.hidden; });
    let busy = false;
    const showStatus = (txt, kind) => { status.textContent = txt; status.dataset.kind = kind; };
    const paint = () => {
      const st = Sync.status();
      if (!busy) showStatus(st.text, st.kind);
      const cc = Sync.cfg();
      who.textContent = Sync.signedIn() ? tf("Giriş yapıldı: {}", cc.email || "") : t("Giriş yapılmamış.");
      outBtn.hidden = nowBtn.hidden = !Sync.signedIn();
    };
    const doSign = async create => {
      if (busy) return;
      busy = true;
      showStatus(t("Bağlanılıyor…"), "run");
      inBtn.disabled = upBtn.disabled = true;
      try {
        await Sync.signIn({ apiKey: apiKey.value, projectId: projectId.value, emulator: emulator.value, email: email.value }, password.value, create);
        password.value = "";
        busy = false;
        showStatus(t("Giriş yapıldı. Eşitleniyor…"), "run");
      } catch (e) {
        busy = false;
        showStatus(syncErrText(e), "err");
      } finally {
        inBtn.disabled = upBtn.disabled = false;
        paint2();
      }
    };
    const paint2 = () => { const cc = Sync.cfg(); who.textContent = Sync.signedIn() ? tf("Giriş yapıldı: {}", cc.email || "") : t("Giriş yapılmamış."); outBtn.hidden = nowBtn.hidden = !Sync.signedIn(); };
    const inBtn = btn(t("Giriş yap"), "primary", () => doSign(false));
    const upBtn = btn(t("Hesap oluştur"), "light2", () => doSign(true));
    const nowBtn = btn(t("Şimdi eşitle"), "gold", () => { Sync.run(); paint(); });
    const outBtn = btn(t("Çıkış yap"), "danger", async () => {
      if (await Dlg.confirm(t("Bu cihazda bulut oturumu kapatılsın mı? Veriler bu cihazda kalır."), t("Çıkış yap"))) { Sync.signOut(); paint(); }
    });
    const help = h("details", { class: "help" }, h("summary", null, t("Firebase nasıl hazırlanır? (bir kez)")),
      h("ol", null,
        h("li", null, t("console.firebase.google.com adresinde bir proje oluşturun; Project settings → General → Web app ekleyin ve “apiKey” ile “projectId” değerlerini buraya yazın.")),
        h("li", null, t("Authentication → Sign-in method → Email/Password: Enabled (Etkin) yapın.")),
        h("li", null, t("Firestore Database → Create database ile veritabanını oluşturun; Rules sekmesine aşağıdaki kuralları yapıştırıp Publish (Yayınla) deyin."))),
      h("pre", { class: "rules", dir: "ltr" }, "rules_version = '2';\nservice cloud.firestore {\n  match /databases/{database}/documents {\n    match /users/{uid}/{document=**} {\n      allow read, write: if request.auth != null && request.auth.uid == uid;\n    }\n    match /guncelleme/{document=**} {\n      allow read: if true;\n    }\n  }\n}"),
      h("p", { class: "muted" }, t("Telefonda ve bilgisayarda aynı e-posta ve şifreyle giriş yapın; kayıtlar, belgeler ve hatırlatıcılar iki tarafta da görünür.")));
    // 📶 Wi‑Fi ile internetsiz eşitleme (ikinci seçenek)
    const lc = Lan.cfg();
    const lanHost = inp({ value: lc.host || "", dir: "ltr", autocomplete: "off", spellcheck: "false", inputmode: "decimal", placeholder: "192.168.1.5" });
    const lanCode = inp({ value: lc.code || "", dir: "ltr", autocomplete: "off", inputmode: "numeric", maxlength: "6", placeholder: "123456" });
    const lanStatus = h("div", { class: "sync-status", role: "status" });
    const lanPaint = () => {
      const c2 = Lan.cfg();
      if (!Lan.supported()) { lanStatus.textContent = t("Wi‑Fi eşitleme için telefon uygulamasının yeni sürümü (1.8) gerekir: ⬆ Güncelleme'den kurun."); lanStatus.dataset.kind = "err"; return; }
      lanStatus.textContent = c2.last ? tf("Son Wi‑Fi eşitleme: {}", hhmm(new Date(c2.last)) + (c2.name ? " · " + c2.name : "")) : "";
      lanStatus.dataset.kind = "ok";
    };
    const lanBtn = btn(t("📶 Wi‑Fi ile eşitle"), "primary", async () => {
      if (!Lan.supported()) { lanPaint(); return; }
      lanBtn.disabled = true;
      lanStatus.dataset.kind = "run";
      try {
        const r = await Lan.run(lanHost.value, lanCode.value, s => { lanStatus.textContent = s; });
        lanStatus.textContent = tf("Wi‑Fi eşitleme tamam: gelen {}, giden {}", r.got, r.sent) + (r.files ? " · " + tf("{} belge", r.files) : "");
        lanStatus.dataset.kind = "ok";
        toast(t("Eşitlendi ✓"));
      } catch (e) {
        lanStatus.textContent = Lan.errText(e);
        lanStatus.dataset.kind = "err";
      } finally { lanBtn.disabled = false; }
    });
    const lanBox = h("div", { class: "lan-box" },
      h("h3", null, t("📶 Wi‑Fi ile eşitleme (internetsiz)")),
      h("p", { class: "muted" }, t("İnternet yokken: telefon ve bilgisayar aynı modeme / Wi‑Fi'a bağlı olsun. Bilgisayardaki ☁ Eşitleme penceresinde yazan adresi ve kodu girin. Aynı bulut hesabındaysanız kod gerekmez.")),
      field(t("Bilgisayarın adresi"), lanHost), field(t("Kod"), lanCode), lanStatus, h("div", { class: "row-btns" }, lanBtn));
    lanPaint();
    const entry = Sheets.open({ title: t("☁ Eşitleme"), cls: "form",
      body: h("div", { class: "form-grid" }, status, who,
        h("div", { class: "row-btns" }, nowBtn, outBtn),
        field(t("Firebase API key"), apiKey), field(t("Project ID"), projectId), field(t("E-posta"), email), field(t("Şifre"), password),
        advBtn, adv,
        h("div", { class: "row-btns" }, inBtn, upBtn), lanBox, help),
      footer: [btn(t("Kapat"), "light", () => Sheets.close(entry))] });
    entry.syncStatus = paint;
    paint();
  },

  /* ================================================================ menü */
  menu() {
    let entry;
    const item = (emo, label, fn) => h("button", { type: "button", class: "menu-item", onclick: () => { Sheets.close(entry); fn(); } },
      h("span", { class: "mi-emo" }, emo), h("span", null, label));
    const langs = seg(Object.entries(LANGS).map(([k, v]) => ({ v: k, label: v })), LANG, v => {
      setLang(v);
      Sheets.closeAll();
      App.build();
      Rem.scheduleAll();
    }, "seg3 lang-seg");
    const items = [
      item("📒", t("Kişi Defteri"), () => Forms.book()),
      item("📄", t("Tüm Kayıtlar Dökümü"), () => Forms.statement(null)),
      item("🔔", t("🔔 Hatırlatıcılar").replace("🔔 ", ""), () => Forms.reminders({})),
      item("☁", t("☁ Eşitleme").replace("☁ ", ""), () => Forms.sync()),
      item("💾", t("Yedek Al"), () => Backup.export()),
      item("♻", t("Yedekten Geri Yükle"), () => Backup.import()),
      item("⚙", t("⚙ Ayarlar").replace("⚙ ", ""), () => Forms.settings()),
      item("⬆", Upd.state === "available" ? tf("Güncelleme: {} hazır", "v" + Upd.info.surum) : t("Güncelleme"), () => Forms.update()),
      item("ℹ", t("Hakkında"), () => Forms.about()),
    ];
    if (bridgeHas("exitApp")) items.push(item("⏻", t("Çıkış"), async () => {
      if (await Dlg.confirm(t("Programdan çıkmak istiyor musunuz?"), t("Çıkış"))) bridge().exitApp();
    }));
    entry = Sheets.open({ title: t("Menü"), cls: "dialog menu side", dismissable: true,
      body: h("div", null, h("div", { class: "menu-brand" }, h("img", { src: "assets/logo.svg", alt: "", width: 44, height: 44 }),
        h("div", null, h("b", null, t(APP_TITLE)), h("div", { class: "muted" }, ltr("v" + appVersion())))),
        h("div", { class: "menu-list" }, items),
        h("div", { class: "field lang-field" }, h("span", { class: "flabel" }, "🌐 " + t("Dil")), langs.el)) });
  },

  about() {
    const st = Sync.status();
    const entry = Sheets.open({ title: t("Hakkında"), cls: "dialog",
      body: h("div", { class: "about" }, h("img", { src: "assets/logo.svg", alt: "", width: 96, height: 96 }),
        h("h3", null, t(APP_TITLE)), h("div", null, t("Sürüm") + " ", ltr(appVersion())),
        h("p", null, t("Kayıtlar, belgeler ve hatırlatıcılar bu cihazda saklanır. ☁ Eşitleme ile telefon ve bilgisayar aynı hesap üzerinden birlikte çalışır.")),
        h("p", { class: "muted" }, st.text),
        h("p", { class: "muted" }, t("Yedek Al ile düzenli yedek almanız önerilir."))),
      footer: [btn(t("Kapat"), "light", () => Sheets.close(entry))] });
  },
};

/* ================================================================ yedek */
const Backup = {
  async export() {
    toast(t("Yedek hazırlanıyor…"));
    try {
      const json = await Store.exportJson();
      const name = `AlacakVerecek_yedek_${stamp()}.json`;
      await saveBlobAs(textToBlob(json, "application/json"), "application/json", name);
      if (!bridgeHas("saveFile")) Dlg.alert(tf("Yedek alındı:\n{}\n\nYedeği USB bellek gibi ayrı bir yerde saklamanız önerilir.", name), t("Yedek"));
    } catch (e) {
      Dlg.alert(tf("Yedek alınamadı: {}", e && e.message || e), t("Hata"));
    }
  },
  import() {
    const fi = h("input", { type: "file", hidden: true, onchange: async e => {
      const f = e.target.files[0];
      fi.remove();
      if (!f) return;
      let text;
      try { text = await f.text(); JSON.parse(text); } catch (err) { Dlg.alert(t("Bu dosya geçerli bir yedek değil."), t("Hata")); return; }
      if (!(await Dlg.confirm(t("Bu cihazdaki tüm kayıtlar silinip yedekteki verilerle değiştirilecek. Devam edilsin mi?"), t("Yedekten Geri Yükle"), { danger: true }))) return;
      try {
        await Store.importJson(text);
        App.sel = App.isWide() ? "ALL" : null; App.view = "list";
        App.applyView();
        App.refresh();
        Rem.scheduleAll();
        Dlg.alert(t("Yedek geri yüklendi."), t("Yedek"));
      } catch (err) {
        Dlg.alert(t("Bu dosya geçerli bir yedek değil."), t("Hata"));
      }
    } });
    document.body.appendChild(fi);
    fi.click();
  },
};
