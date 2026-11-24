/* Firebase eşitleme — yalnızca REST (ESITLEME_SPEC.md §1-4). Arayüzü asla bloklamaz. */
'use strict';

class SyncError extends Error {
  constructor(code, detail) { super(code + (detail ? ": " + detail : "")); this.code = code; this.detail = detail || ""; }
}

const DATE_FIELDS = new Set(["ts", "due", "created_at", "updated_at", "added_at", "at"]);
const AUTH_ERRORS = {
  EMAIL_EXISTS: "Bu e-posta ile zaten bir hesap var. 'Giriş yap' düğmesini kullanın.",
  EMAIL_NOT_FOUND: "Bu e-posta ile hesap bulunamadı. Önce 'Hesap oluştur' düğmesine basın.",
  INVALID_PASSWORD: "E-posta veya şifre yanlış.",
  INVALID_LOGIN_CREDENTIALS: "E-posta veya şifre yanlış.",
  WEAK_PASSWORD: "Şifre çok zayıf (en az 6 karakter olmalı).",
  INVALID_EMAIL: "E-posta adresi geçersiz.",
  MISSING_PASSWORD: "Şifre yazılmamış.",
  MISSING_EMAIL: "E-posta yazılmamış.",
  OPERATION_NOT_ALLOWED: "Firebase'de E-posta/Şifre ile giriş açık değil (Authentication → Sign-in method → Email/Password).",
  CONFIGURATION_NOT_FOUND: "Firebase Authentication bu projede etkinleştirilmemiş veya Project ID yanlış.",
  API_KEY_INVALID: "API anahtarı (API key) geçersiz.",
  TOO_MANY_ATTEMPTS_TRY_LATER: "Çok fazla deneme yapıldı. Biraz sonra tekrar deneyin.",
  USER_DISABLED: "Bu hesap devre dışı bırakılmış.",
  TOKEN_EXPIRED: "Oturumun süresi doldu, tekrar giriş yapın.",
  INVALID_REFRESH_TOKEN: "Oturumun süresi doldu, tekrar giriş yapın.",
  USER_NOT_FOUND: "Oturumun süresi doldu, tekrar giriş yapın.",
  NETWORK: "İnternet bağlantısı yok veya sunucuya ulaşılamadı.",
  PERMISSION_DENIED: "Firestore kuralları ayarlanmamış: Firebase konsolunda Firestore → Rules bölümüne yardımdaki kuralları yapıştırıp yayınlayın.",
  NOT_FOUND: "Firestore veritabanı oluşturulmamış: Firebase konsolunda Firestore Database → Create database.",
  NO_CONFIG: "Önce API key, Project ID, e-posta ve şifreyi yazın.",
  NOT_SIGNED_IN: "Giriş yapılmamış.",
};
function syncErrText(e) {
  if (e instanceof SyncError) {
    const k = Object.keys(AUTH_ERRORS).find(k => e.code === k || e.code.startsWith(k));
    if (k) return t(AUTH_ERRORS[k]);
    if (/API key not valid/i.test(e.detail) || /API key not valid/i.test(e.code)) return t(AUTH_ERRORS.API_KEY_INVALID);
    return tf("Eşitleme hatası: {}", e.code + (e.detail ? " " + e.detail : ""));
  }
  return tf("Eşitleme hatası: {}", (e && e.message) || String(e));
}

