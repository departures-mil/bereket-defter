// Telefon arayüzü duman testi (gerçek Chromium): ortak çekirdek üst çubuğu, ayarlar sırası, kalıcı silme yok kuralı.
// Çalıştır: node test/mobil.test.js   (playwright-core: PLAYWRIGHT_CORE ya da npm; tarayıcı: CHROME ya da PLAYWRIGHT_BROWSERS_PATH)
'use strict';
const http = require('http'), fs = require('fs'), path = require('path'), assert = require('assert');
const pw = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const ROOT = path.join(__dirname, '..', 'mobil');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json' };

(async () => {
  const srv = http.createServer((q, r) => {
    const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
    if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); return r.end(); }
    r.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
  }).listen(0, '127.0.0.1');
  await new Promise(r => srv.once('listening', r));
  const url = 'http://127.0.0.1:' + srv.address().port + '/index.html';
  const b = await pw.chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const errs = [];
  async function sayfa(init) {
    const p = await b.newPage({ viewport: { width: 412, height: 900 } });
    p.on('pageerror', e => errs.push(e.message));
    await p.route(/github(usercontent)?\.com|googleapis|formsubmit/, r => r.fulfill({ status: 404, body: '' }));
    if (init) await p.addInitScript(init);
    await p.goto(url);
    await p.waitForFunction(() => typeof App !== 'undefined' && App.sumEl && document.querySelector('.topbar .topbar-actions'));
    return p;
  }
  let ok = 0;
  const t = async (ad, f) => { await f(); ok++; console.log('✓', ad); };

  const p = await sayfa("localStorage.setItem('fc.onboarding.done','true')");
  await t('üst çubuk: Eşitle · Wi‑Fi · Güncelle · tema · dil', async () => {
    const k = await p.evaluate(() => ['.sync-act', '.lan-act', '.update-act', '.theme-btn', '.lang-switch'].map(s => !!document.querySelector('.topbar ' + s)));
    assert.deepStrictEqual(k, [true, true, true, true, true]);
  });
  await t('sürüm ve şemalar (falcon varsayılan, klasik kayıtlı)', async () => {
    const r = await p.evaluate(() => ({ v: APP_VERSION, s: document.documentElement.getAttribute('data-scheme'), k: FC.look.schemes().indexOf('klasik') >= 0 }));
    assert.ok(/^\d+\.\d+\.\d+$/.test(r.v)); assert.strictEqual(r.s, 'falcon'); assert.ok(r.k);
  });
  await t('ayarlar: Görünüm ilk, Admin ile iletişim EN SON', async () => {
    const r = await p.evaluate(() => { Forms.settings(); const g = document.querySelector('.sheet .settings-grid'); const c = [...g.children];
      return { first: c[0].getAttribute('data-fc-card'), last: c[c.length - 1].getAttribute('data-fc-card') || c[c.length - 1].className, n: c.length }; });
    assert.strictEqual(r.first, 'look'); assert.ok(/contact/.test(r.last), r.last); assert.ok(r.n >= 7);
  });
  await t('kendi silme → arşiv → geri al (aynı kimlik)', async () => {
    const r = await p.evaluate(async () => {
      Sheets.closeAll();
      const pp = Store.addPerson({ name: 'Deneme Kişi', phone: '1' });
      const id = pp.id || pp;
      Store.deletePerson(id);
      const a1 = (Store.meta.arsiv || []).length, gone = !Store.person(id);
      const i = (Store.meta.arsiv || []).findIndex(x => x.col === 'persons' && x.row.id === id);
      const back = Store.restore(i);
      return { a1, gone, back, again: !!Store.person(id) };
    });
    assert.ok(r.a1 >= 1 && r.gone && r.back && r.again, JSON.stringify(r));
  });
  await t('uzak silme yerelde arşivlenir; çakışmada eski hal yedeklenir', async () => {
    const r = await p.evaluate(() => {
      const pp = Store.addPerson({ name: 'Uzak', phone: '2' }); const id = pp.id || pp;
      const loc = Store.data.persons.get(id);
      const ts = [];
      Sync.apply('persons', Object.assign({}, loc, { name: 'Uzak (yeni)', m: loc.m + 10 }), ts);   // yerel kirli + uzak daha yeni
      const c = (Store.meta.cakisma || []).some(x => x.row.id === id && x.row.name === 'Uzak');
      Sync.apply('persons', { id, m: loc.m + 20, del: true }, ts);
      const a = (Store.meta.arsiv || []).some(x => x.kaynak === 'uzak' && x.row.id === id && x.row.name === 'Uzak (yeni)');
      return { c, a };
    });
    assert.ok(r.c && r.a, JSON.stringify(r));
  });
  await t('v1.22: hızlı kayıt ayrıştırıcı (tr/en/ar)', async () => {
    const r = await p.evaluate(() => {
      const K = [{ id: 'a', name: 'Ahmet Yılmaz' }, { id: 'b', name: 'Ali' }, { id: 'c', name: 'محمد' }];
      const f = s => { const x = Ekler._.hizliAyristir(s, K); return [x.ad, x.direction, x.currency, x.amount]; };
      return [f("Ahmet'e 500 TL verdim"), f("Ali'den 1.500 dolar aldım kira için"), f("Ali bana 300 lira ödedi"), f("received 200$ from Ali"),
        f("gave John 20 usd for lunch"), f("أعطيت محمد 100 دولار"), f("استلمت من خالد 5000 ليرة سورية"), f("Ahmet 2 bin TL verdi"),
        Ekler._.hizliAyristir("Ali'den 1.500 dolar aldım kira için", K).description];
    });
    assert.deepStrictEqual(r, [["Ahmet Yılmaz", "VERDIM", "TRY", 500], ["Ali", "ALDIM", "USD", 1500], ["Ali", "ALDIM", "TRY", 300],
      ["Ali", "ALDIM", "USD", 200], ["John", "VERDIM", "USD", 20], ["محمد", "VERDIM", "USD", 100], ["خالد", "ALDIM", "SYP", 5000],
      ["Ahmet Yılmaz", "ALDIM", "TRY", 2000], "kira"]);
  });
  await t('v1.22: mesaj, senet, taksit, PIN, CSV', async () => {
    const r = await p.evaluate(() => {
      const E = Ekler._;
      const m = E.mesajMetni('bakiye', 'tr', 'Ali', { USD: 150, TRY: -50 }, 'Ahmet', '25.11.2026');
      const k = E.pinKaydi('4321');
      const pid = Store.addPerson({ name: 'CSV Ali' });
      Store.addTx({ person: pid, ts: '2026-11-01 10:00', direction: 'VERDIM', currency: 'USD', amount: 1234.5, description: 'a;b' });
      const csv = E.csvDisa();
      const coz = E.csvCozumle(csv);
      const coz2 = E.csvCozumle('Date,Person,Type,Currency,Amount\n2026-11-03,Yeni Can,Received,TRY,"1,500.00"\nbozuk,x,gave,USD,1');
      return { m: m.includes('Bana olan borcunuz: 150,00 $') && m.includes('Size olan borcum: 50,00 ₺') && m.endsWith('Ahmet'),
        senet: E.senetHtml({ borclu: 'A<b>', tutar: 10, cur: 'USD' }, 'ar').includes('dir="rtl"') && E.senetHtml({ borclu: 'A<b>' }, 'tr').includes('A&lt;b&gt;'),
        taksit: E.taksitler(1000, 3, new Date(2026, 0, 31, 10, 0), 'ay'),
        pin: E.pinDogru(k, '4321') && !E.pinDogru(k, '1111'), sha: E.sha256('abc'),
        csv: [coz.satirlar.length, coz.satirlar[0].yinelenen, coz.satirlar[0].amount],
        csv2: [coz2.satirlar.length, coz2.satirlar[0].amount, coz2.satirlar[0].direction, [...coz2.yeniKisiler], coz2.hatalar] };
    });
    assert.ok(r.m && r.senet && r.pin, JSON.stringify(r));
    assert.deepStrictEqual(r.taksit, [['2026-01-31 10:00', 333.33], ['2026-02-28 10:00', 333.33], ['2026-03-31 10:00', 333.34]]);
    assert.strictEqual(r.sha, 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');
    assert.deepStrictEqual(r.csv, [1, true, 1234.5]);
    assert.deepStrictEqual(r.csv2, [1, 1500, 'ALDIM', ['Yeni Can'], [[3, 'tarih']]]);
  });
  await t('v1.22: yedekten eksikleri getir (silmez, üzerine yazmaz) + geri al çubuğu + etiket', async () => {
    const r = await p.evaluate(async () => {
      Sheets.closeAll();
      const pid = Store.addPerson({ name: 'Yedek Kişi', tags: 'aile, iş' });
      const tid = Store.addTx({ person: pid, ts: '2026-11-02 10:00', direction: 'VERDIM', currency: 'USD', amount: 50, description: 'eski' });
      const y = Ekler._.anlik();
      Store.deleteTx(tid);
      Store.updateContact(pid, { name: 'Yedek Kişi (yeni)' });
      await new Promise(r => setTimeout(r, 120));
      const bar = !!document.querySelector('#geri-al');
      const once = await Ekler._.eksikler(y, false);
      const s = await Ekler._.eksikler(y, true);
      App.refresh();
      return { bar, once: once.tx[1], s: s.tx[1], kisi: Store.person(pid).name, geri: !!Store.tx(tid), dirty: Store.data.tx.get(tid).dirty,
        etiket: !!document.querySelector('#etiket-bar .chip'), ara: Store.persons('aile').some(p => p.id === pid) };
    });
    assert.deepStrictEqual(r, { bar: true, once: 1, s: 1, kisi: 'Yedek Kişi (yeni)', geri: true, dirty: 1, etiket: true, ara: true });
  });
  await t('v1.22: raporlar, mesaj, taksit, senet, hızlı kayıt pencereleri açılır; tutar gizleme', async () => {
    const r = await p.evaluate(() => {
      const out = [];
      const pid = Store.persons()[0].id;
      for (const f of [() => Ekler.raporlar(), () => Ekler.mesaj(pid), () => Ekler.taksit(pid), () => Ekler.senet(pid), () => Ekler.hizliKayit("Ali'den 5 dolar aldım"), () => Ekler.yedekler()]) {
        f(); out.push(document.querySelectorAll('.sheet').length); Sheets.closeAll();
      }
      Ekler.gizleDegistir(true);
      const gizli = document.querySelector('.sum-tiles').textContent.includes('•••••');
      const st = Statement.build({ pid: null, start: '1970-01-01 00:00', end: '2999-12-31 23:59', cur: '', hourly: false }).body.includes('•••••');
      Ekler.gizleDegistir(false);
      return { out, gizli, st, hizli: !!document.querySelector('#hizli-inp'), goz: !!document.querySelector('.top-btn.goz') };
    });
    assert.deepStrictEqual(r, { out: [1, 1, 1, 1, 1, 1], gizli: true, st: false, hizli: true, goz: true });
  });
  await t('v1.22: PIN kilidi açılışta ekranı kapatır', async () => {
    const r = await p.evaluate(() => {
      Ekler.A.pin = Ekler._.pinKaydi('2468'); Ekler.kilitle();
      const kilit = !!document.querySelector('.kilit');
      const inp = document.querySelector('.kilit-pin'); inp.value = '1111'; document.querySelector('.kilit .btn.primary').click();
      const yanlis = !!document.querySelector('.kilit');
      inp.value = '2468'; document.querySelector('.kilit .btn.primary').click();
      const acik = !document.querySelector('.kilit');
      Ekler.A.pin = null;
      return { kilit, yanlis, acik };
    });
    assert.deepStrictEqual(r, { kilit: true, yanlis: true, acik: true });
  });
  await p.close();

  const p2 = await sayfa("localStorage.setItem('fc.onboarding.done','true');localStorage.setItem('fc.lang','\"ar\"');localStorage.setItem('fc.scheme','\"klasik\"');localStorage.setItem('fc.theme','\"light\"')");
  await t('Arapça RTL + klasik şema', async () => {
    const r = await p2.evaluate(() => ({ dir: document.documentElement.dir, lang: LANG, s: document.documentElement.getAttribute('data-scheme') }));
    assert.deepStrictEqual(r, { dir: 'rtl', lang: 'ar', s: 'klasik' });
  });
  await p2.close();

  // v1.22.1: Android'de güncelleme WebView fetch'i kullanmaz (CORS → "Failed to fetch"); latest.json yerel httpGet, indirme yerel apkUpdate
  const SAHTE = `localStorage.setItem('fc.onboarding.done','true');
    window.__istekler = []; window.__plan = null;
    window.AndroidBridge = {
      appVersion: () => '1.0.0',
      httpGet: (id, url) => { __istekler.push(url); setTimeout(() => window.__fcHttp(id, { status: 200, body: JSON.stringify({ schema: 1, app: 'bereket-defter', version: '9.9.9',
        assets: { android: { file: 'BereketDefter-9.9.9.apk', size: 1000, sha256: 'a'.repeat(64), patches: {} } } }) }), 5); },
      apkUpdate: (j) => { __plan = JSON.parse(j); const e = (o) => setTimeout(() => window.__fcApk(o), 5);
        e({ type: 'progress', patch: false, done: 500, total: 1000 }); setTimeout(() => { window.__fcApk({ type: 'progress', patch: false, done: 1000, total: 1000, finished: true });
        window.__fcApk({ type: 'installing' }); window.__fcApk({ type: 'done', result: 'done' }); }, 30); }
    };`;
  const p3 = await sayfa(SAHTE);
  await t('Android güncellemesi: yerel denetim + yerel indirme (CORS yok)', async () => {
    const r = await p3.evaluate(async () => {
      const durumlar = []; FC.updater.subscribe(s => durumlar.push(s.status));
      const plan = await FC.updater.check();
      await FC.updater.run();
      return { v: plan && plan.version, url: __istekler[0], tam: __plan && __plan.full.url, son: FC.updater.state().status, indi: durumlar.indexOf('downloading') >= 0,
        izin: FC.updater.errorText('IZIN') === FC.t('bd.izin') };
    });
    assert.strictEqual(r.v, '9.9.9'); assert.ok(/releases\/latest\/download\/latest\.json$/.test(r.url), r.url);
    assert.ok(/releases\/download\/v9\.9\.9\/BereketDefter-9\.9\.9\.apk$/.test(r.tam), r.tam);
    assert.strictEqual(r.son, 'done'); assert.ok(r.indi); assert.ok(r.izin);
  });
  await p3.close();
  await b.close(); srv.close();
  assert.deepStrictEqual(errs, [], 'sayfa hataları: ' + errs.join(' | '));
  console.log(ok + ' telefon testi geçti');
})().catch(e => { console.error(e); process.exit(1); });
