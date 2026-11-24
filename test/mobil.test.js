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
  await p.close();

  const p2 = await sayfa("localStorage.setItem('fc.onboarding.done','true');localStorage.setItem('fc.lang','\"ar\"');localStorage.setItem('fc.scheme','\"klasik\"');localStorage.setItem('fc.theme','\"light\"')");
  await t('Arapça RTL + klasik şema', async () => {
    const r = await p2.evaluate(() => ({ dir: document.documentElement.dir, lang: LANG, s: document.documentElement.getAttribute('data-scheme') }));
    assert.deepStrictEqual(r, { dir: 'rtl', lang: 'ar', s: 'klasik' });
  });
  await p2.close();
  await b.close(); srv.close();
  assert.deepStrictEqual(errs, [], 'sayfa hataları: ' + errs.join(' | '));
  console.log(ok + ' telefon testi geçti');
})().catch(e => { console.error(e); process.exit(1); });
