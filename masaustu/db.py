"""SQLite veritabanı katmanı."""
import ast
import json
import mimetypes
import os
import shutil
import sqlite3
import sys
import time
import uuid
from datetime import datetime

CURRENCIES = ["USD", "TRY", "SYP"]
CURRENCY_NAMES = {"USD": "Dolar ($)", "TRY": "Türk Lirası (₺)", "SYP": "Suriye Lirası (£S)"}
CURRENCY_SYMBOLS = {"USD": "$", "TRY": "₺", "SYP": "£S"}
# VERDIM: kişiye verdim (o bana borçlu -> alacağım artar)
# ALDIM : kişiden aldım (alacağım azalır / ben borçlanırım)
DIRECTIONS = {"VERDIM": "Verdim (Çıktı)", "ALDIM": "Aldım (Girdi)"}
# Kişiye ulaşma yolları (her biri açılıp kapatılabilir) ve ek iletişim bilgileri
CHANNELS = ("wa", "tg", "sg", "call")
CONTACT_FIELDS = ("phone2", "wa_phone", "tg_user", "sg_phone", "email", "address", "tags")   # v1.22: tags = etiketler (virgülle)
# Eşitleme (v1.2): yerel tablo -> Firestore koleksiyonu (ESITLEME_SPEC.md)
SYNC_TABLES = {"persons": "persons", "transactions": "tx", "photos": "docs", "reminders": "rem", "history": "hist"}
CHUNK = 700000  # bir blob parçasındaki en fazla bayt


def now_ms():
    return int(time.time() * 1000)


def new_uid():
    return uuid.uuid4().hex


def file_chunks(size):
    return (size + CHUNK - 1) // CHUNK if size > 0 else 0


def parse_old(text):
    """Geçmiş satırındaki eski değerler: v1.2+ JSON, v1.0-1.1 Python repr(dict)."""
    if not text:
        return {}
    try:
        v = json.loads(text)
    except ValueError:
        try:
            v = ast.literal_eval(text)
        except (ValueError, SyntaxError):
            return {}
    return v if isinstance(v, dict) else {}


POINTER = "veri-konumu.txt"   # v1.21: eski taşınabilir kurulumun veri klasörü (köprü yazar, kurulu program okur)


def default_data_dir():
    base = os.environ.get("APPDATA") if sys.platform == "win32" else os.path.expanduser("~/.local/share")
    return os.path.join(base or os.path.expanduser("~"), "AlacakVerecek")


def data_dir():
    """Veri klasörü HİÇ değişmez: AV_DATA_DIR (eski taşınabilir başlatıcı) > köprünün bıraktığı işaret > %APPDATA%\\AlacakVerecek."""
    d = os.environ.get("AV_DATA_DIR")
    if not d:
        d = default_data_dir()
        try:
            with open(os.path.join(d, POINTER), encoding="utf-8-sig") as f:
                alt = f.read().strip()
            if alt and os.path.isfile(os.path.join(alt, "veriler.db")):
                d = alt
        except OSError:
            pass
    os.makedirs(os.path.join(d, "fotograflar"), exist_ok=True)
    return d


