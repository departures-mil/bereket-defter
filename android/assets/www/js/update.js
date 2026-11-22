/* Uygulama içi güncelleme: GitHub deposundaki "guncelleme/mobil.json" bildirgesinden yeni sürümü okur,
   paketi indirip AndroidBridge.installBundle ile kurar ve uygulamayı yeniden açar. Kayıtlara dokunmaz. */
'use strict';

// Güncellemeler GitHub'dan gelir (Firebase yalnızca canlı kayıt eşitlemesi içindir).
const GITHUB_RAW = "https://raw.githubusercontent.com/departures-mil/bereket-defter/main";
const UPDATE_CHANNEL = "mobil";
// Güncelleme ayarları (⚙ Ayarlar): Store.meta.updCfg. Yeni sürüm yalnızca uygulama açılışında denetlenir.
const UPD_DEFAULTS = { notify: true };

const UPDATE_ERRORS = {
  NETWORK: "İnternet bağlantısı yok veya sunucuya ulaşılamadı.",
  BAD_PACKAGE: "İndirilen güncelleme bozuk, tekrar deneyin.",
  WRITE: "Güncelleme kaydedilemedi. Telefonda yer açıp tekrar deneyin.",
  NO_BRIDGE: "Güncelleme yalnızca telefon uygulamasında yapılabilir.",
  NEED_APK: "Bu güncelleme için yeni APK gerekiyor ama henüz yayınlanmamış.",
};

function versionParts(v) {
  const out = String(v || "").trim().replace(/^v/i, "").split(".").map(p => parseInt(p.replace(/\D/g, ""), 10) || 0);
  while (out.length && out[out.length - 1] === 0) out.pop();
  return out;
}
function versionNewer(a, b) {
  const x = versionParts(a), y = versionParts(b);
  for (let i = 0; i < Math.max(x.length, y.length); i++) {
    const p = x[i] || 0, q = y[i] || 0;
    if (p !== q) return p > q;
  }
  return false;
}

/* ---- indirme bilgisi biçimleri (TR/AR: virgül, EN: nokta) ---- */
function fmtNum(x, dg) { const s = x.toFixed(dg); return LANG === "en" ? s : s.replace(".", ","); }
function fmtMB(b, ref) { const mb = b / 1048576; return fmtNum(mb, (ref || b) >= 10 * 1048576 ? 1 : 2); }
function fmtSpeed(bps) {
  return bps >= 1048576 ? tf("{} MB/sn", fmtNum(bps / 1048576, 1)) : tf("{} KB/sn", Math.max(1, Math.round(bps / 1024)));
}
function fmtEta(sec) {
  sec = Math.max(1, Math.round(sec));
  if (sec < 60) return tf("~{} sn", sec);
  const m = Math.floor(sec / 60), r = sec % 60;
  return r ? tf("~{} dk {} sn", m, r) : tf("~{} dk", m);
}

