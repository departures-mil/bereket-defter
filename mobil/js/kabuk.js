/* Bereket Defter (telefon) — ortak çekirdek kabuğu (cekirdek/fc-core.js). ui.js'ten SONRA yüklenir; App.init'ten önce FC.init çalışır.
   Burada: sağ üst sıra (Duyurular · Eşitle · Wi‑Fi · Güncelle · Tema · Dil | Tam ekran · Kapat), "klasik" renk şeması (1.20'ye kadarki
   yeşil görünüm), dil eşlemesi (LANG ↔ FC.i18n), ayarlar (Görünüm · Eşitleme · Arşiv · Yedek · Asistan · Kullanım · Hata raporu ·
   Hakkında · Admin ile iletişim EN SON), ilk açılış rehberi (kendi Firebase'iniz), "neler yeni", çökme raporu, Kullanım Limitleri
   (Firestore REST çağrıları FC.usage.wrapFetch ile sayılır) ve Android güncellemesi (yerel FcGuncelle: GitHub Releases latest.json →
   android kanalı; kurulu APK + FCD1 yama → yeni APK, SHA-256; yama olmazsa tam APK). */
(function () {
  'use strict';
  var APP = 'bereket-defter', REPO = 'bereket-defter';
  var AB = window.AndroidBridge || null;
  var ui = FC.ui;
  var T = function (k, v) { return FC.t(k, v); };

  FC.i18n.add({
    tr: {
      'bd.ayarlar': 'Ayarlar', 'bd.sync': 'Eşitleme (telefon ⇄ bilgisayar)',
      'bd.sync.desc': 'Kayıtlar kendi Firebase hesabınızla telefon ve bilgisayarlar arasında eşitlenir; aynı ağdaysanız Wi‑Fi ile internetsiz de eşitlenir. Hiçbir kayıt silinmez ya da körü körüne üzerine yazılmaz.',
      'bd.sync.open': 'Eşitleme ayarları', 'bd.yedek': 'Yedek', 'bd.yedek.desc': 'Kayıtların ve belgelerin tam yedeğini alın ya da yedekten geri yükleyin.',
      'bd.yedek.al': 'Yedek al', 'bd.yedek.yukle': 'Yedekten geri yükle',
      'bd.arsiv': 'Arşiv ve silinenler', 'bd.arsiv.desc': 'Başka cihazda silinen kayıtlar bu cihazda silinmez, burada arşivlenir. Kendi sildikleriniz de burada durur; istediğinizi geri alabilirsiniz.',
      'bd.arsiv.bos': 'Arşivde kayıt yok.', 'bd.arsiv.geri': 'Geri al', 'bd.arsiv.geriAlindi': 'Geri alındı: {s}', 'bd.arsiv.olmadi': 'Geri alınamadı: bağlı olduğu kişi ya da kayıt yok. Önce onu geri alın.',
      'bd.arsiv.uzak': 'başka cihazda silindi', 'bd.arsiv.yerel': 'bu cihazda silindi', 'bd.arsiv.yedek': 'Çakışma yedeği: {n} kayıt', 'bd.arsiv.yedekKaydet': 'Yedekleri kaydet (JSON)', 'bd.arsiv.fazla': '… ve {n} kayıt daha',
      'bd.tur.persons': 'Kişi', 'bd.tur.tx': 'Kayıt', 'bd.tur.rem': 'Hatırlatıcı', 'bd.tur.docs': 'Belge', 'bd.tur.hist': 'Geçmiş',
      'bd.ob.fb': 'Firebase bilgileri kaydedildi. Eşitleme ekranında e-posta ve şifrenizle giriş yapın (ilk kez ise "Hesap oluştur").',
      'bd.izin': 'Kurulum için "Bilinmeyen uygulamaları yükle" iznini verin, sonra Güncelle\'ye yeniden basın.'
    },
    en: {
      'bd.ayarlar': 'Settings', 'bd.sync': 'Sync (phone ⇄ computer)',
      'bd.sync.desc': 'Records sync between phones and computers through your own Firebase account; on the same network they also sync over Wi‑Fi without internet. Nothing is deleted or blindly overwritten.',
      'bd.sync.open': 'Sync settings', 'bd.yedek': 'Backup', 'bd.yedek.desc': 'Take a full backup of records and documents, or restore from a backup.',
      'bd.yedek.al': 'Back up', 'bd.yedek.yukle': 'Restore from backup',
      'bd.arsiv': 'Archive and deleted', 'bd.arsiv.desc': 'Records deleted on another device are not deleted here; they are archived. Records you deleted yourself are kept here too, and you can restore any of them.',
      'bd.arsiv.bos': 'The archive is empty.', 'bd.arsiv.geri': 'Restore', 'bd.arsiv.geriAlindi': 'Restored: {s}', 'bd.arsiv.olmadi': 'Could not restore: the person or record it belongs to is missing. Restore that first.',
      'bd.arsiv.uzak': 'deleted on another device', 'bd.arsiv.yerel': 'deleted on this device', 'bd.arsiv.yedek': 'Conflict backup: {n} records', 'bd.arsiv.yedekKaydet': 'Save backups (JSON)', 'bd.arsiv.fazla': '… and {n} more',
      'bd.tur.persons': 'Person', 'bd.tur.tx': 'Record', 'bd.tur.rem': 'Reminder', 'bd.tur.docs': 'Document', 'bd.tur.hist': 'History',
      'bd.ob.fb': 'Firebase details saved. Sign in with your e-mail and password on the sync screen (first time: "Create account").',
      'bd.izin': 'Allow "Install unknown apps" for the installation, then press Update again.'
    },
    ar: {
      'bd.ayarlar': 'الإعدادات', 'bd.sync': 'المزامنة (الهاتف ⇄ الحاسوب)',
      'bd.sync.desc': 'تتم مزامنة السجلات بين الهواتف والحواسيب عبر حساب Firebase الخاص بك؛ وفي الشبكة نفسها تتم المزامنة عبر Wi‑Fi دون إنترنت أيضاً. لا يُحذف شيء ولا يُكتب فوق شيء دون تحقق.',
      'bd.sync.open': 'إعدادات المزامنة', 'bd.yedek': 'النسخ الاحتياطي', 'bd.yedek.desc': 'خذ نسخة احتياطية كاملة من السجلات والمستندات أو استعدها من نسخة احتياطية.',
      'bd.yedek.al': 'نسخ احتياطي', 'bd.yedek.yukle': 'الاستعادة من نسخة احتياطية',
      'bd.arsiv': 'الأرشيف والمحذوفات', 'bd.arsiv.desc': 'السجلات المحذوفة على جهاز آخر لا تُحذف هنا بل تُؤرشف. وتبقى هنا أيضاً السجلات التي حذفتها بنفسك، ويمكنك استعادة أيٍّ منها.',
      'bd.arsiv.bos': 'الأرشيف فارغ.', 'bd.arsiv.geri': 'استعادة', 'bd.arsiv.geriAlindi': 'تمت الاستعادة: {s}', 'bd.arsiv.olmadi': 'تعذّرت الاستعادة: الشخص أو السجل المرتبط غير موجود. استعده أولاً.',
      'bd.arsiv.uzak': 'حُذف على جهاز آخر', 'bd.arsiv.yerel': 'حُذف على هذا الجهاز', 'bd.arsiv.yedek': 'نسخة احتياطية للتعارضات: {n} سجل', 'bd.arsiv.yedekKaydet': 'حفظ النسخ الاحتياطية (JSON)', 'bd.arsiv.fazla': '… و{n} سجلات أخرى',
      'bd.tur.persons': 'شخص', 'bd.tur.tx': 'سجل', 'bd.tur.rem': 'تذكير', 'bd.tur.docs': 'مستند', 'bd.tur.hist': 'السجل',
      'bd.ob.fb': 'تم حفظ بيانات Firebase. سجّل الدخول ببريدك الإلكتروني وكلمة المرور في شاشة المزامنة (أول مرة: «إنشاء حساب»).',
      'bd.izin': 'اسمح بـ«تثبيت التطبيقات غير المعروفة» للتثبيت، ثم اضغط «تحديث» مرة أخرى.'
    }
  });

  /* ---------- "klasik": 1.20'ye kadarki görünüm (yeşil üst çubuk, açık kartlar, deniz yeşili arka plan) ---------- */
  var KL = {
    '--bg': '#0b6e74', '--bg-grid': '#0000', '--panel': '#fffffff7', '--panel-solid': '#ffffff', '--panel-hover': '#f4faf8',
    '--border': '#dfe7e4', '--border-strong': '#0f8f6a', '--border-w': '1px', '--text': '#111111', '--muted': '#5f6b68', '--label': '#06513f',
    '--nav-text': '#33504a', '--nav-title': '#6a837d', '--accent': '#0f8f6a', '--accent-2': '#0b6e74', '--on-accent': '#ffffff',
    '--primary-1': '#0f8f6a', '--primary-2': '#0f8f6a', '--active-1': '#0f8f6a29', '--active-2': '#0f8f6a12', '--active-line': '#0f8f6a66',
    '--accent-soft': '#e3f4ee', '--accent-line': '#0f8f6a59', '--focus': '#0f8f6a', '--focus-w': '2px', '--focus-ring': '#0f8f6a2e',
    '--danger': '#c0392b', '--danger-text': '#c0392b', '--danger-soft': '#fdecea', '--danger-line': '#c0392b59',
    '--ok': '#0f8f6a', '--ok-text': '#0f8f6a', '--ok-soft': '#e3f6ee', '--ok-line': '#0f8f6a59',
    '--warn': '#e0a200', '--warn-text': '#5a4300', '--warn-soft': '#fff3b0', '--warn-line': '#e0a20080',
    '--sidebar-bg': '#ffffff', '--topbar-bg': '#06513ff0', '--modal-bg': '#ffffff', '--modal-border': '#dfe7e4', '--backdrop': '#00140f80',
    '--toast-bg': '#222222', '--toast-text': '#ffffff', '--toast-line': '#222222', '--toast-err-bg': '#c0392b', '--toast-err-text': '#ffffff', '--toast-err-line': '#c0392b',
    '--badge-text': '#06513f', '--badge-bg': '#e3f4ee', '--badge-line': '#dfe7e4', '--on-badge': '#ffffff',
    '--bar-track': '#e6ecea', '--scroll-thumb': '#0f8f6a59', '--glow-1': '#0000', '--glow-2': '#0000'
  };
  var KD = Object.assign({}, KL, {
    '--bg': '#062b23', '--panel': '#0b3a30f2', '--panel-solid': '#0b3a30', '--panel-hover': '#0f4a3d', '--border': '#1c5a4b',
    '--border-strong': '#34c29a', '--text': '#eef7f4', '--muted': '#a7c4bc', '--label': '#cfeee4', '--accent': '#34c29a', '--accent-2': '#2aa6ad',
    '--on-accent': '#04241c', '--primary-1': '#34c29a', '--primary-2': '#34c29a', '--active-1': '#34c29a33', '--active-line': '#34c29a66',
    '--accent-soft': '#0f4a3d', '--danger': '#ff8a7a', '--danger-text': '#ff8a7a', '--danger-soft': '#4a1f1b', '--ok': '#5ee0b5', '--ok-text': '#5ee0b5',
    '--ok-soft': '#0f4a3d', '--warn': '#ffd24a', '--warn-text': '#ffd24a', '--warn-soft': '#4a3a0a', '--modal-bg': '#062b23', '--modal-border': '#1c5a4b',
    '--badge-text': '#eef7f4', '--badge-bg': '#0f4a3d', '--badge-line': '#1c5a4b', '--on-badge': '#04241c', '--bar-track': '#0f4a3d'
  });
  FC.look.registerScheme('klasik', { label: { tr: 'Klasik (eski görünüm)', en: 'Classic (previous look)', ar: 'الكلاسيكي (المظهر السابق)' }, light: KL, dark: KD });

  /* ---------- dil: uygulama (LANG, bereket_lang) ↔ çekirdek (fc.lang) ---------- */
  var eskiKullanici = (function () { try { return !!localStorage.getItem('bereket_lang') || !!localStorage.getItem('bereket_sched'); } catch (e) { return false; } })();
  if (FC.storage.get('lang', null) == null) FC.i18n.set(LANG);
  else if (FC.i18n.lang() !== LANG) { LANG = FC.i18n.lang(); try { localStorage.setItem('bereket_lang', LANG); } catch (e) { /* yok */ } }
  FC.i18n.onChange(function (l) {
    if (l === LANG && document.documentElement.lang === l) return;
    setLang(l);
    if (typeof App !== 'undefined' && App.sumEl) { Sheets.closeAll(); App.build(); Rem.scheduleAll(); }
  });

  /* ---------- Kullanım Limitleri: Firestore REST çağrıları (sync.js fetch) kendiliğinden sayılır ---------- */
  FC.usage.wrapFetch();

  /* ---------- Android güncellemesi: indirme + yama + kurulum yerelde (FcGuncelle; WebView'de GitHub indirmesi CORS'a takılır) ---------- */
  if (FC.host.kind === 'android' && AB && typeof AB.apkUpdate === 'function') {
    FC.host.update.run = function (plan, onEv) {
      return new Promise(function (resolve, reject) {
        window.__fcApk = function (ev) {
          if (!ev) return;
          if (ev.type === 'progress') onEv({ patch: !!ev.patch, done: ev.done, total: ev.total, finished: !!ev.finished });
          else if (ev.type === 'patchFailed') onEv({ patchFailed: true, error: ev.error });
          else if (ev.type === 'installing') onEv({ installing: true });
          else if (ev.type === 'done') resolve(ev.result || 'done');
          else if (ev.type === 'error') {
            if (ev.error === 'IZIN') ui.toast(T('bd.izin'), 'info', 9000);
            reject(Object.assign(new Error(ev.error || 'FAILED'), { code: ev.error || 'FAILED' }));
          }
        };
        try {
          AB.apkUpdate(JSON.stringify({ version: plan.version, full: plan.full, patch: plan.mode === 'patch' ? { url: plan.url, sha256: plan.sha256, size: plan.size } : null }));
        } catch (e) { reject(e); }
      });
    };
    FC.host.can.update = true;

    /* v1.22.1 düzeltmesi: WebView (appassets.androidplatform.net) GitHub'dan fetch edemez — github.com yönlendirmesi CORS başlığı
       vermez, 1.21–1.22'de "Güncelleme yapılamadı: Failed to fetch" buradan geliyordu. (1) latest.json yerel AB.httpGet ile okunur;
       (2) "Güncelle" çekirdeğin WebView indirmesi yerine yukarıdaki yerel FcGuncelle yolunu (FC.host.update.run) kullanır.
       Çekirdek kopyası değişmez: FC.updater yalnızca sarılır (durum + abonelik aynı biçimde). */
    if (typeof AB.httpGet === 'function') {
      var httpSeq = 0, httpWait = {};
      window.__fcHttp = function (id, r) { var f = httpWait[id]; if (f) { delete httpWait[id]; f(r || {}); } };
      var yerelGet = function (url) {
        return new Promise(function (resolve, reject) {
          var id = 'h' + (++httpSeq) + '_' + Date.now();
          var to = setTimeout(function () { delete httpWait[id]; reject(Object.assign(new Error('TIMEOUT'), { code: 'TIMEOUT' })); }, 45000);
          httpWait[id] = function (r) {
            clearTimeout(to);
            if (r.error) reject(Object.assign(new Error(r.error), { code: 'NETWORK' }));
            else if (r.status !== 200) reject(Object.assign(new Error('HTTP ' + r.status), { code: 'HTTP_' + r.status }));
            else resolve(r.body || '');
          };
          try { AB.httpGet(id, url); } catch (e) { clearTimeout(to); delete httpWait[id]; reject(e); }
        });
      };
      FC.host.net = { download: function (url) { return yerelGet(url).then(function (t) { return new TextEncoder().encode(t); }); } };
    }
    (function () {
      var U = FC.updater, son = U.state(), ust = null, aboneler = [], calisiyor = false;
      function durum() { var s = {}, k; for (k in son) s[k] = son[k]; if (ust) for (k in ust) s[k] = ust[k]; return s; }
      function yay() { var s = durum(); aboneler.slice().forEach(function (f) { try { f(s); } catch (e) { /* yok */ } }); }
      function ayarla(p) { ust = ust || {}; for (var k in p) ust[k] = p[k]; yay(); }
      U.subscribe(function (s) { son = s; if (ust && !calisiyor && ['checking', 'available', 'none'].indexOf(s.status) >= 0) ust = null; yay(); });
      var W = {};
      for (var k in U) W[k] = U[k];
      W.state = durum;
      W.subscribe = function (f) { aboneler.push(f); try { f(durum()); } catch (e) { /* yok */ } return function () { aboneler = aboneler.filter(function (x) { return x !== f; }); }; };
      W.errorText = function (c) { return c === 'IZIN' ? T('bd.izin') : U.errorText(c); };
      W.check = function (o) { if (!calisiyor) ust = null; return U.check(o); };
      W.run = async function () {
        if (calisiyor) return;
        var p = son.plan || (await U.check());
        if (!p) { if (son.error) yay(); return; }
        calisiyor = true;
        var tr = { patch: FC.progress.tracker(p.mode === 'patch' ? p.size : 0), full: FC.progress.tracker(p.full.size) };
        var bas = { done: 0, total: p.size, pct: 0, remaining: p.size, speed: 0 };
        ust = null; ayarla({ status: 'downloading', mode: p.mode, progress: bas, error: null, fallback: false, patchError: null });
        if (FC.storage) FC.storage.set('whatsnew.pending', { version: p.version, notes: p.notes });
        try {
          var r = await FC.host.update.run(p, function (ev) {
            if (ev.patchFailed) ayarla({ status: 'downloading', mode: 'full', fallback: true, patchError: ev.error || '', progress: { done: 0, total: p.full.size, pct: 0, remaining: p.full.size, speed: 0 } });
            else if (ev.installing) ayarla({ status: 'installing' });
            else if (ev.done != null) ayarla({ status: 'downloading', mode: ev.patch ? 'patch' : 'full', progress: tr[ev.patch ? 'patch' : 'full'].update(ev.done, ev.finished) });
          });
          ayarla({ status: 'done' });
          return r;
        } catch (e) {
          ayarla({ status: 'error', error: e.code || e.message || 'ERR' });
          throw e;
        } finally { calisiyor = false; }
      };
      FC.updater = W;
    })();
  }

  /* ---------- çekirdeği başlat ---------- */
  if (eskiKullanici) {   // 1.20'den gelen kullanıcı: rehber yerine "neler yeni"
    if (FC.storage.get('onboarding.done', null) == null) FC.storage.set('onboarding.done', true);
    if (FC.storage.get('whatsnew.seen', null) == null) FC.storage.set('whatsnew.seen', '1.20.0');
  }
  FC.init({ app: APP, repo: REPO, version: APP_VERSION, announcements: true, whatsnew: false, onboarding: false });
  var wn = FC.whatsnew.start({ version: APP_VERSION, notes: function (v) { return (window.BEREKET_NOTES || {})[v] || null; } });
  try {   // 1.20'nin gönderilemeyen admin mesajları ortak gelen kutusu kuyruğuna
    var q = JSON.parse(localStorage.getItem('adminIletisim.kuyruk') || '[]');
    if (q.length) { q.forEach(function (it) { FC.contact.send({ tur: 'oneri', mesaj: it.m, iletisim: it.e || '' }); }); localStorage.removeItem('adminIletisim.kuyruk'); }
  } catch (e) { /* yok */ }

  function OB() {
    var fb = null;
    return {
      firebase: true, ai: false, store: false,
      onFirebase: function (cfg) { fb = cfg; },
      onClose: function () {
        if (!fb || Sync.signedIn()) return;
        Sync.setCfg({ apiKey: fb.apiKey, projectId: fb.projectId });
        fb = null;
        ui.toast(T('bd.ob.fb'), 'info', 9000);
        setTimeout(function () { Forms.sync(); }, 300);
      }
    };
  }
  document.addEventListener('DOMContentLoaded', function () {
    if (!wn) setTimeout(function () { if (!Sheets.stack.length) FC.onboarding.maybeStart(OB()); }, 900);
  });

  /* ---------- üst çubuk ---------- */
  var tb = null;
  function esitleDurum() {
    if (!tb) return;
    var st = Sync.status(), n = 0;
    if (Sync.signedIn()) COLS.forEach(function (c) { Store.data[c].forEach(function (r) { if (r.dirty) n++; }); });
    var k = { run: 'syncing', err: 'error', off: 'off', ok: 'idle' }[st.kind] || 'off';
    if (k !== 'off' && navigator.onLine === false) k = 'offline';
    tb.setSync(k, n);
    if (Sync.signedIn() && Sync.cfg().projectId) FC.usage.setProject && FC.usage.setProject(Sync.cfg().projectId);
  }
  function ustCubuk(header) {
    var old = header.querySelector('.topbar-actions'); if (old) old.remove();
    tb = FC.topbar.mount(header, {
      before: [FC.announcements.button()],
      sync: { state: 'off', onClick: function () { App.syncNow(); } },
      lan: { onClick: function () { Forms.sync(); setTimeout(function () { var b = document.querySelector('.lan-box'); if (b) b.scrollIntoView({ block: 'center' }); }, 150); } }
    });
    tb.setLan(typeof Lan !== 'undefined' && Lan.busy ? 'busy' : (Lan.cfg().last ? 'on' : 'off'));
    esitleDurum();
  }
  window.addEventListener('online', esitleDurum);
  window.addEventListener('offline', esitleDurum);

  function guncelle() { var b = document.querySelector('.topbar .update-act'); if (b) b.click(); }

  /* ---------- ayarlar ---------- */
  function syncKart() {
    var c = ui.card({ key: 'bereket-sync', title: T('bd.sync'), icon: 'sync', desc: T('bd.sync.desc') });
    c.appendChild(ui.el('div.fc-row', null, [
      ui.el('button.btn.small.primary', { type: 'button', html: ui.icon('sync') + ui.esc(T('bd.sync.open')), onclick: function () { Forms.sync(); } })
    ]));
    return c;
  }
  function yedekKart() {
    var c = ui.card({ key: 'bereket-yedek', title: T('bd.yedek'), icon: 'download', desc: T('bd.yedek.desc') });
    c.appendChild(ui.el('div.fc-row', null, [
      ui.el('button.btn.small', { type: 'button', html: ui.icon('download') + ui.esc(T('bd.yedek.al')), onclick: function () { Backup.export(); } }),
      ui.el('button.btn.small', { type: 'button', html: ui.icon('sync') + ui.esc(T('bd.yedek.yukle')), onclick: function () { Backup.import(); } })
    ]));
    return c;
  }
  function etiket(col, r) {
    if (col === 'persons') return r.name || '—';
    if (col === 'tx') return Store.personName(r.person) + ' · ' + String(r.ts || '').slice(0, 16) + ' · ' + r.amount + ' ' + r.currency;
    if (col === 'rem') return Store.personName(r.person) + ' · ' + String(r.due || '').slice(0, 16) + (r.note ? ' · ' + r.note : '');
    if (col === 'docs') return r.name || r.id;
    return r.id;
  }
  function arsivKart(yenile) {
    var c = ui.card({ key: 'bereket-arsiv', title: T('bd.arsiv'), icon: 'box', desc: T('bd.arsiv.desc') });
    var a = Store.meta.arsiv || [];
    if (!a.length) c.appendChild(ui.el('p.card-desc', { text: T('bd.arsiv.bos') }));
    a.slice(0, 40).forEach(function (it, i) {
      var b = ui.el('button.btn.small', { type: 'button', html: ui.icon('sync') + ui.esc(T('bd.arsiv.geri')) });
      b.addEventListener('click', function () {
        if (Store.restore(i)) { ui.toast(T('bd.arsiv.geriAlindi', { s: etiket(it.col, it.row) }), 'ok'); App.refresh(); yenile(); }
        else ui.toast(T('bd.arsiv.olmadi'), 'error', 7000);
      });
      c.appendChild(ui.el('div.arsiv-row', null, [
        ui.el('div.grow', null, [ui.el('span', { text: T('bd.tur.' + it.col) + ' · ' + etiket(it.col, it.row), dir: 'auto' }),
          ui.el('small', { text: (it.kaynak === 'uzak' ? T('bd.arsiv.uzak') : T('bd.arsiv.yerel')) + ' · ' + new Date(it.at).toLocaleString(LANG === 'ar' ? 'ar-u-nu-latn' : LANG) })]), b]));
    });
    if (a.length > 40) c.appendChild(ui.el('p.card-desc', { text: T('bd.arsiv.fazla', { n: a.length - 40 }) }));
    var y = Store.meta.cakisma || [];
    if (y.length) {
      c.appendChild(ui.el('p.card-desc', { text: T('bd.arsiv.yedek', { n: y.length }), style: 'margin-top:10px' }));
      c.appendChild(ui.el('button.btn.small', { type: 'button', html: ui.icon('download') + ui.esc(T('bd.arsiv.yedekKaydet')), onclick: function () {
        saveBlobAs(new Blob([JSON.stringify(y, null, 1)], { type: 'application/json' }), 'application/json', 'bereket-cakisma-yedekleri-' + new Date().toISOString().slice(0, 10) + '.json');
      } }));
    }
    return c;
  }
  function ayarlar() {
    var holder = ui.el('div');
    var entry = Sheets.open({ title: T('bd.ayarlar'), cls: 'wide-sheet', body: holder });
    function ciz() {
      holder.innerHTML = '';
      var grid = FC.settings.build(holder, {
        cards: [syncKart(), window.Ekler ? Ekler.ayarKarti(ciz) : null, arsivKart(ciz), yedekKart()].filter(Boolean),
        usage: { firebase: true, ai: false, project: function () { return Sync.signedIn() ? Sync.cfg().projectId : ''; } },
        about: { version: APP_VERSION }, onboarding: OB()
      });
      return grid;
    }
    ciz();
    return entry;
  }

  window.Kabuk = { ustCubuk: ustCubuk, esitleDurum: esitleDurum, ayarlar: ayarlar, guncelle: guncelle };
})();
