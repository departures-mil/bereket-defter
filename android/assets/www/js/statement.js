/* Hesap dökümü (günlük / saatlik) — masaüstü StatementDialog.build_html ile aynı içerik. */
'use strict';

const STMT_BASE_CSS = `
.st{font-family:'Segoe UI',Roboto,Arial,sans-serif;font-size:11pt;color:#223;background:#fff;line-height:1.35}
.st h2{color:#06513f;margin:0;font-size:16pt}
.st h3{color:#0b6e74;margin:14px 0 4px;font-size:12.5pt}
.st h3.sum{color:#06513f}
.st .st-head{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 16px}
.st .st-name{font-size:14pt;font-weight:700;margin-top:2px}
.st .st-meta{color:#667;text-align:end}
.st hr{border:0;border-top:1px solid #cfd8d5;margin:10px 0}
.st table{width:100%;border-collapse:collapse;margin:0}
.st th{background:#06513f;color:#fff;padding:5px;border:1px solid #06513f;font-weight:600;text-align:start}
.st,.st th{overflow-wrap:normal;word-break:normal}
.st td{border:1px solid #cfd8d5;padding:5px;vertical-align:top;overflow-wrap:break-word;word-break:normal}
.st td.t{white-space:nowrap}
.st td.n{text-align:right;white-space:nowrap}
.st td.c{text-align:center}
.st .ver{color:#c0392b}.st .al{color:#0f8f6a}.st .pos{color:#0f8f6a}.st .neg{color:#c0392b}
.st .subt{color:#556;margin:3px 0 0;font-style:italic}
.st .muted{color:#667}
.st .foot{color:#667;font-size:9pt}
.st bdi{unicode-bidi:isolate}
@media print{.st{font-size:10pt}.st tr{page-break-inside:avoid}}
`;
/** dar ekranda tabloları kart düzenine çevirir (yatay kaydırma olmasın) */
function stmtStackCss(prefix) {
  const p = prefix;
  return `
${p} table, ${p} tbody, ${p} tr, ${p} td{display:block;width:auto}
${p} thead, ${p} tr.hd{display:none}
${p} tr{border:1px solid #cfd8d5;border-radius:8px;margin:6px 0;padding:4px 8px;background:#fff}
${p} td{border:0;padding:2px 0;display:flex;justify-content:space-between;gap:10px;text-align:start}
${p} td.n, ${p} td.c{text-align:end;white-space:normal}
${p} td::before{content:attr(data-l);color:#667;font-weight:600;flex:0 0 auto}
${p} td:empty{display:none}
${p} td.desc{display:block}
${p} td.desc::before{display:block}
`;
}

