package com.bereket.alacakverecek;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.webkit.WebView;

import com.departuresmil.ortak.FcDelta;

import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Ortak çekirdek Android güncellemesi (v1.21) — window.AndroidBridge.apkUpdate(planJson) buraya gelir
 * (MainActivity$Bridge.smali içindeki küçük yönlendirme yöntemleri; Java kaynağı yalnız bu dosya + ortak FcDelta).
 *
 * plan: {version, full:{url, sha256, size}, patch:{url, sha256, size}|null} — FC.updater, GitHub Releases latest.json → "android" kanalı.
 * 1) Yama varsa: indir (SHA-256 doğrula) → kurulu APK (applicationInfo.sourceDir) + FCD1 yama → yeni APK; hedef SHA-256 tam APK'nınkiyle aynı olmalı.
 * 2) Yama yoksa ya da herhangi bir hata olursa: tam APK indirilir, SHA-256 doğrulanır.
 * 3) Sonuç cache/apk/BereketDefter.apk (eski installApk ile aynı yer, FilesProvider bu klasörü verir) → paket yükleyici açılır.
 * Olaylar JS'e: window.__fcApk({type:'progress'|'patchFailed'|'installing'|'done'|'error', …}). "Bilinmeyen uygulamalar" izni yoksa
 * ayar ekranı açılır ve 'error' IZIN döner (kullanıcı izin verip Güncelle'ye yeniden basar). İndirme yerelde yapılır: WebView'den
 * GitHub indirmesi CORS'a takılır. Tüm sürümler aynı anahtarla imzalanır (CI: ANDROID_KEYSTORE_* secret'ları).
 *
 * v1.22.1: window.AndroidBridge.httpGet(id, url) — latest.json gibi küçük metinleri (≤ 2 MB) yerelde indirir; sonuç
 * window.__fcHttp(id, {status, body} | {error}). WebView (https://appassets.androidplatform.net) GitHub'dan fetch edemiyordu
 * ("Failed to fetch": github.com yönlendirmesi CORS başlığı vermez), bu yüzden 1.21–1.22'de telefon güncellemesi hiç başlamıyordu.
 */
public final class FcGuncelle {
    private static volatile boolean busy = false;

    private FcGuncelle() { }

    public static void notify(Context c, String title, String body) {
        try { Reminders.show(c.getApplicationContext(), "fc_agent", title, body); } catch (Throwable ignored) { }
    }

    public static void apkUpdate(final Activity a, final WebView w, final String planJson) {
        if (busy) { emit(a, w, "{\"type\":\"error\",\"error\":\"BUSY\"}"); return; }
        busy = true;
        new Thread(new Runnable() {
            @Override public void run() {
                try {
                    JSONObject p = new JSONObject(planJson);
                    JSONObject full = p.getJSONObject("full");
                    JSONObject patch = p.optJSONObject("patch");
                    File dir = new File(a.getCacheDir(), "apk");
                    if (!dir.isDirectory() && !dir.mkdirs()) throw new IOException("WRITE");
                    File out = new File(dir, "BereketDefter.apk");
                    String want = full.getString("sha256").toLowerCase();
                    boolean ok = false;
                    if (patch != null && patch.optString("url", "").length() > 0) {
                        File pf = new File(dir, "update.patch");
                        try {
                            download(a, w, patch.getString("url"), pf, patch.optLong("size", 0), true);
                            String ps = patch.optString("sha256", "");
                            if (ps.length() > 0 && !ps.equalsIgnoreCase(FcDelta.hex(FcDelta.sha256(pf)))) throw new IOException("BAD_HASH");
                            File installed = new File(a.getApplicationInfo().sourceDir);
                            FcDelta.Header h = FcDelta.apply(installed, pf, out, null);
                            if (!want.equalsIgnoreCase(h.dstSha256Hex())) throw new IOException("BAD_HASH");
                            ok = true;
                        } catch (Exception e) {
                            emit(a, w, "{\"type\":\"patchFailed\",\"error\":" + JSONObject.quote(String.valueOf(e.getMessage())) + "}");
                        } finally {
                            pf.delete();
                        }
                    }
                    if (!ok) {
                        download(a, w, full.getString("url"), out, full.optLong("size", 0), false);
                        if (!want.equalsIgnoreCase(FcDelta.hex(FcDelta.sha256(out)))) { out.delete(); throw new IOException("BAD_HASH"); }
                    }
                    if (Build.VERSION.SDK_INT >= 26 && !a.getPackageManager().canRequestPackageInstalls()) {
                        a.runOnUiThread(new Runnable() { @Override public void run() {
                            try {
                                a.startActivity(new Intent("android.settings.MANAGE_UNKNOWN_APP_SOURCES", Uri.parse("package:" + a.getPackageName())));
                            } catch (Throwable ignored) { }
                        } });
                        throw new IOException("IZIN");
                    }
                    emit(a, w, "{\"type\":\"installing\"}");
                    final File apk = out;
                    a.runOnUiThread(new Runnable() { @Override public void run() {
                        try {
                            Intent i = new Intent(Intent.ACTION_VIEW);
                            i.setDataAndType(FilesProvider.uriFor(a, apk), "application/vnd.android.package-archive");
                            i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
                            a.startActivity(i);
                        } catch (Throwable e) {
                            emit(a, w, "{\"type\":\"error\",\"error\":\"INSTALLER\"}");
                        }
                    } });
                    emit(a, w, "{\"type\":\"done\",\"result\":\"done\"}");
                } catch (Exception e) {
                    emit(a, w, "{\"type\":\"error\",\"error\":" + JSONObject.quote(String.valueOf(e.getMessage())) + "}");
                } finally {
                    busy = false;
                }
            }
        }, "fc-guncelle").start();
    }

    public static void httpGet(final Activity a, final WebView w, final String id, final String url) {
        new Thread(new Runnable() {
            @Override public void run() {
                String res;
                HttpURLConnection c = null;
                try {
                    c = open(url);
                    int st = c.getResponseCode();
                    String body = "";
                    if (st == 200) {
                        InputStream in = c.getInputStream();
                        java.io.ByteArrayOutputStream bo = new java.io.ByteArrayOutputStream();
                        try {
                            byte[] buf = new byte[16384];
                            int n;
                            while ((n = in.read(buf)) > 0) {
                                bo.write(buf, 0, n);
                                if (bo.size() > 2 * 1024 * 1024) throw new IOException("TOO_BIG");
                            }
                        } finally {
                            try { in.close(); } catch (IOException ignored) { }
                        }
                        body = new String(bo.toByteArray(), "UTF-8");
                    }
                    res = "{\"status\":" + st + ",\"body\":" + JSONObject.quote(body) + "}";
                } catch (Exception e) {
                    res = "{\"error\":" + JSONObject.quote(String.valueOf(e.getMessage())) + "}";
                } finally {
                    if (c != null) c.disconnect();
                }
                final String js = "window.__fcHttp && window.__fcHttp(" + JSONObject.quote(String.valueOf(id)) + "," + res + ")";
                if (w == null) return;
                a.runOnUiThread(new Runnable() { @Override public void run() {
                    try { w.evaluateJavascript(js, null); } catch (Throwable ignored) { }
                } });
            }
        }, "fc-http").start();
    }

    /** GitHub adresini açar, yönlendirmeleri (en çok 6) izler; dönen bağlantının yanıt kodu 3xx değildir. */
    private static HttpURLConnection open(String url) throws IOException {
        if (url == null || (!url.startsWith("https://github.com/") && !url.startsWith("https://objects.githubusercontent.com/")
                && !url.startsWith("https://release-assets.githubusercontent.com/"))) throw new IOException("BAD_URL");
        for (int hop = 0; hop < 6; hop++) {
            HttpURLConnection c = (HttpURLConnection) new URL(url).openConnection();
            c.setInstanceFollowRedirects(false);
            c.setUseCaches(false);
            c.setConnectTimeout(20000);
            c.setReadTimeout(60000);
            c.setRequestProperty("User-Agent", "BereketDefter-Android");
            int st = c.getResponseCode();
            if (st >= 300 && st < 400) {
                String loc = c.getHeaderField("Location");
                c.disconnect();
                if (loc == null || !loc.startsWith("https://")) throw new IOException("HTTP " + st);
                url = loc;
                continue;
            }
            return c;
        }
        throw new IOException("REDIRECTS");
    }

    private static void download(Activity a, WebView w, String url, File dst, long size, boolean patch) throws IOException {
        HttpURLConnection c = open(url);
        int st = c.getResponseCode();
        if (st != 200) { c.disconnect(); throw new IOException("HTTP " + st); }
        long total = size > 0 ? size : Math.max(0, c.getContentLength());
        long done = 0, last = 0;
        InputStream in = c.getInputStream();
        FileOutputStream fo = new FileOutputStream(dst);
        try {
            byte[] buf = new byte[65536];
            int n;
            while ((n = in.read(buf)) > 0) {
                fo.write(buf, 0, n);
                done += n;
                long now = System.currentTimeMillis();
                if (now - last > 200) {
                    last = now;
                    emit(a, w, "{\"type\":\"progress\",\"patch\":" + patch + ",\"done\":" + done + ",\"total\":" + total + "}");
                }
            }
        } finally {
            try { fo.close(); } catch (IOException ignored) { }
            try { in.close(); } catch (IOException ignored) { }
            c.disconnect();
        }
        emit(a, w, "{\"type\":\"progress\",\"patch\":" + patch + ",\"done\":" + done + ",\"total\":" + total + ",\"finished\":true}");
    }

    private static void emit(Activity a, final WebView w, final String json) {
        if (w == null) return;
        a.runOnUiThread(new Runnable() { @Override public void run() {
            try { w.evaluateJavascript("window.__fcApk && window.__fcApk(" + json + ")", null); } catch (Throwable ignored) { }
        } });
    }
}
