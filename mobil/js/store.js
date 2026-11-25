/* Yerel veri: IndexedDB (persons, tx, docs, blobs, rem, hist, meta) + bellekte tam kopya.
 * Satır alanları ESITLEME_SPEC.md §3 ile aynıdır; ek olarak yerel: dirty (0/1), bu (docs: parçalar yüklendi). */
'use strict';

const COLS = ["persons", "tx", "docs", "rem", "hist"];
const FIELDS = {
  persons: { s: ["name", "phone", "note", "phone2", "wa_phone", "tg_user", "sg_phone", "email", "address", "tags", "created_at"],
             b: ["ch_wa", "ch_tg", "ch_sg", "ch_call"], d: [], i: [] },
  tx: { s: ["person", "ts", "direction", "currency", "description", "created_at", "updated_at"], b: [], d: ["amount"], i: [] },
  docs: { s: ["tx", "name", "ext", "mime", "added_at"], b: [], d: [], i: ["size", "chunks"] },
  rem: { s: ["person", "kind", "currency", "due", "note", "created_at"], b: ["done"], d: ["amount"], i: [] },
  hist: { s: ["tx", "action", "at", "old"], b: [], d: [], i: [] },
};
const CHUNK = 700000;
const DB_NAME = "bereket_defter";

const Store = {
  idb: null,
  data: { persons: new Map(), tx: new Map(), docs: new Map(), rem: new Map(), hist: new Map() },
  meta: {},
  blobIds: new Set(),
  onChange: [],          // yerel değişiklikten sonra çağrılır (eşitleme zamanlayıcısı, hatırlatıcılar)

  open() {
    return new Promise((res, rej) => {
      const rq = indexedDB.open(DB_NAME, 1);
      rq.onupgradeneeded = () => {
        const db = rq.result;
        for (const s of [...COLS, "blobs", "meta"]) if (!db.objectStoreNames.contains(s)) db.createObjectStore(s, { keyPath: "id" });
      };
      rq.onsuccess = () => { this.idb = rq.result; res(); };
      rq.onerror = () => rej(rq.error);
    });
  },
  _all(store) {
    return new Promise((res, rej) => {
      const rq = this.idb.transaction(store).objectStore(store).getAll();
      rq.onsuccess = () => res(rq.result || []);
      rq.onerror = () => rej(rq.error);
    });
  },
  _keys(store) {
    return new Promise((res, rej) => {
      const os = this.idb.transaction(store).objectStore(store);
      const rq = os.getAllKeys ? os.getAllKeys() : os.getAll();
      rq.onsuccess = () => res((rq.result || []).map(x => (typeof x === "object" ? x.id : x)));
      rq.onerror = () => rej(rq.error);
    });
  },
  _put(store, objs) {
    if (!Array.isArray(objs)) objs = [objs];
    return new Promise((res, rej) => {
      const tr = this.idb.transaction(store, "readwrite");
      const os = tr.objectStore(store);
      for (const o of objs) os.put(o);
      tr.oncomplete = () => res();
      tr.onerror = () => rej(tr.error);
      tr.onabort = () => rej(tr.error);
    });
  },
  _del(store, id) {
    return new Promise((res, rej) => {
      const tr = this.idb.transaction(store, "readwrite");
      tr.objectStore(store).delete(id);
      tr.oncomplete = () => res();
      tr.onerror = () => rej(tr.error);
    });
  },
  _clear(stores) {
    return new Promise((res, rej) => {
      const tr = this.idb.transaction(stores, "readwrite");
      for (const s of stores) tr.objectStore(s).clear();
      tr.oncomplete = () => res();
      tr.onerror = () => rej(tr.error);
    });
  },
  _logErr(e) { console.warn("IndexedDB yazılamadı", e); },

  async load() {
    for (const c of COLS) {
      const m = new Map();
      for (const r of await this._all(c)) m.set(r.id, r);
      this.data[c] = m;
    }
    this.meta = {};
    for (const r of await this._all("meta")) this.meta[r.id] = r.v;
    this.blobIds = new Set(await this._keys("blobs"));
  },
  setMeta(k, v) {
    this.meta[k] = v;
    this._put("meta", { id: k, v }).catch(e => this._logErr(e));
  },

  /* ---------------- satır düzeyi */
  get(col, id) { const r = this.data[col].get(id); return r && !r.del ? r : null; },
  live(col) { const out = []; for (const r of this.data[col].values()) if (!r.del) out.push(r); return out; },
  _nextM(old) { const n = Date.now(); return old && old.m >= n ? old.m + 1 : n; },
  /** yerel değişiklik: m yenilenir, dirty=1, kaydedilir */
  save(col, row, quiet) {
    const old = this.data[col].get(row.id);
    row.m = this._nextM(old);
    row.dirty = 1;
    row.del = false;
    this.data[col].set(row.id, row);
    this._put(col, row).catch(e => this._logErr(e));
    if (!quiet) this.changed();
    return row;
  },
  tomb(col, id, quiet) {
    const old = this.data[col].get(id);
    if (!old || old.del) return;
    this.archive(col, old, "yerel");
    const row = { id, m: this._nextM(old), del: true, dirty: 1 };
    if (col === "docs") row._ch = old.chunks || 0;   // v1.21: belge dosyası silinmez (arşivden geri alınabilir)
    this.data[col].set(id, row);
    this._put(col, row).catch(e => this._logErr(e));
    if (!quiet) this.changed();
  },
  /* ---------------- v1.21: kalıcı silme yok — silinen kayıt arşive, çakışmada eski hal yedeğe (meta: arsiv / cakisma) */
  archive(col, row, kaynak) {
    if (!row || row.del) return;
    const a = (this.meta.arsiv || []).slice(0, 499);
    const r = Object.assign({}, row); delete r.dirty;
    a.unshift({ at: Date.now(), kaynak: kaynak || "yerel", col, row: r });
    this.setMeta("arsiv", a);
  },
  conflict(col, row) {
    if (!row || row.del) return;
    const a = (this.meta.cakisma || []).slice(0, 499);
    const r = Object.assign({}, row); delete r.dirty;
    a.unshift({ at: Date.now(), col, row: r });
    this.setMeta("cakisma", a);
  },
  /** arşivdeki kaydı geri koyar (aynı kimlik, yeni değişiklik zamanı → diğer cihazlara da geri gelir). false: bağlı kişi/kayıt yok */
  restore(i) {
    const a = (this.meta.arsiv || []).slice();
    const it = a[i];
    if (!it) return false;
    const r = Object.assign({}, it.row);
    if ((it.col === "tx" || it.col === "rem") && !this.person(r.person)) return false;
    if (it.col === "docs" && !this.tx(r.tx)) return false;
    if (it.col === "docs") r.bu = this.blobIds.has(r.id) ? 0 : 1;
    this.save(it.col, r);
    a.splice(i, 1);
    this.setMeta("arsiv", a);
    return true;
  },

  /** eşitleme: uzak satırı yerel hale getirir (dirty=0) */
  putRemote(col, row) { this.data[col].set(row.id, row); return row; },
  flush(col, rows) { return this._put(col, rows).catch(e => this._logErr(e)); },
  persist(col, row) { this._put(col, row).catch(e => this._logErr(e)); },
  changed() { for (const f of this.onChange) { try { f(); } catch (e) { console.warn(e); } } },

  /* ---------------- dosyalar */
  putBlob(id, blob) { this.blobIds.add(id); return this._put("blobs", { id, blob }); },
  getBlob(id) {
    return new Promise((res, rej) => {
      const rq = this.idb.transaction("blobs").objectStore("blobs").get(id);
      rq.onsuccess = () => {
        const r = rq.result;
        if (!r) return res(null);
        res(r.blob instanceof Blob ? r.blob : new Blob([r.blob]));
      };
      rq.onerror = () => rej(rq.error);
    });
  },
  delBlob(id) { this.blobIds.delete(id); Thumbs.drop(id); this._del("blobs", id).catch(e => this._logErr(e)); },

  /* ---------------- kişiler */
  persons(search) {
    let rows = this.live("persons");
    const q = lower(search).trim();
    if (q) rows = rows.filter(p => [p.name, p.phone, p.phone2, p.email].some(v => lower(v).includes(q)));
    return rows.sort((a, b) => String(a.name).localeCompare(String(b.name), LANG === "ar" ? "ar" : "tr", { sensitivity: "base" }));
  },
  person(id) { return this.get("persons", id); },
  addPerson(fields) {
    const p = { id: uuidHex(), created_at: nowStr() };
    for (const k of FIELDS.persons.s) if (!(k in p)) p[k] = "";
    for (const k of FIELDS.persons.b) p[k] = false;
    this._applyContact(p, fields);
    this.save("persons", p);
    return p.id;
  },
  _applyContact(p, fields) {
    for (const k in fields) {
      if (FIELDS.persons.b.includes(k)) p[k] = !!fields[k];
      else if (FIELDS.persons.s.includes(k) && k !== "created_at") {
        const v = String(fields[k] == null ? "" : fields[k]).trim();
        if (k === "name" && !v) continue;
        p[k] = v;
      }
    }
  },
  updateContact(id, fields) {
    const old = this.person(id);
    if (!old) return;
    const p = Object.assign({}, old);
    this._applyContact(p, fields);
    this.save("persons", p);
  },
  setChannel(id, ch, on) { this.updateContact(id, { ["ch_" + ch]: on }); },
  txCount(pid) { let n = 0; for (const r of this.data.tx.values()) if (!r.del && r.person === pid) n++; return n; },
  deletePerson(pid) {
    for (const tx of this.live("tx")) if (tx.person === pid) {
      for (const d of this.docsOf(tx.id)) this.tomb("docs", d.id, true);
      this.tomb("tx", tx.id, true);
    }
    for (const r of this.live("rem")) if (r.person === pid) this.tomb("rem", r.id, true);
    this.tomb("persons", pid, true);
    this.changed();
  },

  /* ---------------- bakiyeler */
  /** {cur: [verilen, alinan, bakiye]}; bakiye > 0 => alacak */
  balances(pid, until) {
    const res = {};
    for (const c of CURRENCIES) res[c] = [0, 0, 0];
    for (const r of this.data.tx.values()) {
      if (r.del || !res[r.currency]) continue;
      if (pid && r.person !== pid) continue;
      if (!pid && !this.person(r.person)) continue;
      if (until && !(r.ts < until)) continue;
      res[r.currency][r.direction === "VERDIM" ? 0 : 1] += Number(r.amount) || 0;
    }
    for (const c of CURRENCIES) res[c][2] = res[c][0] - res[c][1];
    return res;
  },
  /** her para birimi için [toplam alacak, toplam verecek] (kişi bazında netleştirilmiş) */
  totalsOverall() {
    const per = new Map();
    for (const r of this.data.tx.values()) {
      if (r.del || !this.person(r.person) || !CURRENCIES.includes(r.currency)) continue;
      const k = r.person + "|" + r.currency;
      per.set(k, (per.get(k) || 0) + (r.direction === "VERDIM" ? 1 : -1) * (Number(r.amount) || 0));
    }
    const res = {};
    for (const c of CURRENCIES) res[c] = [0, 0];
    for (const [k, b] of per) {
      const c = k.split("|")[1];
      if (b > 0.000001) res[c][0] += b; else if (b < -0.000001) res[c][1] += -b;
    }
    return res;
  },

  /* ---------------- kayıtlar */
  docCount(txId) { let n = 0; for (const d of this.data.docs.values()) if (!d.del && d.tx === txId) n++; return n; },
  /** artan sırada (eskiden yeniye) — masaüstü ORDER BY ts */
  transactions({ pid, start, end, currency, text } = {}) {
    const q = lower(text).trim();
    const out = [];
    for (const r of this.data.tx.values()) {
      if (r.del) continue;
      const p = this.person(r.person);
      if (!p) continue;
      if (pid && r.person !== pid) continue;
      if (start && r.ts < start) continue;
      if (end && r.ts > end) continue;
      if (currency && r.currency !== currency) continue;
      if (q && !lower(r.description).includes(q) && !lower(p.name).includes(q)) continue;
      out.push(r);
    }
    return out.sort((a, b) => (a.ts < b.ts ? -1 : a.ts > b.ts ? 1 : (a.created_at < b.created_at ? -1 : a.created_at > b.created_at ? 1 : 0)));
  },
  tx(id) { return this.get("tx", id); },
  personName(id) { const p = this.data.persons.get(id); return p && !p.del ? p.name : "?"; },
  addTx(v) {
    const r = { id: uuidHex(), person: v.person, ts: ts16(v.ts), direction: v.direction, currency: v.currency,
      amount: v.amount, description: String(v.description || "").trim(), created_at: nowStr(), updated_at: "" };
    this.save("tx", r, true);
    return r.id;
  },
  _hist(old, action) {
    const o = { ts: old.ts, direction: old.direction, currency: old.currency, amount: old.amount,
      description: old.description || "", person: old.person, person_name: this.personName(old.person) };
    this.save("hist", { id: uuidHex(), tx: old.id, action, at: nowStr(), old: JSON.stringify(o) }, true);
  },
  updateTx(id, v) {
    const old = this.tx(id);
    if (!old) return;
    this._hist(old, "DEGISTIRILDI");
    const r = Object.assign({}, old, { person: v.person, ts: ts16(v.ts), direction: v.direction, currency: v.currency,
      amount: v.amount, description: String(v.description || "").trim(), updated_at: nowStr() });
    this.save("tx", r, true);
  },
  deleteTx(id) {
    const old = this.tx(id);
    if (!old) return;
    this._hist(old, "SILINDI");
    for (const d of this.docsOf(id)) this.tomb("docs", d.id, true);
    this.tomb("tx", id, true);
    this.changed();
  },
  history(txId) {
    return this.live("hist").filter(x => x.tx === txId).sort((a, b) => (a.at < b.at ? -1 : a.at > b.at ? 1 : a.m - b.m));
  },

  /* ---------------- belgeler */
  docsOf(txId) {
    return this.live("docs").filter(d => d.tx === txId).sort((a, b) => (a.added_at < b.added_at ? -1 : a.added_at > b.added_at ? 1 : a.m - b.m));
  },
  async addDoc(txId, file) {
    const id = uuidHex();
    const name = file.name || ("belge" + extOf("", file.type));
    const size = file.size || 0;
    const blob = file instanceof Blob ? file : new Blob([file]);
    await this.putBlob(id, blob);
    this.save("docs", { id, tx: txId, name, ext: extOf(name, file.type), mime: file.type || MIME_BY_EXT[extOf(name, "")] || "",
      size, chunks: Math.ceil(size / CHUNK), added_at: nowStr(), bu: 0 }, true);
    return id;
  },
  deleteDoc(id) { this.tomb("docs", id, true); },

  /* ---------------- hatırlatıcılar */
  reminders({ pid, pendingOnly = true, until } = {}) {
    return this.live("rem").filter(r => this.person(r.person) && (!pid || r.person === pid) && (!pendingOnly || !r.done) &&
      (!until || ts16(r.due) <= until))
      .sort((a, b) => (a.done - b.done) || (ts16(a.due) < ts16(b.due) ? -1 : ts16(a.due) > ts16(b.due) ? 1 : 0) ||
        (a.created_at < b.created_at ? -1 : 1));
  },
  reminder(id) { return this.get("rem", id); },
  addReminder(v) {
    const r = { id: uuidHex(), person: v.person, kind: v.kind, currency: v.currency, amount: v.amount || 0, due: ts16(v.due),
      note: String(v.note || "").trim(), done: false, created_at: nowStr() };
    this.save("rem", r);
    return r.id;
  },
  updateReminder(id, v) {
    const old = this.reminder(id);
    if (!old) return;
    if (v.due) v = Object.assign({}, v, { due: ts16(v.due) });
    this.save("rem", Object.assign({}, old, v, { note: String(v.note != null ? v.note : old.note || "").trim() }));
  },
  setReminderDone(id, done) { const r = this.reminder(id); if (r) this.save("rem", Object.assign({}, r, { done: !!done })); },
  deleteReminder(id) { this.tomb("rem", id); },

  /* ---------------- yedek */
  async exportJson() {
    const out = { app: "bereket-alacak-verecek", format: 1, version: appVersion(), created: nowStr() };
    for (const c of COLS) out[c] = [...this.data[c].values()].map(r => { const o = Object.assign({}, r); delete o.dirty; delete o.bu; return o; });
    out.files = {};
    for (const d of this.live("docs")) {
      const b = await this.getBlob(d.id);
      if (b) out.files[d.id] = await blobToBase64(b);
    }
    return JSON.stringify(out);
  },
  async importJson(text) {
    const data = JSON.parse(text);
    if (!data || data.app !== "bereket-alacak-verecek" || !Array.isArray(data.persons)) throw new Error("format");
    await this._clear([...COLS, "blobs"]);
    const now = Date.now();
    for (const c of COLS) {
      const m = new Map();
      const rows = (data[c] || []).filter(r => r && typeof r.id === "string").map(r => Object.assign({}, r, { m: now, dirty: 1, bu: 0 }));
      for (const r of rows) m.set(r.id, r);
      this.data[c] = m;
      await this._put(c, rows);
    }
    this.blobIds = new Set();
    for (const id in (data.files || {})) {
      const d = this.data.docs.get(id);
      if (!d || d.del) continue;
      await this.putBlob(id, new Blob([base64ToBytes(data.files[id])], { type: d.mime || "" }));
    }
    Thumbs.reset();
    this.changed();
  },
};

/* küçük resim URL önbelleği */
const Thumbs = {
  urls: new Map(),
  async url(id) {
    if (this.urls.has(id)) return this.urls.get(id);
    const b = await Store.getBlob(id);
    if (!b) return null;
    const u = URL.createObjectURL(b);
    this.urls.set(id, u);
    return u;
  },
  drop(id) { const u = this.urls.get(id); if (u) { URL.revokeObjectURL(u); this.urls.delete(id); } },
  reset() { for (const u of this.urls.values()) URL.revokeObjectURL(u); this.urls.clear(); },
};
