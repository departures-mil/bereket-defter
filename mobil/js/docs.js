/* Dekont / belgeler: küçük resimler, dosya türü kutucukları, tam ekran görüntüleyici (iki parmakla yakınlaştırma). */
'use strict';

/** belge nesnesi: {id?, name, ext, mime, size, blob? (yeni dosya)} */
async function docBlob(d) {
  if (d.blob) return d.blob;
  return d.id ? Store.getBlob(d.id) : null;
}
const EXT_COLORS = { ".pdf": "#c0392b", ".doc": "#2b579a", ".docx": "#2b579a", ".xls": "#217346", ".xlsx": "#217346",
  ".zip": "#7d5a00", ".txt": "#556", ".heic": "#8e44ad" };

function docTile(d, { onOpen, onRemove } = {}) {
  const img = isImageDoc(d);
  const face = h("div", { class: "dface" });
  if (img) {
    const im = h("img", { alt: d.name, loading: "lazy", decoding: "async" });
    im.onerror = () => { clear(face).append(typeFace(d)); };
    face.append(im);
    if (d.blob) { im.src = URL.createObjectURL(d.blob); d._url = im.src; }
    else if (d.id) Thumbs.url(d.id).then(u => { if (u) im.src = u; else { clear(face).append(typeFace(d, true)); } });
  } else {
    face.append(typeFace(d, d.id && !d.blob && !Store.blobIds.has(d.id)));
  }
  const tile = h("div", { class: "dtile" },
    h("button", { type: "button", class: "dopen", title: d.name, "aria-label": t("Aç") + ": " + d.name, onclick: () => (onOpen || openDoc)(d) },
      face, h("div", { class: "dname" }, d.name)),
    onRemove ? h("button", { type: "button", class: "drm", title: t("Seçili belgeyi kaldır"), "aria-label": t("Seçili belgeyi kaldır"),
      onclick: e => { e.stopPropagation(); onRemove(d); } }, "✕") : null);
  return tile;
}
function typeFace(d, missing) {
  const ext = (d.ext || extOf(d.name, d.mime) || "?").replace(".", "").toUpperCase().slice(0, 5);
  return h("div", { class: "dtype", style: `background:${EXT_COLORS[d.ext] || "#0b6e74"}` },
    h("span", { class: "dtype-ext" }, missing ? "⏳" : ext), h("span", { class: "dtype-size" }, missing ? t("İndiriliyor…") : fileSizeText(d.size)));
}

async function openDoc(d) {
  const blob = await docBlob(d);
  if (!blob) { Dlg.alert(t("Bu belge henüz bu cihaza inmedi. Eşitleme bitince tekrar deneyin."), t("Belge")); return; }
  if (isImageDoc(d)) { Viewer.open(d, blob); return; }
  Dlg.menu([
    { icon: h("span", { class: "mi-emo" }, "📂"), label: t("Aç"), fn: () => openBlobExternal(blob, mimeOfDoc(d), d.name) },
    { icon: h("span", { class: "mi-emo" }, "💾"), label: t("Farklı kaydet…"), fn: () => saveBlobAs(blob, mimeOfDoc(d), d.name) },
    { icon: h("span", { class: "mi-emo" }, "📤"), label: t("Paylaş"), fn: () => shareBlob(blob, mimeOfDoc(d), d.name) },
  ], d.name);
}