const Statement = {
  bal(b, c, short) {
    if (Math.abs(b) < 0.005) return `<bdi dir="ltr">0 ${CURRENCY_SYMBOLS[c]}</bdi>`;
    const cls = b > 0 ? "pos" : "neg";
    const label = short ? "" : (b > 0 ? t("Alacak") : t("Verecek")) + " ";
    return `<span class="${cls}">${esc(label)}<bdi dir="ltr">${esc(money(short ? b : Math.abs(b), c))}</bdi></span>`;
  },
  /** o: {pid, start "YYYY-MM-DD HH:MM", end "YYYY-MM-DD HH:MM", cur, hourly} -> {body, full, title, fileBase} */
  build(o) {
    const person = o.pid ? Store.person(o.pid) : null;
    const curs = o.cur ? [o.cur] : CURRENCIES;
    const rows = Store.transactions({ pid: o.pid, start: o.start, end: o.end + ":59", currency: o.cur });
    const openBal = Store.balances(o.pid, o.start);
    const opening = {}, running = {};
    for (const c of CURRENCIES) { opening[c] = openBal[c][2]; running[c] = openBal[c][2]; }
    const name = person ? person.name : t("Tüm kişiler");
    const H = [];
    const d1 = tsDisplay(o.start), d2 = tsDisplay(o.end);
    const nowD = tsDisplay(nowStr());
    H.push(`<div class="st-head"><div><h2>${esc(t(APP_TITLE))}</h2><div class="st-name">${esc(tf("Hesap Dökümü — {}", name))}</div>` +
      `<div><bdi dir="ltr">${d1} – ${d2}</bdi></div></div><div class="st-meta">${esc(t("Oluşturulma"))}: <bdi dir="ltr">${nowD}</bdi>` +
      (person && person.phone ? `<br><bdi dir="ltr">${esc(person.phone)}</bdi>` : "") + `</div></div><hr>`);
    H.push(`<p><b>${esc(t("Devreden bakiye"))}:</b> ` + curs.map(c => this.bal(opening[c], c)).join(" &nbsp;|&nbsp; ") + "</p>");
    const cols = [t("Saat")].concat(person ? [] : [t("Kişi")]).concat([t("İşlem"), t("Birim"), t("Verilen (Çıktı)"),
      t("Alınan (Girdi)"), t("Bakiye"), t("Açıklama"), t("Belge")]);
    const th = "<thead><tr>" + cols.map(c => `<th>${esc(c)}</th>`).join("") + "</tr></thead>";
    const groups = new Map();
    for (const r of rows) {
      const key = o.hourly ? r.ts.slice(0, 13) : r.ts.slice(0, 10);
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(r);
    }
    if (!rows.length) H.push(`<p class="muted">${esc(t("Bu aralıkta kayıt yok."))}</p>`);
    for (const [key, items] of groups) {
      const d = parseTs(key.slice(0, 10) + " 00:00");
      let title = `<bdi dir="ltr">${key.slice(8, 10)}.${key.slice(5, 7)}.${key.slice(0, 4)}</bdi> ${esc(dayName(d))}`;
      if (o.hourly) title += ` — ${esc(t("saat"))} <bdi dir="ltr">${key.slice(11, 13)}:00–${key.slice(11, 13)}:59</bdi>`;
      H.push(`<h3>${title}</h3><table>${th}<tbody>`);
      const sub = {};
      for (const c of CURRENCIES) sub[c] = [0, 0];
      let ci = 0;
      const L = () => esc(cols[ci++]);
      for (const r of items) {
        const c = r.currency, ver = r.direction === "VERDIM";
        running[c] += ver ? r.amount : -r.amount;
        sub[c][ver ? 0 : 1] += r.amount;
        const n = Store.docCount(r.id);
        ci = 0;
        H.push(`<tr><td data-l="${L()}" class="t"><bdi dir="ltr">${r.ts.slice(11, 16)}</bdi></td>` +
          (person ? "" : `<td data-l="${L()}">${esc(Store.personName(r.person))}</td>`) +
          `<td data-l="${L()}" class="t ${ver ? "ver" : "al"}">${esc(ver ? t("Verdim") : t("Aldım"))}</td><td data-l="${L()}">${c}</td>` +
          `<td data-l="${L()}" class="n">${ver ? `<bdi dir="ltr">${esc(money(r.amount, c))}</bdi>` : ""}</td>` +
          `<td data-l="${L()}" class="n">${ver ? "" : `<bdi dir="ltr">${esc(money(r.amount, c))}</bdi>`}</td>` +
          `<td data-l="${L()}" class="n">${this.bal(running[c], c, true)}</td>` +
          `<td data-l="${L()}" class="desc">${esc(r.description || "")}</td><td data-l="${L()}" class="c">${n || "—"}</td></tr>`);
      }
      H.push("</tbody></table>");
      const subs = CURRENCIES.filter(c => sub[c][0] || sub[c][1]).map(c =>
        `${c}: ${esc(t("verilen"))} <bdi dir="ltr">${esc(money(sub[c][0], c))}</bdi>, ${esc(t("alınan"))} <bdi dir="ltr">${esc(money(sub[c][1], c))}</bdi>`);
      H.push(`<p class="subt">${esc(o.hourly ? t("Saat toplamı") : t("Gün toplamı"))} — ${subs.join(" | ")}</p>`);
    }
    const tot = {};
    for (const c of CURRENCIES) tot[c] = [0, 0];
    for (const r of rows) tot[r.currency][r.direction === "VERDIM" ? 0 : 1] += r.amount;
    const sc = [t("Para birimi"), t("Devreden"), t("Verilen"), t("Alınan"), t("Kapanış bakiyesi")];
    H.push(`<hr><h3 class="sum">${esc(t("Özet"))}</h3><table class="sumt"><thead><tr>` + sc.map(c => `<th>${esc(c)}</th>`).join("") + "</tr></thead><tbody>");
    for (const c of curs) {
      H.push(`<tr><td data-l="${esc(sc[0])}">${esc(t(CURRENCY_NAMES[c]))}</td><td data-l="${esc(sc[1])}" class="n">${this.bal(opening[c], c, true)}</td>` +
        `<td data-l="${esc(sc[2])}" class="n"><bdi dir="ltr">${esc(money(tot[c][0], c))}</bdi></td>` +
        `<td data-l="${esc(sc[3])}" class="n"><bdi dir="ltr">${esc(money(tot[c][1], c))}</bdi></td>` +
        `<td data-l="${esc(sc[4])}" class="n"><b>${this.bal(running[c], c)}</b></td></tr>`);
    }
    H.push(`</tbody></table><p class="foot">${esc(t("Bakiye: pozitif = alacak (kişi borçlu), negatif = verecek (biz borçluyuz)."))}</p>`);
    const body = H.join("");
    const dir = isRtl() ? "rtl" : "ltr";
    const docTitle = tf("Hesap Dökümü — {}", name);
    const full = `<!DOCTYPE html><html lang="${LANG}" dir="${dir}"><head><meta charset="utf-8">` +
      `<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light">` +
      `<title>${esc(docTitle)}</title><style>html{color-scheme:light}body{margin:12px;background:#fff}${STMT_BASE_CSS}` +
      `@media screen and (max-width:700px){${stmtStackCss(".st")}}</style></head>` +
      `<body><div class="st" dir="${dir}">${body}</div></body></html>`;
    const safe = String(person ? person.name : "tum").replace(/[^\p{L}\p{N}_-]+/gu, "_").slice(0, 40) || "kisi";
    return { body, full, title: docTitle, fileBase: `dokum_${safe}_${stamp()}` };
  },
  injectCss() {
    if ($("#st-css")) return;
    document.head.appendChild(h("style", { id: "st-css" }, STMT_BASE_CSS + stmtStackCss(".st.narrow")));
  },
  print(full, jobName) {
    if (bridgeHas("printHtml")) { bridge().printHtml(full, jobName); return; }
    const fr = h("iframe", { class: "print-frame", title: "print", "aria-hidden": "true" });
    document.body.appendChild(fr);
    fr.onload = () => {
      try { fr.contentWindow.focus(); fr.contentWindow.print(); } catch (e) { console.warn(e); }
      setTimeout(() => fr.remove(), 60000);
    };
    fr.srcdoc = full;
  },
};
