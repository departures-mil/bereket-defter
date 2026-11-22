"""Wi‑Fi (aynı modem / router) üzerinden internetsiz eşitleme — telefon ⇄ bilgisayar (v1.12).

Bilgisayar açık olduğu sürece aynı ağdaki telefonu bekler (HTTP, port 47341, JSON):
  GET  /bereket/lan/hello                       → {app, name, version, account}
  POST /bereket/lan/sync   {key, docs:{col:[fields]}, have:[belge kimliği]}
                           → {docs:{col:[fields]}, need:[belge kimliği], name}
  POST /bereket/lan/blob   {key, id}            → {data: base64} (bilgisayardaki belge dosyası)
  POST /bereket/lan/upload {key, id, data}      → {ok: true} (telefondaki belge dosyası)
Kayıtlar Firebase eşitlemesiyle AYNI biçimde (Firestore alanları) ve AYNI kuralla birleştirilir (SyncEngine._apply):
her kayıtta son değiştirilen (m) kazanır, silinenler işaretle yayılır, hiçbir şey körü körüne üzerine yazılmaz.
Wi‑Fi'dan gelen değişiklikler "kirli" işaretlenir: internet gelince buluta da gönderilir (iki taraf da gönderebilir; aynı m
ikinci kez yazılınca hiçbir şey değişmez). Anahtar: bilgisayardaki 6 haneli eşleme kodu ya da iki cihaz aynı bulut
hesabına bağlıysa hesaptan türetilen anahtar.
Tüm veritabanı işleri eşitleme motorunun kendi iş parçacığında, bulut eşitlemesiyle sırayla yapılır.
"""
import base64
import hashlib
import json
import os
import random
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 47341
MAX_BODY = 80 * 1024 * 1024


def uid_key(uid):
    return hashlib.sha256(f"bereket-lan:{uid}".encode()).hexdigest()[:24] if uid else ""


def local_ips():
    out = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        out.append(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    try:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if ip not in out and not ip.startswith("127."):
                out.append(ip)
    except OSError:
        pass
    return out


class LanServer:
    def __init__(self, engine, version=""):
        self.engine = engine
        self.version = version
        self.httpd = None
        self.error = ""
        self.last = None        # {"at", "name", "got", "sent"}

    # --- eşleme kodu (esitleme.json → lanCode)
    def code(self):
        c = self.engine.cfg.get("lanCode") or ""
        if not (len(c) == 6 and c.isdigit()):
            c = "".join(random.choice("0123456789") for _ in range(6))
            with self.engine._lock:
                self.engine.cfg["lanCode"] = c
            self.engine._save()
        return c

    def new_code(self):
        with self.engine._lock:
            self.engine.cfg["lanCode"] = ""
        return self.code()

    def key_ok(self, key):
        key = str(key or "").strip()
        if not key:
            return False
        if key == self.code():
            return True
        uk = uid_key(self.engine.cfg.get("uid"))
        return bool(uk) and key == uk

    @property
    def running(self):
        return self.httpd is not None

    def start(self):
        if self.httpd:
            return True
        srv = self

        class H(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *a):
                pass

            def _cors(self):
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.send_header("Access-Control-Allow-Private-Network", "true")

            def _send(self, code, obj):
                data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
                self.send_response(code)
                self._cors()
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_OPTIONS(self):
                self.send_response(204)
                self._cors()
                self.send_header("Content-Length", "0")
                self.end_headers()

            def do_GET(self):
                if self.path.split("?")[0] == "/bereket/lan/hello":
                    return self._send(200, {"app": "bereket-lan", "name": socket.gethostname(), "version": srv.version,
                                            "account": bool(srv.engine.cfg.get("uid"))})
                self._send(404, {"error": "not found"})

            def do_POST(self):
                try:
                    n = int(self.headers.get("Content-Length") or 0)
                    if n <= 0 or n > MAX_BODY:
                        return self._send(413, {"error": "size"})
                    body = json.loads(self.rfile.read(n).decode("utf-8"))
                except Exception:
                    return self._send(400, {"error": "bad request"})
                if not srv.key_ok(body.get("key")):
                    return self._send(403, {"error": "key"})
                kind = self.path.split("?")[0].rsplit("/", 1)[-1]
                if kind not in ("sync", "blob", "upload"):
                    return self._send(404, {"error": "not found"})
                res = srv.engine.lan_call(kind, body)
                if res is None:
                    return self._send(503, {"error": "busy"})
                if res.get("error"):
                    return self._send(500, res)
                if kind == "sync":
                    srv.last = {"name": body.get("device") or "", "got": res.get("_got", 0), "sent": res.get("_sent", 0)}
                res.pop("_got", None)
                res.pop("_sent", None)
                self._send(200, res)

        try:
            self.httpd = ThreadingHTTPServer(("0.0.0.0", PORT), H)
            self.httpd.daemon_threads = True
        except OSError as e:
            self.httpd = None
            self.error = str(e)
            return False
        self.error = ""
        threading.Thread(target=self.httpd.serve_forever, name="wifi-esitleme", daemon=True).start()
        return True

    def stop(self):
        if self.httpd:
            h, self.httpd = self.httpd, None
            threading.Thread(target=h.shutdown, daemon=True).start()
