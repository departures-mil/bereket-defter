/* Wi‑Fi (aynı modem / router) üzerinden internetsiz eşitleme — telefon ⇄ bilgisayar (v1.14).
 * Bilgisayardaki Bereket Defter (masaüstü 1.14+) açıkken: adres (192.168.x.x:47341) + 6 haneli kod.
 * İki cihaz aynı bulut hesabındaysa kod sorulmaz (hesaptan türetilen anahtar).
 * Kayıtlar bulut eşitlemesiyle AYNI biçimde (Sync.encode/decode) ve AYNI kuralla (Sync.apply) birleşir: son değişen kazanır,
 * silinenler işaretle yayılır, hiçbir şey körü körüne üzerine yazılmaz. Wi‑Fi'dan gelenler "kirli" işaretlenir → internet gelince
 * buluta da gider. Belgeler (fotoğraf/dosya) eksik olan tarafa aktarılır.
 * Telefon uygulaması 1.8 (nativeCode 15) gerekir: eski APK https sayfadan yerel ağa http isteğini engelliyordu. */
const LAN_PORT = 47341;
const Lan = {
  busy: false,
  cfg() { return Store.meta.lan || {}; },
  setCfg(p) { Store.setMeta("lan", Object.assign({}, this.cfg(), p)); },
  supported() { return typeof Upd === "undefined" || !bridge() || Upd.nativeCode() >= 15; },
  async uidKey() {
    const uid = Sync.cfg().uid;
    if (!uid || !(window.crypto && crypto.subtle)) return "";
    const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode("bereket-lan:" + uid));
    return Array.from(new Uint8Array(b)).map(x => x.toString(16).padStart(2, "0")).join("").slice(0, 24);
  },
  base(host) {
    host = String(host || "").trim().replace(/^https?:\/\//, "").replace(/\/.*$/, "");
    if (!host) return "";
    if (!/:\d+$/.test(host)) host += ":" + LAN_PORT;
    return "http://" + host;
  },
  async post(base, path, body, ms) {
    const ac = new AbortController();
    const tm = setTimeout(() => ac.abort(), ms || 60000);
    let res;
    try {
      res = await fetch(base + "/bereket/lan/" + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body), signal: ac.signal });
    } catch (e) { throw new Error("NET"); } finally { clearTimeout(tm); }
    if (res.status === 403) throw new Error("KEY");
    let j = null;
    try { j = await res.json(); } catch (e) { j = null; }
    if (!res.ok || !j) throw new Error((j && j.error) || ("HTTP " + res.status));
    return j;
  },
  /** progress(metin) ile ilerleme bildirir. Döner: {got, sent, files} */
  async run(host, code, progress) {
    if (this.busy) throw new Error("BUSY");
    const base = this.base(host);
    if (!base) throw new Error("ADDR");
    const say = s => { try { progress && progress(s); } catch (e) { /* */ } };
    this.busy = true;
    try {
      const key = String(code || "").trim() || await this.uidKey();
      say(t("Bilgisayara bağlanılıyor…"));
      const docs = {};
      for (const col of COLS) docs[col] = [...Store.data[col].values()].map(r => Sync.encode(col, r));
      const res = await this.post(base, "sync", { key, device: (navigator.userAgent.match(/\(([^;)]+);[^)]*\)/) || [])[1] || "telefon", docs, have: [...Store.blobIds] }, 120000);
      say(t("Kayıtlar birleştiriliyor…"));
      let got = 0;
      const aside = [];
      const applyOne = async (col, r) => {
        const loc = Store.data[col].get(r.id);
        if (loc && loc.m === r.m && !!loc.del === !!r.del) return;   // aynı sürüm: dokunma (kirli işareti korunur)
        const toSave = [];
        this._changed = Sync.apply(col, r, toSave) || this._changed;
        const now = Store.data[col].get(r.id);
        const took = now && now.m === r.m && !!now.del === !!r.del && (!loc || loc.m !== r.m || !!loc.del !== !!r.del);
        if (took) {
          got++;
          now.dirty = 1;   // internet gelince buluta da gönderilsin
          if (col === "docs" && !now.del) now.bu = Store.blobIds.has(now.id) ? 0 : 1;
        }
        if (toSave.length) await Store.flush(col, toSave);
      };
      this._changed = false;
      for (const col of COLS) {
        for (const fields of (res.docs && res.docs[col]) || []) {
          const r = Sync.decode(col, { fields, name: "x/" + ((fields.id && fields.id.stringValue) || "") });
          if (!r.id) continue;
          if (!Sync.parentOk(col, r)) { aside.push([col, r]); continue; }
          await applyOne(col, r);
        }
      }
      for (const [col, r] of aside) if (Sync.parentOk(col, r)) await applyOne(col, r);
      // bilgisayarın istediği belgeler → gönder
      let files = 0;
      for (const id of res.need || []) {
        const blob = await Store.getBlob(id);
        if (!blob) continue;
        say(tf("Belge gönderiliyor: {}", ++files));
        await this.post(base, "upload", { key, id, data: await blobToBase64(blob) }, 180000);
      }
      // telefonda olmayan belgeler → al
      for (const d of Store.live("docs")) {
        if (Store.blobIds.has(d.id) || !Store.tx(d.tx)) continue;
        say(tf("Belge alınıyor: {}", ++files));
        try {
          const b = await this.post(base, "blob", { key, id: d.id }, 180000);
          if (!b.data) continue;
          await Store.putBlob(d.id, new Blob([base64ToBytes(b.data)], { type: d.mime || MIME_BY_EXT[d.ext] || "" }));
          const cur = Store.data.docs.get(d.id);
          if (cur && !cur.del) { cur.bu = 0; cur.dirty = 1; Store.persist("docs", cur); }
          this._changed = true;
        } catch (e) { if (e.message === "KEY") throw e; }
      }
      const sent = Object.values(docs).reduce((n, a) => n + a.length, 0);
      this.setCfg({ host: String(host).trim(), code: String(code || "").trim(), last: Date.now(), name: res.name || "", lastGot: got });
      if ((got || this._changed) && typeof App !== "undefined") App.onRemoteChange();
      if (Sync.signedIn()) Sync.runSoon(1500);   // internet varsa Wi‑Fi'dan gelenler buluta da gitsin
      return { got, sent, files, name: res.name || "" };
    } finally { this.busy = false; }
  },
  errText(e) {
    const k = String((e && e.message) || e);
    if (k === "KEY") return t("Kod yanlış. Bilgisayardaki ☁ Eşitleme penceresinde yazan 6 haneli kodu girin.");
    if (k === "NET") return t("Bilgisayara ulaşılamadı. İkisi aynı Wi‑Fi'da mı, bilgisayarda Bereket Defter açık mı, adres doğru mu?");
    if (k === "ADDR") return t("Bilgisayarın adresini yazın (ör. 192.168.1.5).");
    if (k === "BUSY") return t("Eşitleniyor…");
    return tf("Wi‑Fi eşitleme hatası: {}", k);
  },
};