const Upd = {
  state: "idle",   // idle | checking | none | available | downloading | installed | apk | error
  info: null, err: "", prog: [0, 0], speed: 0, listeners: [], lastCheck: 0, busy: false,
  notified: new Set(), popupWanted: false,

  cfg() {
    const c = (typeof Store !== "undefined" && Store.meta && Store.meta.updCfg) || {};
    return { notify: c.notify !== false };
  },
  setCfg(c) { Store.setMeta("updCfg", { notify: !!(c && c.notify) }); },

  emit() { for (const f of this.listeners) { try { f(); } catch (e) { console.warn(e); } } },
  set(state, extra) { this.state = state; Object.assign(this, extra || {}); this.emit(); },
  nativeCode() { try { return bridgeHas("nativeCode") ? Number(bridge().nativeCode()) || 0 : 0; } catch (e) { return 0; } },
  needsApk(info) { return Number((info || {}).minNative || 0) > this.nativeCode(); },
  errText() {
    const k = String(this.err || "").split(":")[0];
    return UPDATE_ERRORS[k] ? t(UPDATE_ERRORS[k]) : tf("Güncelleme hatası: {}", this.err);
  },

  async getJson(path) {
    let res;
    try { res = await fetch(`${GITHUB_RAW}/${path}?t=${Date.now()}`, { cache: "no-store" }); } catch (e) { throw new Error("NETWORK"); }
    if (res.status === 404) return {};
    if (!res.ok) throw new Error("HTTP " + res.status);
    try { return await res.json(); } catch (e) { throw new Error("NETWORK"); }
  },

  /** quiet: arka plan denetimi; ekranda "denetleniyor" göstermez, hata olursa bulunan sürümü silmez. */
  async check(opt) {
    const quiet = !!(opt && opt.quiet);
    if (this.busy || ["downloading", "installed"].includes(this.state)) return this.state;
    this.busy = true;
    this.lastCheck = Date.now();
    if (!quiet) this.set("checking", { err: "" });
    try {
      const info = await this.getJson("guncelleme/" + UPDATE_CHANNEL + ".json");
      if (["downloading", "installed"].includes(this.state)) return this.state;
      if (info.surum && info.dosya && versionNewer(info.surum, APP_VERSION)) this.set("available", { info, err: "" });
      else this.set("none", { info, err: "" });
    } catch (e) {
      if (!(quiet && this.state === "available")) this.set("error", { err: e.message || String(e) });
    } finally {
      this.busy = false;
    }
    if (this.state === "available") this.maybeNotify();
    return this.state;
  },

  /** her yeni sürüm için bir kez: uygulama açıksa soru penceresi, arka plandaysa Android bildirimi */
  maybeNotify() {
    const ver = String(this.info.surum);
    if (this.notified.has(ver)) return;
    this.notified.add(ver);
    if (!this.cfg().notify) return;
    if (Sheets.stack.some(s => s.isUpdate)) return;   // ⬆ Güncelleme penceresi zaten açık
    const b = bridge();
    if (document.hidden && b && typeof b.scheduleReminder === "function") {
      try {
        b.scheduleReminder("upd_" + ver, Date.now() + 500, t("⬆ Güncelleme"),
          tf("Yeni sürüm hazır: {}", "v" + ver) + " " + t("Güncellemek için dokunun."));
      } catch (e) { console.warn(e); }
    }
    try { if (navigator.vibrate) navigator.vibrate([120, 60, 120]); } catch (e) { /* yok */ }
    this.popupWanted = true;
    this.popupSoon();
  },
  popupSoon() {
    if (!this.popupWanted) return;
    if (document.hidden || Sheets.stack.length) { setTimeout(() => this.popupSoon(), 1500); return; }
    this.popupWanted = false;
    if (this.state !== "available") return;
    const info = this.info || {};
    const notes = String(info.notlar || "").trim();
    Dlg.confirm(tf("Yeni sürüm hazır: {}", "v" + info.surum) + "\n" + tf("Kullandığınız sürüm: {}", "v" + APP_VERSION) +
      (notes ? "\n\n" + notes : "") + "\n\n" +
      t("Güncelleme sadece uygulamayı yeniler; kayıtlarınız, kişileriniz ve belgeleriniz olduğu gibi kalır."),
      t("⬆ Güncelleme"), { yes: t("⬆ Şimdi güncelle"), no: t("Sonra") }).then(ok => {
      if (ok) Forms.update({ autoInstall: true });
    });
  },

  /** Dosyayı GitHub'dan akış hâlinde indirir, base64 döner; prog = [indirilen bayt, toplam bayt], speed = bayt/sn. */
  async fetchB64(file, size, sha) {
    let done = 0, last = 0, total = Number(size || 0);
    const t0 = Date.now();
    const tick = force => {
      const now = Date.now();
      if (!force && now - last < 200) return;
      last = now;
      this.speed = done / Math.max((now - t0) / 1000, 0.05);
      this.prog = [done, Math.max(total, done)];
      this.emit();
    };
    this.prog = [0, total]; this.speed = 0; this.emit();
    let res;
    try { res = await fetch(`${GITHUB_RAW}/guncelleme/${file}?t=${Date.now()}`, { cache: "no-store" }); }
    catch (e) { throw new Error("NETWORK"); }
    if (!res.ok) throw new Error("HTTP " + res.status);
    if (!total) total = Number(res.headers.get("Content-Length") || 0);
    const chunks = [];
    if (res.body && res.body.getReader) {
      const rd = res.body.getReader();
      for (;;) {
        const { value, done: end } = await rd.read();
        if (end) break;
        chunks.push(value); done += value.length; tick(false);
      }
    } else {
      const ab = new Uint8Array(await res.arrayBuffer());
      chunks.push(ab); done = ab.length;
    }
    tick(true);
    const bytes = new Uint8Array(done);
    let o = 0;
    for (const c of chunks) { bytes.set(c, o); o += c.length; }
    if (sha && crypto && crypto.subtle) {
      const h = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", bytes)))
        .map(x => x.toString(16).padStart(2, "0")).join("");
      if (h !== String(sha).toLowerCase()) throw new Error("BAD_PACKAGE");
    }
    let bin = "";
    for (let i = 0; i < bytes.length; i += 32768) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 32768));
    this.prog = [done, done];
    return btoa(bin);
  },
  /** İndirme bilgisi parça parça: { pct, size: "5,9 / 10,3 MB", left: "4,4 MB", speed: "1,1 MB/sn", eta: "~5 sn" } */
  progInfo() {
    const [d, tot] = this.prog;
    if (!tot) return null;
    const left = Math.max(tot - d, 0);
    return {
      pct: Math.min(100, Math.floor(d * 100 / tot)),
      size: tf("{} / {} MB", fmtMB(d, tot), fmtMB(tot, tot)),
      left: tf("{} MB", fmtMB(left, tot)),
      speed: this.speed > 0 ? fmtSpeed(this.speed) : "",
      eta: this.speed > 0 && left > 0 && d > 0 ? fmtEta(left / this.speed) : "",
    };
  },
  pct() { const [d, tot] = this.prog; return tot ? Math.min(100, Math.floor(d * 100 / tot)) : 0; },

  async install() {
    const info = this.info;
    if (!info || this.state === "downloading") return;
    this.set("downloading", { err: "", prog: [0, 0] });
    try {
      if (!bridgeHas("installBundle")) throw new Error("NO_BRIDGE");
      if (this.needsApk(info)) {
        // yerel (Java) kısım da değişmiş: APK indirilir, Android kurulum ekranı açılır
        if (!info.apkDosya || !bridgeHas("installApk")) throw new Error("NEED_APK");
        const b64 = await this.fetchB64(info.apkDosya, info.apkBoyut, info.apkSha256);
        const r = String(bridge().installApk(b64, info.apkSha256));
        if (r === "IZIN") { this.set("apk", { err: "IZIN" }); return; }
        if (r !== "ok") throw new Error(r);
        this.set("apk", { err: "" });
        return;
      }
      const b64 = await this.fetchB64(info.dosya, info.boyut, info.sha256);
      const r = String(bridge().installBundle(b64, String(info.surum), String(info.sha256 || "")));
      if (r !== "ok") throw new Error(r);
      this.set("installed");
      setTimeout(() => bridge().restartApp(), 1200);
    } catch (e) {
      this.set("error", { err: e.message || String(e) });
    }
  },

  init() {
    try { if (bridgeHas("bundleOk")) bridge().bundleOk(); } catch (e) { /* yok */ }
    setTimeout(() => this.check({ quiet: true }), 2500);   // yalnızca açılışta denetlenir
    document.addEventListener("visibilitychange", () => { if (!document.hidden) this.popupSoon(); });
  },
};
