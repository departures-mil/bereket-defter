// Telefon ekran görüntüleri: PLAYWRIGHT_CORE=… PLAYWRIGHT_BROWSERS_PATH=… node araclar/ekran_mobil.js <klasör>
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const pw = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const ROOT = path.join(__dirname, '..', 'mobil'), OUT = path.resolve(process.argv[2] || 'ekran');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2' };
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
    if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); return r.end(); }
    r.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0, '127.0.0.1');
  await new Promise(r => srv.once('listening', r));
  const url = 'http://127.0.0.1:' + srv.address().port + '/index.html';
  const b = await pw.chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  for (const [ad, lang, scheme, theme] of [['tr-falcon-dark', 'tr', 'falcon', 'dark'], ['ar-falcon-light', 'ar', 'falcon', 'light'], ['tr-klasik', 'tr', 'klasik', 'light']]) {
    const p = await b.newPage({ viewport: { width: 412, height: 915 }, deviceScaleFactor: 2 });
    await p.route(/github(usercontent)?\.com|googleapis|formsubmit/, r => r.fulfill({ status: 404, body: '' }));
    await p.addInitScript(`localStorage.setItem('fc.onboarding.done','true');localStorage.setItem('fc.whatsnew.seen','"9.9.9"');localStorage.setItem('fc.lang','"${lang}"');localStorage.setItem('fc.scheme','"${scheme}"');localStorage.setItem('fc.theme','"${theme}"');localStorage.setItem('bereket_lang','${lang}')`);
    await p.goto(url);
    await p.waitForFunction(() => typeof App !== 'undefined' && App.sumEl);
    await p.evaluate(() => {
      if (Store.persons('').length) return;
      const a = Store.addPerson({ name: 'Ahmet Yılmaz', phone: '+905551112233', ch_wa: true, ch_call: true });
      const m = Store.addPerson({ name: 'محمد الأحمد', phone: '+963944000000', ch_tg: true });
      Store.addTx({ person: a, ts: '2026-11-20 10:15:00', direction: 'VERDIM', currency: 'USD', amount: 250, description: 'Kira avansı' });
      Store.addTx({ person: a, ts: '2026-11-22 16:40:00', direction: 'ALDIM', currency: 'USD', amount: 100, description: 'Kısmi ödeme' });
      Store.addTx({ person: m, ts: '2026-11-21 12:00:00', direction: 'VERDIM', currency: 'SYP', amount: 1500000, description: 'Malzeme' });
      App.refresh();
    });
    await p.waitForTimeout(700);
    await p.screenshot({ path: path.join(OUT, 'telefon-' + ad + '-defter.png') });
    await p.evaluate(() => Forms.settings());
    await p.waitForTimeout(600);
    await p.screenshot({ path: path.join(OUT, 'telefon-' + ad + '-ayarlar.png') });
    await p.close();
    console.log(ad, 'ok');
  }
  await b.close(); srv.close();
})().catch(e => { console.error(e); process.exit(1); });