/* ------------------------------------------------------------------ tam ekran resim görüntüleyici */
const Viewer = {
  active: null,
  open(d, blob) {
    const url = URL.createObjectURL(blob);
    const img = h("img", { class: "vimg", src: url, alt: d.name, draggable: "false" });
    const stage = h("div", { class: "vstage" }, img);
    const st = { s: 1, x: 0, y: 0 };
    const apply = () => { img.style.transform = `translate(${st.x}px, ${st.y}px) scale(${st.s})`; };
    const clampPan = () => {
      const r = stage.getBoundingClientRect();
      const w = img.offsetWidth * st.s, hh = img.offsetHeight * st.s;
      const mx = Math.max(0, (w - r.width) / 2), my = Math.max(0, (hh - r.height) / 2);
      st.x = Math.min(mx, Math.max(-mx, st.x));
      st.y = Math.min(my, Math.max(-my, st.y));
    };
    const zoomAt = (ns, cx, cy) => {
      ns = Math.min(8, Math.max(1, ns));
      const r = stage.getBoundingClientRect();
      const ox = cx - (r.left + r.width / 2), oy = cy - (r.top + r.height / 2);
      st.x = ox - (ox - st.x) * (ns / st.s);
      st.y = oy - (oy - st.y) * (ns / st.s);
      st.s = ns;
      if (st.s === 1) { st.x = 0; st.y = 0; }
      clampPan(); apply();
    };
    const pts = new Map();
    let pinch = null, pan = null, lastTap = 0;
    stage.addEventListener("pointerdown", e => {
      stage.setPointerCapture(e.pointerId);
      pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pts.size === 2) {
        const [a, b] = [...pts.values()];
        pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), s: st.s };
        pan = null;
      } else if (pts.size === 1) {
        pan = { x: e.clientX, y: e.clientY, sx: st.x, sy: st.y };
        const now = Date.now();
        if (now - lastTap < 300) { zoomAt(st.s > 1.2 ? 1 : 2.5, e.clientX, e.clientY); pan = null; }
        lastTap = now;
      }
    });
    stage.addEventListener("pointermove", e => {
      if (!pts.has(e.pointerId)) return;
      pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pinch && pts.size >= 2) {
        const [a, b] = [...pts.values()];
        const d2 = Math.hypot(a.x - b.x, a.y - b.y);
        zoomAt(pinch.s * d2 / (pinch.d || 1), (a.x + b.x) / 2, (a.y + b.y) / 2);
      } else if (pan && st.s > 1) {
        st.x = pan.sx + e.clientX - pan.x; st.y = pan.sy + e.clientY - pan.y;
        clampPan(); apply();
      }
    });
    const up = e => { pts.delete(e.pointerId); if (pts.size < 2) pinch = null; if (!pts.size) pan = null; };
    stage.addEventListener("pointerup", up);
    stage.addEventListener("pointercancel", up);
    stage.addEventListener("wheel", e => { e.preventDefault(); zoomAt(st.s * (e.deltaY < 0 ? 1.2 : 1 / 1.2), e.clientX, e.clientY); }, { passive: false });
    const close = () => this.close();
    const mime = mimeOfDoc(d);
    const el = h("div", { class: "viewer", role: "dialog", "aria-modal": "true", "aria-label": d.name },
      h("div", { class: "vbar" }, h("div", { class: "vname" }, d.name),
        h("button", { class: "icon-btn vx", type: "button", "aria-label": t("Kapat"), title: t("Kapat"), onclick: close }, "✕")),
      stage,
      h("div", { class: "vtools" },
        h("button", { class: "btn light", type: "button", onclick: () => zoomAt(st.s * 1.25, innerWidth / 2, innerHeight / 2) }, t("Yakınlaştır +")),
        h("button", { class: "btn light", type: "button", onclick: () => zoomAt(st.s / 1.25, innerWidth / 2, innerHeight / 2) }, t("Uzaklaştır −")),
        h("button", { class: "btn light", type: "button", onclick: () => saveBlobAs(blob, mime, d.name) }, t("Farklı kaydet…")),
        h("button", { class: "btn light", type: "button", onclick: () => shareBlob(blob, mime, d.name) }, t("Paylaş")),
        h("button", { class: "btn light", type: "button", onclick: () => openBlobExternal(blob, mime, d.name) }, t("Harici programda aç"))));
    document.body.appendChild(el);
    document.body.classList.add("noscroll");
    this.active = { el, url };
  },
  close() {
    if (!this.active) return;
    this.active.el.remove();
    URL.revokeObjectURL(this.active.url);
    this.active = null;
    if (!Sheets.stack.length) document.body.classList.remove("noscroll");
  },
};