const Sync = {
  idToken: "", exp: 0,
  running: false, again: false, timer: null, interval: null,
  lastErr: "", lastOk: null, listeners: [],

  cfg() { return Store.meta.sync || {}; },
  setCfg(patch) { Store.setMeta("sync", Object.assign({}, this.cfg(), patch)); },
  signedIn() { const c = this.cfg(); return !!(c.refreshToken && c.uid && c.apiKey && c.projectId); },
  ep() {
    const c = this.cfg();
    const emu = String(c.emulator || "").trim();
    const pid = encodeURIComponent(String(c.projectId || "").trim());
    const root = `projects/${pid}/databases/(default)/documents`;
    return {
      auth: emu ? `http://${emu}:9099/identitytoolkit.googleapis.com/v1` : "https://identitytoolkit.googleapis.com/v1",
      token: emu ? `http://${emu}:9099/securetoken.googleapis.com/v1/token` : "https://securetoken.googleapis.com/v1/token",
      fs: (emu ? `http://${emu}:8080/v1/` : "https://firestore.googleapis.com/v1/") + root,
      root,
    };
  },
  status() {
    if (this.running) return { kind: "run", text: t("Eşitleniyor…") };
    if (this.lastErr) return { kind: "err", text: this.lastErr };
    if (!this.signedIn()) return { kind: "off", text: t("Eşitleme kapalı (giriş yapılmamış)") };
    const at = this.lastOk || (Store.meta.lastSync ? new Date(Store.meta.lastSync) : null);
    return { kind: "ok", text: at ? tf("Son eşitleme: {}", hhmm(at)) : t("Henüz eşitlenmedi") };
  },
  emit() { for (const f of this.listeners) { try { f(); } catch (e) { console.warn(e); } } },

  /* ---------------- HTTP */
  async _fetch(url, opts) {
    let res;
    try { res = await fetch(url, opts); } catch (e) { throw new SyncError("NETWORK"); }
    let body = null;
    const txt = await res.text();
    try { body = txt ? JSON.parse(txt) : null; } catch (e) { body = null; }
    return { res, body, txt };
  },
  _authErr(body, status) {
    const msg = (body && body.error && (body.error.message || body.error.status)) || ("HTTP " + status);
    const code = String(msg).split(/[ :]/)[0];
    return new SyncError(code, String(msg).slice(code.length).replace(/^[ :]+/, ""));
  },
  async authCall(path, payload) {
    const c = this.cfg();
    const { res, body } = await this._fetch(`${this.ep().auth}/${path}?key=${encodeURIComponent(c.apiKey)}`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    if (!res.ok) throw this._authErr(body, res.status);
    return body;
  },
  async signIn(cfg, password, create) {
    const prevUid = this.cfg().lastUid || "";
    this.setCfg({ apiKey: cfg.apiKey.trim(), projectId: cfg.projectId.trim(), emulator: (cfg.emulator || "").trim(), email: cfg.email.trim() });
    if (!cfg.apiKey.trim() || !cfg.projectId.trim() || !cfg.email.trim() || !password) throw new SyncError("NO_CONFIG");
    const b = await this.authCall(create ? "accounts:signUp" : "accounts:signInWithPassword",
      { email: cfg.email.trim(), password, returnSecureToken: true });
    this.idToken = b.idToken;
    this.exp = Date.now() + (parseInt(b.expiresIn, 10) || 3600) * 1000;
    const patch = { uid: b.localId, refreshToken: b.refreshToken, email: b.email || cfg.email.trim(), lastUid: b.localId };
    if (prevUid !== b.localId) {
      // başka hesap: imleçleri sıfırla, yerel her şeyi yeniden yükle
      patch.cursors = {};
      for (const col of COLS) {
        const rows = [...Store.data[col].values()];
        for (const r of rows) { r.dirty = 1; if (col === "docs") r.bu = 0; }
        Store.flush(col, rows);
      }
    }
    this.setCfg(patch);
    this.lastErr = "";
    this.emit();
    this.start();
    this.runSoon(50);
  },
  signOut() {
    this.idToken = ""; this.exp = 0; this.lastErr = "";
    this.setCfg({ refreshToken: "", uid: "" });
    this.emit();
  },
  async ensureToken(force) {
    const c = this.cfg();
    if (!this.signedIn()) throw new SyncError("NOT_SIGNED_IN");
    if (!force && this.idToken && this.exp - Date.now() > 5 * 60 * 1000) return this.idToken;
    const { res, body } = await this._fetch(`${this.ep().token}?key=${encodeURIComponent(c.apiKey)}`, {
      method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: "grant_type=refresh_token&refresh_token=" + encodeURIComponent(c.refreshToken) });
    if (!res.ok) throw this._authErr(body, res.status);
    this.idToken = body.id_token;
    this.exp = Date.now() + (parseInt(body.expires_in, 10) || 3600) * 1000;
    if (body.refresh_token && body.refresh_token !== c.refreshToken) this.setCfg({ refreshToken: body.refresh_token });
    return this.idToken;
  },
  async fs(method, path, payload, retried) {
    const tok = await this.ensureToken();
    const opts = { method, headers: { Authorization: "Bearer " + tok } };
    if (payload !== undefined) { opts.headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(payload); }
    const { res, body } = await this._fetch(this.ep().fs + path, opts);
    if (res.status === 401 && !retried) { await this.ensureToken(true); return this.fs(method, path, payload, true); }
    if (!res.ok) {
      const err = Array.isArray(body) ? (body[0] || {}).error : body && body.error;
      const st = (err && err.status) || "";
      if (res.status === 404 && method === "GET" && path.includes("/blobs/")) return null;
      if (res.status === 403 || st === "PERMISSION_DENIED") throw new SyncError("PERMISSION_DENIED", err && err.message);
      if (res.status === 404 || st === "NOT_FOUND") throw new SyncError("NOT_FOUND", err && err.message);
      throw new SyncError(st || ("HTTP_" + res.status), err && err.message);
    }
    return body;
  },

  /* ---------------- kodlama */
  docName(col, id) { return `${this.ep().root}/users/${this.cfg().uid}/${col}/${id}`; },
  encode(col, r) {
    const f = { id: { stringValue: r.id }, m: { integerValue: String(r.m) } };
    if (r.del) { f.del = { booleanValue: true }; return f; }
    f.del = { booleanValue: false };
    const F = FIELDS[col];
    for (const k of F.s) f[k] = { stringValue: String(r[k] == null ? "" : r[k]) };
    for (const k of F.b) f[k] = { booleanValue: !!r[k] };
    for (const k of F.d) f[k] = { doubleValue: Number(r[k]) || 0 };
    for (const k of F.i) f[k] = { integerValue: String(Math.round(Number(r[k]) || 0)) };
    return f;
  },
  val(v) {
    if (!v) return undefined;
    if ("stringValue" in v) return v.stringValue;
    if ("integerValue" in v) return Number(v.integerValue);
    if ("doubleValue" in v) return Number(v.doubleValue);
    if ("booleanValue" in v) return !!v.booleanValue;
    if ("timestampValue" in v) return v.timestampValue;
    if ("bytesValue" in v) return v.bytesValue;
    if ("nullValue" in v) return null;
    return undefined;
  },
  decode(col, doc) {
    const f = doc.fields || {};
    const id = this.val(f.id) || doc.name.split("/").pop();
    const r = { id: String(id), m: Number(this.val(f.m)) || 0 };
    if (this.val(f.del) === true) { r.del = true; return r; }
    r.del = false;
    const F = FIELDS[col];
    for (const k of F.s) {
      const v = this.val(f[k]);
      r[k] = v == null ? "" : String(v);
      if (/^\d{4}-\d\d-\d\dT\d\d:\d\d/.test(r[k]) && DATE_FIELDS.has(k)) r[k] = r[k].slice(0, 10) + " " + r[k].slice(11, 19).replace(/[^\d:]+$/, "");
    }
    for (const k of F.b) { const v = this.val(f[k]); r[k] = v === true || v === 1 || v === "1"; }
    for (const k of F.d) r[k] = Number(this.val(f[k])) || 0;
    for (const k of F.i) r[k] = Math.round(Number(this.val(f[k])) || 0);
    return r;
  },

  /* ---------------- çalıştırma */
  start() {
    if (!this.interval) this.interval = setInterval(() => this.run(), 60000);
  },
  runSoon(ms) {
    clearTimeout(this.timer);
    this.timer = setTimeout(() => this.run(), ms == null ? 3000 : ms);
  },
  async run() {
    if (!this.signedIn()) return false;
    if (this.running) { this.again = true; return false; }
    this.running = true;
    this.emit();
    let changed = false;
    try {
      await this.ensureToken();
      changed = await this.pull();   // §4: önce PULL, sonra PUSH (eski çevrimdışı düzenleme yenisini ezmesin)
      await this.push();
      if (await this.fetchBlobs()) changed = true;
      this.lastOk = new Date();
      Store.setMeta("lastSync", this.lastOk.getTime());
      this.lastErr = "";
    } catch (e) {
      this.lastErr = syncErrText(e);
      console.info("Eşitleme:", e && e.message);
    } finally {
      this.running = false;
      this.emit();
      if (changed && typeof App !== "undefined") App.onRemoteChange();
      if (this.again) { this.again = false; this.runSoon(300); }
    }
    return true;
  },
  async commit(writes) {
    if (writes.length) await this.fs("POST", ":commit", { writes });
  },
  async push() {
    const dirty = {};
    for (const col of COLS) dirty[col] = [...Store.data[col].values()].filter(r => r.dirty);
    // 1) yeni belgelerin dosya parçaları (en çok 8 yazma / istek)
    for (const d of dirty.docs) {
      if (d.del || d.bu) continue;
      const blob = await Store.getBlob(d.id);
      if (!blob) continue;
      const n = Math.ceil(blob.size / CHUNK);
      let writes = [];
      for (let i = 0; i < n; i++) {
        const b64 = await blobToBase64(blob.slice(i * CHUNK, (i + 1) * CHUNK));
        writes.push({ update: { name: this.docName("blobs", `${d.id}_${i}`), fields: {
          doc: { stringValue: d.id }, i: { integerValue: String(i) }, d: { bytesValue: b64 }, m: { integerValue: String(d.m) } } },
          updateTransforms: [{ fieldPath: "sm", setToServerValue: "REQUEST_TIME" }] });
        if (writes.length >= 8) { await this.commit(writes); writes = []; }
      }
      await this.commit(writes);
      const cur = Store.data.docs.get(d.id);
      if (cur && !cur.del) { cur.bu = 1; if (cur.chunks !== n) cur.chunks = n; Store.persist("docs", cur); }
    }
    // 2) satırlar: ebeveynler önce, ≤ 200 yazma / istek
    let batch = [], snap = [];
    const flush = async () => {
      if (!batch.length) return;
      await this.commit(batch);
      const touched = {};
      for (const [col, id, m] of snap) {
        const r = Store.data[col].get(id);
        if (r && r.m === m && r.dirty) { r.dirty = 0; (touched[col] = touched[col] || []).push(r); }
      }
      for (const col in touched) await Store.flush(col, touched[col]);
      batch = []; snap = [];
    };
    for (const col of COLS) {
      for (const r0 of dirty[col]) {
        const r = Store.data[col].get(r0.id);
        if (!r || !r.dirty) continue;
        const extra = [];
        if (col === "docs" && r.del && r._ch) for (let i = 0; i < r._ch; i++) extra.push({ delete: this.docName("blobs", `${r.id}_${i}`) });
        if (batch.length + 1 + extra.length > 200) await flush();
        batch.push({ update: { name: this.docName(col, r.id), fields: this.encode(col, r) },
          updateTransforms: [{ fieldPath: "sm", setToServerValue: "REQUEST_TIME" }] });
        for (const x of extra) batch.push(x);
        snap.push([col, r.id, r.m]);
      }
    }
    await flush();
  },
  parentOk(col, r) {
    if (r.del) return true;
    if (col === "tx" || col === "rem") return !!Store.person(r.person);
    if (col === "docs") return !!Store.tx(r.tx);
    return true;
  },
  same(col, a, b) {
    if (!a || !!a.del !== !!b.del) return false;
    if (b.del) return true;
    const F = FIELDS[col];
    for (const k of [...F.s, ...F.b, ...F.d, ...F.i]) if (String(a[k] == null ? "" : a[k]) !== String(b[k] == null ? "" : b[k])) {
      if (F.b.includes(k) && !!a[k] === !!b[k]) continue;
      return false;
    }
    return true;
  },
  /** birleştirme kuralı §4; true = görünür bir şey değişti */
  apply(col, r, toSave) {
    const loc = Store.data[col].get(r.id);
    if (loc && loc.dirty && loc.m > r.m) return false;
    if (loc && !loc.dirty && loc.m === r.m && !!loc.del === !!r.del) return false;   // kendi yazdığımız / değişmemiş
    if (r.del) {
      const was = loc && !loc.del;
      if (was) Store.archive(col, loc, "uzak");   // v1.21: başka cihazda silinen kayıt burada arşivlenir (belge dosyası da kalır)
      const row = { id: r.id, m: r.m, del: true, dirty: 0 };
      Store.putRemote(col, row);
      toSave.push(row);
      return !!was;
    }
    const changed = !this.same(col, loc, r);
    if (changed && loc && loc.dirty && !loc.del) Store.conflict(col, loc);   // gönderilmemiş eski değişiklik → çakışma yedeği
    r.dirty = 0;
    if (col === "docs") r.bu = 1;
    Store.putRemote(col, r);
    toSave.push(r);
    return changed;
  },
  async pull() {
    const cfg = this.cfg();
    const uid = cfg.uid;
    const cursors = Object.assign({}, cfg.cursors || {});
    let changed = false;
    const aside = [];
    for (const col of COLS) {
      let cur = cursors[col] || { sm: "1970-01-01T00:00:00Z", name: "" };
      let startAt = null;
      for (;;) {
        const q = { structuredQuery: {
          from: [{ collectionId: col }],
          where: { fieldFilter: { field: { fieldPath: "sm" }, op: "GREATER_THAN_OR_EQUAL", value: { timestampValue: cur.sm } } },
          orderBy: [{ field: { fieldPath: "sm" }, direction: "ASCENDING" }, { field: { fieldPath: "__name__" }, direction: "ASCENDING" }],
          limit: 300 } };
        if (startAt) q.structuredQuery.startAt = startAt;
        const res = await this.fs("POST", `/users/${uid}:runQuery`, q);
        const docs = (Array.isArray(res) ? res : []).filter(x => x && x.document).map(x => x.document);
        const toSave = [];
        for (const d of docs) {
          const r = this.decode(col, d);
          if (!this.parentOk(col, r)) { aside.push([col, r]); continue; }
          if (this.apply(col, r, toSave)) changed = true;
        }
        if (toSave.length) await Store.flush(col, toSave);
        const last = docs[docs.length - 1];
        if (last) {
          const sm = last.fields && last.fields.sm && last.fields.sm.timestampValue;
          if (sm) {
            cur = { sm, name: last.name };
            cursors[col] = cur;
            this.setCfg({ cursors: Object.assign({}, cursors) });
            startAt = { before: false, values: [{ timestampValue: sm }, { referenceValue: last.name }] };
          }
        }
        if (docs.length < 300 || !startAt) break;
      }
    }
    // ebeveyni eksik olanları sona bırak, tekrar dene
    let progress = true;
    while (aside.length && progress) {
      progress = false;
      for (let i = aside.length - 1; i >= 0; i--) {
        const [col, r] = aside[i];
        if (!this.parentOk(col, r)) continue;
        const toSave = [];
        if (this.apply(col, r, toSave)) changed = true;
        await Store.flush(col, toSave);
        aside.splice(i, 1);
        progress = true;
      }
    }
    for (const [col, r] of aside) console.info(`Eşitleme: ${col}/${r.id} atlandı (bağlı kayıt yok)`);
    return changed;
  },
  async fetchBlobs() {
    const uid = this.cfg().uid;
    let got = false;
    for (const d of Store.live("docs")) {
      if (Store.blobIds.has(d.id) || !Store.tx(d.tx)) continue;
      const parts = [];
      let ok = true;
      for (let i = 0; i < (d.chunks || 0); i++) {
        const doc = await this.fs("GET", `/users/${uid}/blobs/${d.id}_${i}`);
        const b64 = doc && doc.fields && doc.fields.d && doc.fields.d.bytesValue;
        if (b64 == null) { ok = false; break; }
        parts.push(base64ToBytes(b64));
      }
      if (!ok) continue;
      await Store.putBlob(d.id, new Blob(parts, { type: d.mime || MIME_BY_EXT[d.ext] || "" }));
      got = true;
    }
    return got;
  },
};