def remember_data_dir(d):
    """Köprü: bu kurulumun veri klasörü varsayılan değilse, yeni kurulum aynı klasörü açsın diye işaret bırakır."""
    d = os.path.abspath(d)
    base = default_data_dir()
    if os.path.normcase(d) == os.path.normcase(os.path.abspath(base)):
        return False
    os.makedirs(base, exist_ok=True)
    tmp = os.path.join(base, POINTER + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(d)
    os.replace(tmp, os.path.join(base, POINTER))
    return True


SCHEMA = """
CREATE TABLE IF NOT EXISTS persons(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  phone TEXT DEFAULT '',
  note TEXT DEFAULT '',
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS transactions(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  person_id INTEGER NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
  ts TEXT NOT NULL,
  direction TEXT NOT NULL CHECK(direction IN ('VERDIM','ALDIM')),
  currency TEXT NOT NULL CHECK(currency IN ('USD','TRY','SYP')),
  amount REAL NOT NULL CHECK(amount > 0),
  description TEXT DEFAULT '',
  created_at TEXT NOT NULL,
  updated_at TEXT
);
CREATE INDEX IF NOT EXISTS ix_tx_person_ts ON transactions(person_id, ts);
CREATE TABLE IF NOT EXISTS photos(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tx_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
  file TEXT NOT NULL,
  original_name TEXT DEFAULT '',
  added_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reminders(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  person_id INTEGER NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
  kind TEXT NOT NULL CHECK(kind IN ('TAHSIL','ODEME')),
  currency TEXT NOT NULL CHECK(currency IN ('USD','TRY','SYP')),
  amount REAL NOT NULL DEFAULT 0,
  due TEXT NOT NULL,
  note TEXT DEFAULT '',
  done INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_rem_due ON reminders(done, due);
CREATE TABLE IF NOT EXISTS history(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tx_id INTEGER NOT NULL,
  action TEXT NOT NULL,
  old_values TEXT,
  at TEXT NOT NULL
);
"""


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class DB:
    def __init__(self, path=None):
        self.dir = os.path.dirname(os.path.abspath(path)) if path else data_dir()
        self.path = path or os.path.join(self.dir, "veriler.db")
        self.photo_dir = os.path.join(self.dir, "fotograflar")
        os.makedirs(self.photo_dir, exist_ok=True)
        self.on_change = None  # yerel değişiklikte çağrılır (eşitleme zamanlayıcısı)
        self._last_m = 0
        self.con = sqlite3.connect(self.path, timeout=30)
        self.con.row_factory = sqlite3.Row
        self.con.execute("PRAGMA foreign_keys=ON")
        self.con.executescript(SCHEMA)
        self._migrate()
        self.con.commit()

    def _migrate(self):
        cols = {r[1] for r in self.con.execute("PRAGMA table_info(persons)")}
        for c in CONTACT_FIELDS:
            if c not in cols:
                self.con.execute(f"ALTER TABLE persons ADD COLUMN {c} TEXT DEFAULT ''")
        for c in CHANNELS:
            if "ch_" + c not in cols:
                self.con.execute(f"ALTER TABLE persons ADD COLUMN ch_{c} INTEGER DEFAULT 0")
        # v1.2 eşitleme: her satıra uid (uuid hex), m (ms) ve dirty (gönderilecek) eklenir
        extra = {"photos": (("mime", "TEXT DEFAULT ''"), ("size", "INTEGER DEFAULT -1"),
                            ("chunks", "INTEGER DEFAULT 0"), ("blobs_up", "INTEGER DEFAULT 0")),
                 "history": (("tx_uid", "TEXT DEFAULT ''"),)}
        for t in SYNC_TABLES:
            cols = {r[1] for r in self.con.execute(f"PRAGMA table_info({t})")}
            for c, decl in (("uid", "TEXT"), ("m", "INTEGER DEFAULT 0"), ("dirty", "INTEGER DEFAULT 0")) + \
                    extra.get(t, ()):
                if c not in cols:
                    self.con.execute(f"ALTER TABLE {t} ADD COLUMN {c} {decl}")
        # v1.21: hiçbir kayıt kalıcı silinmez — silinen (bu cihazda ya da başka cihazda) arşive, çakışmada eski hal yedeğe
        self.con.execute("CREATE TABLE IF NOT EXISTS arsiv(id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, "
                         "kaynak TEXT NOT NULL, tur TEXT NOT NULL, uid TEXT, baslik TEXT, veri TEXT NOT NULL, "
                         "geri INTEGER NOT NULL DEFAULT 0)")
        self.con.execute("CREATE TABLE IF NOT EXISTS cakisma(id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, "
                         "tur TEXT NOT NULL, uid TEXT, veri TEXT NOT NULL)")
        self.con.execute("CREATE TABLE IF NOT EXISTS tombstones(col TEXT NOT NULL, uid TEXT NOT NULL, "
                         "m INTEGER NOT NULL, dirty INTEGER NOT NULL DEFAULT 1, chunks INTEGER DEFAULT 0, "
                         "PRIMARY KEY(col, uid))")
        m = now_ms()
        for t in SYNC_TABLES:
            for r in self.con.execute(f"SELECT id FROM {t} WHERE uid IS NULL OR uid=''").fetchall():
                self.con.execute(f"UPDATE {t} SET uid=?, m=?, dirty=1 WHERE id=?", (new_uid(), m, r[0]))
            self.con.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS ux_{t}_uid ON {t}(uid)")
            self.con.execute(f"CREATE INDEX IF NOT EXISTS ix_{t}_dirty ON {t}(dirty)")
        self.con.execute("UPDATE history SET tx_uid=(SELECT uid FROM transactions t WHERE t.id=history.tx_id) "
                         "WHERE (tx_uid IS NULL OR tx_uid='') AND tx_id IN (SELECT id FROM transactions)")
        orphan = {}
        for r in self.con.execute("SELECT id, tx_id FROM history WHERE tx_uid IS NULL OR tx_uid=''").fetchall():
            # silinmiş kayıtların eski geçmişi: aynı kayda aynı uuid
            self.con.execute("UPDATE history SET tx_uid=? WHERE id=?", (orphan.setdefault(r[1], new_uid()), r[0]))

    # --- eşitleme yardımcıları ---------------------------------------------
    def _m(self):
        """Bu değişikliğin zamanı (ms); aynı milisaniyede iki değişiklik olsa da artar."""
        self._last_m = max(now_ms(), self._last_m + 1)
        return self._last_m

    def _changed(self):
        cb = self.on_change
        if cb:
            try:
                cb()
            except Exception:
                pass

    def _tomb(self, col, uid, m, chunks=0):
        if uid:
            self.con.execute("INSERT OR REPLACE INTO tombstones(col,uid,m,dirty,chunks) VALUES(?,?,?,1,?)",
                             (col, uid, m, chunks))

    def _remove_file(self, row):
        """v1.21: belge dosyası silinmez, fotograflar/arsiv altına taşınır (arşivden geri alınabilir)."""
        src = self.photo_path(row)
        if not os.path.isfile(src):
            return
        dst = os.path.join(self.photo_dir, "arsiv", row["file"])
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst):
                dst = os.path.splitext(dst)[0] + "-" + new_uid()[:6] + os.path.splitext(dst)[1]
            os.replace(src, dst)
        except OSError:
            pass

    def _tomb_photos(self, tid, m):
        """Kaydın belgelerini silinmiş olarak işaretler ve dosyalarını siler (satırları silmez)."""
        for ph in self.con.execute("SELECT * FROM photos WHERE tx_id=?", (tid,)).fetchall():
            self._tomb("docs", ph["uid"], m, ph["chunks"] if ph["blobs_up"] else 0)
            self._remove_file(ph)
        self._remove_photo_files(tid)

    # --- kişiler ---------------------------------------------------------
    def persons(self, search=""):
        q = "SELECT * FROM persons"
        args = []
        if search:
            q += " WHERE name LIKE ? OR phone LIKE ? OR phone2 LIKE ? OR email LIKE ? OR tags LIKE ?"
            args = [f"%{search}%"] * 5
        return self.con.execute(q + " ORDER BY name COLLATE NOCASE", args).fetchall()

    def person(self, pid):
        return self.con.execute("SELECT * FROM persons WHERE id=?", (pid,)).fetchone()

    def add_person(self, name, phone="", note="", extra=None):
        cur = self.con.execute("INSERT INTO persons(name,phone,note,created_at,uid,m,dirty) VALUES(?,?,?,?,?,?,1)",
                               (name.strip(), phone.strip(), note.strip(), now(), new_uid(), self._m()))
        self.con.commit()
        if extra:
            self.update_contact(cur.lastrowid, extra)
        self._changed()
        return cur.lastrowid

    def update_person(self, pid, name, phone, note, extra=None):
        self.con.execute("UPDATE persons SET name=?,phone=?,note=?,m=?,dirty=1 WHERE id=?",
                         (name.strip(), phone.strip(), note.strip(), self._m(), pid))
        self.con.commit()
        if extra:
            self.update_contact(pid, extra)
        self._changed()

    def update_contact(self, pid, fields):
        """İletişim alanlarını günceller: name/phone/note, CONTACT_FIELDS ve ch_* açık/kapalı."""
        allowed = {"name", "phone", "note", *CONTACT_FIELDS, *("ch_" + c for c in CHANNELS)}
        for k, v in fields.items():
            if k not in allowed:
                continue
            v = (1 if v else 0) if k.startswith("ch_") else str(v or "").strip()
            if k == "name" and not v:
                continue
            self.con.execute(f"UPDATE persons SET {k}=?,m=?,dirty=1 WHERE id=?", (v, self._m(), pid))
        self.con.commit()
        self._changed()

    def set_channel(self, pid, ch, on):
        self.update_contact(pid, {"ch_" + ch: on})

    def delete_person(self, pid):
        self.archive("persons", pid)
        m = self._m()
        for t in self.con.execute("SELECT id, uid FROM transactions WHERE person_id=?", (pid,)).fetchall():
            self._tomb_photos(t["id"], m)
            self._tomb("tx", t["uid"], m)
        for r in self.con.execute("SELECT uid FROM reminders WHERE person_id=?", (pid,)).fetchall():
            self._tomb("rem", r["uid"], m)
        p = self.person(pid)
        if p:
            self._tomb("persons", p["uid"], m)
        self.con.execute("DELETE FROM persons WHERE id=?", (pid,))
        self.con.commit()
        self._changed()

    def tx_count(self, pid):
        return self.con.execute("SELECT COUNT(*) FROM transactions WHERE person_id=?", (pid,)).fetchone()[0]

    # --- bakiyeler -------------------------------------------------------
    def balances(self, pid=None, until=None):
        """{currency: (verilen, alinan, bakiye)}; bakiye > 0 => alacak."""
        q = ("SELECT currency, SUM(CASE WHEN direction='VERDIM' THEN amount ELSE 0 END) v,"
             " SUM(CASE WHEN direction='ALDIM' THEN amount ELSE 0 END) a FROM transactions WHERE 1=1")
        args = []
        if pid is not None:
            q += " AND person_id=?"
            args.append(pid)
        if until:
            q += " AND ts<?"
            args.append(until)
        res = {c: (0.0, 0.0, 0.0) for c in CURRENCIES}
        for r in self.con.execute(q + " GROUP BY currency", args):
            v, a = r["v"] or 0.0, r["a"] or 0.0
            res[r["currency"]] = (v, a, v - a)
        return res

    def totals_overall(self):
        """Her para birimi için toplam alacak ve toplam verecek (kişi bazında netleştirilmiş)."""
        res = {c: [0.0, 0.0] for c in CURRENCIES}
        q = ("SELECT person_id, currency, SUM(CASE WHEN direction='VERDIM' THEN amount ELSE -amount END) b"
             " FROM transactions GROUP BY person_id, currency")
        for r in self.con.execute(q):
            if r["b"] > 0:
                res[r["currency"]][0] += r["b"]
            elif r["b"] < 0:
                res[r["currency"]][1] += -r["b"]
        return res

    # --- kayıtlar --------------------------------------------------------
    def transactions(self, pid=None, start=None, end=None, currency=None, text=""):
        q = ("SELECT t.*, p.name person_name, (SELECT COUNT(*) FROM photos f WHERE f.tx_id=t.id) photo_count"
             " FROM transactions t JOIN persons p ON p.id=t.person_id WHERE 1=1")
        args = []
        if pid is not None:
            q += " AND t.person_id=?"
            args.append(pid)
        if start:
            q += " AND t.ts>=?"
            args.append(start)
        if end:
            q += " AND t.ts<=?"
            args.append(end)
        if currency:
            q += " AND t.currency=?"
            args.append(currency)
        if text:
            q += " AND (t.description LIKE ? OR p.name LIKE ?)"
            args += [f"%{text}%", f"%{text}%"]
        return self.con.execute(q + " ORDER BY t.ts, t.id", args).fetchall()

    def tx(self, tid):
        return self.con.execute("SELECT * FROM transactions WHERE id=?", (tid,)).fetchone()

    def add_tx(self, pid, ts, direction, currency, amount, description=""):
        cur = self.con.execute(
            "INSERT INTO transactions(person_id,ts,direction,currency,amount,description,created_at,uid,m,dirty)"
            " VALUES(?,?,?,?,?,?,?,?,?,1)", (pid, ts, direction, currency, amount, description.strip(), now(),
                                             new_uid(), self._m()))
        self.con.commit()
        self._changed()
        return cur.lastrowid

    def old_json(self, tid):
        """Kaydın şimdiki hali, geçmiş için JSON (ESITLEME_SPEC: hist.old)."""
        r = self.con.execute("SELECT t.*, p.uid puid, p.name pname FROM transactions t "
                             "LEFT JOIN persons p ON p.id=t.person_id WHERE t.id=?", (tid,)).fetchone()
        if not r:
            return None, None
        return r["uid"], json.dumps({"ts": r["ts"], "direction": r["direction"], "currency": r["currency"],
                                     "amount": float(r["amount"]), "description": r["description"] or "",
                                     "person": r["puid"] or "", "person_name": r["pname"] or ""},
                                    ensure_ascii=False)

    def _log(self, tid, action):
        tuid, old = self.old_json(tid)
        if old:
            self.con.execute("INSERT INTO history(tx_id,action,old_values,at,uid,m,dirty,tx_uid)"
                             " VALUES(?,?,?,?,?,?,1,?)", (tid, action, old, now(), new_uid(), self._m(), tuid))

    def update_tx(self, tid, pid, ts, direction, currency, amount, description=""):
        self._log(tid, "DEGISTIRILDI")
        self.con.execute(
            "UPDATE transactions SET person_id=?,ts=?,direction=?,currency=?,amount=?,description=?,updated_at=?,"
            "m=?,dirty=1 WHERE id=?", (pid, ts, direction, currency, amount, description.strip(), now(),
                                       self._m(), tid))
        self.con.commit()
        self._changed()

    def delete_tx(self, tid):
        self.archive("tx", tid)
        self._log(tid, "SILINDI")
        m = self._m()
        self._tomb_photos(tid, m)
        t = self.tx(tid)
        if t:
            self._tomb("tx", t["uid"], m)
        self.con.execute("DELETE FROM transactions WHERE id=?", (tid,))
        self.con.commit()
        self._changed()

    def history(self, tid):
        return self.con.execute(
            "SELECT * FROM history WHERE tx_id=? OR (tx_uid<>'' AND tx_uid=(SELECT uid FROM transactions "
            "WHERE id=?)) ORDER BY at, id", (tid, tid)).fetchall()

    # --- fotoğraflar -----------------------------------------------------
    def photos(self, tid):
        return self.con.execute("SELECT * FROM photos WHERE tx_id=? ORDER BY id", (tid,)).fetchall()

    def photo_path(self, row):
        return os.path.join(self.photo_dir, row["file"])

    def add_photo(self, tid, src_path):
        ext = os.path.splitext(src_path)[1].lower() or ".jpg"
        rel = os.path.join(str(tid), uuid.uuid4().hex + ext)
        dst = os.path.join(self.photo_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src_path, dst)
        size = os.path.getsize(dst)
        self.con.execute("INSERT INTO photos(tx_id,file,original_name,added_at,uid,m,dirty,mime,size,chunks,blobs_up)"
                         " VALUES(?,?,?,?,?,?,1,?,?,?,0)",
                         (tid, rel, os.path.basename(src_path), now(), new_uid(), self._m(),
                          mimetypes.guess_type("x" + ext)[0] or "", size, file_chunks(size)))
        self.con.commit()
        self._changed()

    def delete_photo(self, photo_id):
        r = self.con.execute("SELECT * FROM photos WHERE id=?", (photo_id,)).fetchone()
        if r:
            self.archive("docs", photo_id)
            self._remove_file(r)
            self._tomb("docs", r["uid"], self._m(), r["chunks"] if r["blobs_up"] else 0)
            self.con.execute("DELETE FROM photos WHERE id=?", (photo_id,))
            self.con.commit()
            self._changed()

    def _remove_photo_files(self, tid):
        """Kaydın klasöründe kalan dosyalar da arşive taşınır; yalnız boş klasör silinir."""
        d = os.path.join(self.photo_dir, str(tid))
        if not os.path.isdir(d):
            return
        for root, _dirs, files in os.walk(d):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), self.photo_dir)
                self._remove_file({"file": rel})
        shutil.rmtree(d, ignore_errors=True)

    # --- arşiv (v1.21: kalıcı silme yok) ------------------------------------
    @staticmethod
    def _row(r):
        return {k: r[k] for k in r.keys()} if r is not None else None

    def snapshot(self, tur, rid):
        """Silinmeden önceki tam hal (bağlı kayıtlarla): {'tur', 'person', 'tx': [{..., 'photos': [...]}], 'rem': [...]}."""
        con = self.con
        R = self._row
        if tur == "persons":
            p = con.execute("SELECT * FROM persons WHERE id=?", (rid,)).fetchone()
            if not p:
                return None
            txs = []
            for t in con.execute("SELECT * FROM transactions WHERE person_id=? ORDER BY id", (rid,)).fetchall():
                d = R(t)
                d["photos"] = [R(x) for x in con.execute("SELECT * FROM photos WHERE tx_id=?", (t["id"],))]
                txs.append(d)
            rems = [R(x) for x in con.execute("SELECT * FROM reminders WHERE person_id=?", (rid,))]
            return {"tur": tur, "person": R(p), "tx": txs, "rem": rems, "baslik": p["name"]}
        if tur == "tx":
            t = con.execute("SELECT t.*, p.uid puid, p.name pname FROM transactions t LEFT JOIN persons p "
                            "ON p.id=t.person_id WHERE t.id=?", (rid,)).fetchone()
            if not t:
                return None
            d = R(t)
            d["photos"] = [R(x) for x in con.execute("SELECT * FROM photos WHERE tx_id=?", (rid,))]
            return {"tur": tur, "tx": [d], "baslik": f"{t['pname'] or ''} · {t['ts'][:16]} · {t['amount']:g} {t['currency']}"}
        if tur == "rem":
            r = con.execute("SELECT r.*, p.uid puid, p.name pname FROM reminders r LEFT JOIN persons p "
                            "ON p.id=r.person_id WHERE r.id=?", (rid,)).fetchone()
            if not r:
                return None
            return {"tur": tur, "rem": [R(r)], "baslik": f"{r['pname'] or ''} · {r['due'][:16]} · {r['note'] or ''}"}
        if tur == "docs":
            ph = con.execute("SELECT f.*, t.uid tuid FROM photos f LEFT JOIN transactions t ON t.id=f.tx_id "
                             "WHERE f.id=?", (rid,)).fetchone()
            if not ph:
                return None
            return {"tur": tur, "photos": [R(ph)], "baslik": ph["original_name"] or os.path.basename(ph["file"])}
        return None

    def archive(self, tur, rid, kaynak="yerel"):
        """Satır silinmeden önce çağrılır (commit etmez)."""
        snap = self.snapshot(tur, rid)
        if not snap:
            return None
        uid = (snap.get("person") or (snap.get("tx") or snap.get("rem") or snap.get("photos") or [{}])[0]).get("uid")
        cur = self.con.execute("INSERT INTO arsiv(at,kaynak,tur,uid,baslik,veri) VALUES(?,?,?,?,?,?)",
                               (now(), kaynak, tur, uid, str(snap.get("baslik") or "")[:200],
                                json.dumps(snap, ensure_ascii=False, default=str)))
        return cur.lastrowid

    def archived(self, limit=200):
        return self.con.execute("SELECT * FROM arsiv WHERE geri=0 ORDER BY id DESC LIMIT ?", (limit,)).fetchall()

    def save_conflict(self, tur, uid, row):
        self.con.execute("INSERT INTO cakisma(at,tur,uid,veri) VALUES(?,?,?,?)",
                         (now(), tur, uid, json.dumps(self._row(row) if not isinstance(row, dict) else row,
                                                      ensure_ascii=False, default=str)))

    def conflicts(self):
        return self.con.execute("SELECT * FROM cakisma ORDER BY id DESC").fetchall()

    def _restore_file(self, ph):
        arc = os.path.join(self.photo_dir, "arsiv", ph["file"])
        dst = os.path.join(self.photo_dir, ph["file"])
        if os.path.isfile(arc) and not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.replace(arc, dst)

    def restore(self, aid):
        """Arşivdeki kaydı geri koyar (aynı kimlikle, yeni değişiklik zamanıyla → diğer cihazlara da geri gelir)."""
        a = self.con.execute("SELECT * FROM arsiv WHERE id=?", (aid,)).fetchone()
        if not a or a["geri"]:
            return False
        snap = json.loads(a["veri"])
        con, m = self.con, self._m()
        SKIP = ("id", "puid", "pname", "tuid", "photos", "person_name")

        def ins(table, row, **over):
            row = {k: v for k, v in row.items() if k not in SKIP}
            row.update(over)
            row.update({"m": m, "dirty": 1})
            ex = con.execute(f"SELECT id FROM {table} WHERE uid=?", (row.get("uid"),)).fetchone()
            if ex:
                return ex[0]
            cols = [r[1] for r in con.execute(f"PRAGMA table_info({table})")]
            row = {k: v for k, v in row.items() if k in cols}
            cur = con.execute(f"INSERT INTO {table}({','.join(row)}) VALUES({','.join('?' * len(row))})", list(row.values()))
            con.execute("DELETE FROM tombstones WHERE uid=?", (row.get("uid"),))
            return cur.lastrowid

        def pid_of(uid):
            r = con.execute("SELECT id FROM persons WHERE uid=?", (uid,)).fetchone() if uid else None
            return r[0] if r else None

        def tid_of(uid):
            r = con.execute("SELECT id FROM transactions WHERE uid=?", (uid,)).fetchone() if uid else None
            return r[0] if r else None

        def put_tx(t, pid):
            if pid is None:
                return None
            tid = ins("transactions", t, person_id=pid)
            for ph in t.get("photos") or []:
                newfile = os.path.join(str(tid), os.path.basename(ph["file"]))
                self._restore_file(ph)
                src = os.path.join(self.photo_dir, ph["file"])
                dst = os.path.join(self.photo_dir, newfile)
                if os.path.isfile(src) and src != dst:
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    os.replace(src, dst)
                ins("photos", ph, tx_id=tid, file=newfile, blobs_up=0)
            return tid
        try:
            if snap["tur"] == "persons":
                pid = ins("persons", snap["person"])
                for t in snap.get("tx") or []:
                    put_tx(t, pid)
                for r in snap.get("rem") or []:
                    ins("reminders", r, person_id=pid)
            elif snap["tur"] == "tx":
                t = snap["tx"][0]
                pid = pid_of(t.get("puid"))
                if pid is None:
                    return False
                put_tx(t, pid)
            elif snap["tur"] == "rem":
                r = snap["rem"][0]
                pid = pid_of(r.get("puid"))
                if pid is None:
                    return False
                ins("reminders", r, person_id=pid)
            elif snap["tur"] == "docs":
                ph = snap["photos"][0]
                tid = tid_of(ph.get("tuid"))
                if tid is None:
                    return False
                self._restore_file(ph)
                ins("photos", ph, tx_id=tid, blobs_up=0)
            con.execute("UPDATE arsiv SET geri=1 WHERE id=?", (aid,))
            con.commit()
        except Exception:
            con.rollback()
            raise
        self._changed()
        return True

    # --- hatırlatıcılar ----------------------------------------------------
    # TAHSIL: kişiden alınacak (tahsil edilecek), ODEME: kişiye verilecek (ödenecek)
    def reminders(self, pid=None, pending_only=True, until=None):
        q = "SELECT r.*, p.name person_name FROM reminders r JOIN persons p ON p.id=r.person_id WHERE 1=1"
        args = []
        if pid is not None:
            q += " AND r.person_id=?"
            args.append(pid)
        if pending_only:
            q += " AND r.done=0"
        if until:
            q += " AND r.due<=?"
            args.append(until)
        return self.con.execute(q + " ORDER BY r.done, r.due, r.id", args).fetchall()

    def reminder(self, rid):
        return self.con.execute("SELECT * FROM reminders WHERE id=?", (rid,)).fetchone()

    def add_reminder(self, pid, kind, currency, amount, due, note=""):
        cur = self.con.execute(
            "INSERT INTO reminders(person_id,kind,currency,amount,due,note,created_at,uid,m,dirty)"
            " VALUES(?,?,?,?,?,?,?,?,?,1)", (pid, kind, currency, amount, due, note.strip(), now(), new_uid(),
                                             self._m()))
        self.con.commit()
        self._changed()
        return cur.lastrowid

    def update_reminder(self, rid, pid, kind, currency, amount, due, note=""):
        self.con.execute("UPDATE reminders SET person_id=?,kind=?,currency=?,amount=?,due=?,note=?,m=?,dirty=1"
                         " WHERE id=?", (pid, kind, currency, amount, due, note.strip(), self._m(), rid))
        self.con.commit()
        self._changed()

    def set_reminder_done(self, rid, done=True):
        self.con.execute("UPDATE reminders SET done=?,m=?,dirty=1 WHERE id=?", (1 if done else 0, self._m(), rid))
        self.con.commit()
        self._changed()

    def delete_reminder(self, rid):
        r = self.reminder(rid)
        if r:
            self.archive("rem", rid)
            self._tomb("rem", r["uid"], self._m())
        self.con.execute("DELETE FROM reminders WHERE id=?", (rid,))
        self.con.commit()
        self._changed()

    def pending_changes(self):
        """Buluta henüz gönderilmemiş değişiklik sayısı."""
        n = sum(self.con.execute(f"SELECT COUNT(*) FROM {t} WHERE dirty=1").fetchone()[0] for t in SYNC_TABLES)
        return n + self.con.execute("SELECT COUNT(*) FROM tombstones WHERE dirty=1").fetchone()[0]

    # --- yedek -----------------------------------------------------------
    def backup(self, zip_path):
        import zipfile
        tmp = os.path.join(self.dir, "_yedek_tmp.db")
        bk = sqlite3.connect(tmp)
        self.con.backup(bk)
        bk.close()
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(tmp, "veriler.db")
            for root, _, files in os.walk(self.photo_dir):
                for f in files:
                    full = os.path.join(root, f)
                    z.write(full, os.path.relpath(full, self.dir))
        os.remove(tmp)
