# ==========================================================
#  SERVER AVATAR (TAHAP 2)
#  Menyajikan halaman avatar untuk OBS Browser Source
#  sekaligus menyimpan status robot (sedang bicara / subtitle).
# ==========================================================

import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
AVATAR_DIR = os.path.join(BASE_DIR, "avatar")
os.makedirs(AVATAR_DIR, exist_ok=True)

PORT = 8765

# --- Status global robot (dibaca avatar di browser) ---
_state = {
    "speaking": False,
    "text": "",
    "audio": "",      # nama file audio yang sedang diputar (di folder audio/)
    "token": 0,       # penanda ucapan unik (anti ganda)
    "effect": "",     # efek visual: birthday, doa, ...
    "mood": "idle",   # idle | talk | happy
    "gesture": "",    # gestur lengan: wave | point | hand
    "gestureSide": "right",  # left | right
    "gestureToken": 0,       # penanda gestur unik (anti ganda)
    "ts": 0,
}
_lock = threading.Lock()

# Handler untuk pemicu dari panel test di browser
_trigger_handler = None

# Referensi global ke objek server (agar tidak di-GC -> socket tetap hidup)
_httpd = None


def set_trigger_handler(fn):
    """Daftarkan fungsi(tipe, user, isi)->teks untuk test dari browser."""
    global _trigger_handler
    _trigger_handler = fn


def set_state(**kwargs):
    with _lock:
        _state.update(kwargs)


def get_state():
    with _lock:
        return dict(_state)


def set_gesture(jenis, side="right"):
    """Kirim gestur lengan ke avatar (wave | point | hand)."""
    with _lock:
        _state["gesture"] = jenis
        _state["gestureSide"] = side
        _state["gestureToken"] = _state.get("gestureToken", 0) + 1


_CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".mp3": "audio/mpeg",
}


def _serve_file(handler, path):
    full = os.path.normpath(os.path.join(WEB_DIR, path))
    if not full.startswith(WEB_DIR):
        handler.send_error(403)
        return
    if not os.path.isfile(full):
        handler.send_error(404)
        return
    ext = os.path.splitext(full)[1].lower()
    ctype = _CONTENT_TYPES.get(ext, "application/octet-stream")
    with open(full, "rb") as f:
        data = f.read()
    handler.send_response(200)
    handler.send_header("Content-Type", ctype)
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(data)


def _serve_audio(handler, path):
    full = os.path.normpath(os.path.join(BASE_DIR, path))
    if not full.startswith(os.path.join(BASE_DIR, "audio")):
        handler.send_error(403)
        return
    if not os.path.isfile(full):
        handler.send_error(404)
        return
    with open(full, "rb") as f:
        data = f.read()
    handler.send_response(200)
    handler.send_header("Content-Type", "audio/mpeg")
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(data)


def _daftar_vrm() -> list:
    """Daftar file .vrm/.glb/.gltf di folder avatar/."""
    try:
        files = [f for f in os.listdir(AVATAR_DIR) if f.lower().endswith((".vrm", ".glb", ".gltf"))]
        # Prioritaskan selain seedsan jika ada
        files.sort(key=lambda x: (0 if 'seed' in x.lower() and len(files) > 1 else 1, x.lower()))
        return files
    except Exception:
        return []


def _ada_vrm() -> bool:
    return len(_daftar_vrm()) > 0


def _serve_vrm(handler, nama: str):
    """Serve file .vrm/.glb/.gltf dari folder avatar/."""
    import urllib.parse
    nama = urllib.parse.unquote(nama)
    full = os.path.normpath(os.path.join(AVATAR_DIR, os.path.basename(nama)))
    if not os.path.isfile(full):
        handler.send_error(404)
        return
    ext = os.path.splitext(full)[1].lower()
    ctype = "application/octet-stream"
    if ext == ".glb":
        ctype = "model/gltf-binary"
    elif ext == ".gltf":
        ctype = "model/gltf+json"
    elif ext == ".vrm":
        ctype = "model/vrm"
    with open(full, "rb") as f:
        data = f.read()
    handler.send_response(200)
    handler.send_header("Content-Type", ctype)
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(data)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # matikan log akses biar bersih

    def _json(self, obj, code=200):
        import json
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        import json
        path = self.path.split("?", 1)[0]
        if path != "/trigger":
            self.send_error(404)
            return
        # Baca body
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {}

        tipe = payload.get("tipe", "chat")
        user = payload.get("user", "Penonton")
        isi = payload.get("isi", "")
        koin = payload.get("koin", 0)

        # Gestur lengan (wave/point/hand) -&gt; dikirim ke avatar lewat /state
        gestur = payload.get("gesture") or payload.get("gestur")
        if gestur:
            with _lock:
                _state["gesture"] = gestur
                _state["gestureSide"] = payload.get("side", "right")
                _state["gestureToken"] = _state.get("gestureToken", 0) + 1

        # Panggil handler yang didaftarkan (dari robot.py / test)
        if _trigger_handler is not None:
            try:
                teks = _trigger_handler(tipe, user, isi, koin)
            except TypeError:
                teks = _trigger_handler(tipe, user, isi)
            self._json({"ok": True, "text": teks})
        else:
            self._json({"ok": False, "text": "handler belum siap"}, 503)

    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path == "/" or path == "/avatar":
            # Halaman utama: pakai VRM kalau ada file .vrm, else SVG robot
            if _ada_vrm():
                _serve_file(self, "vrm.html")
            else:
                _serve_file(self, "avatar.html")
            return

        if path == "/vrm":
            _serve_file(self, "vrm.html")
            return

        if path == "/svg":
            _serve_file(self, "avatar.html")
            return

        if path == "/avatar/list":
            models = _daftar_vrm()
            import json
            data = json.dumps({"models": models}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)
            return

        if path.startswith("/avatar/"):
            nama = path[len("/avatar/"):]
            _serve_vrm(self, nama)
            return

        if path == "/state":
            import json
            data = json.dumps(get_state()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)
            return

        if path.startswith("/audio/"):
            _serve_audio(self, path.lstrip("/"))
            return

        _serve_file(self, path.lstrip("/"))


def start_server(port=PORT):
    # PENTING: httpd HARUS disimpan di referensi global, kalau tidak
    # objeknya di-GC Python dan socket-nya ikut tutup -> server mati
    # sendiri setelah beberapa detik (terlihat saat live jalan).
    global _httpd
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    httpd.daemon_threads = True
    _httpd = httpd
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


# ----------------------------------------------------------
#  HANDLER TEST MANDIRI (agar server bisa dites tanpa robot.py)
# ----------------------------------------------------------
_antrian_tes = None


def _worker_tes():
    from queue import Queue
    global _antrian_tes
    _antrian_tes = Queue()
    import suara
    while True:
        item = _antrian_tes.get()
        if item is None:
            break
        teks, gaya, effect = item
        try:
            suara.ucapkan(teks, gaya=gaya, effect=effect)
        except Exception as e:
            print("[WORKER TES]", e)


def _default_handler(tipe, user, isi, koin=0):
    import config
    import khodam
    import otak

    gaya = config.GAYA_CHAT
    effect = ""
    if tipe == "join":
        teks = f"{user} baru masuk. Halo, selamat datang!"
        gaya = config.GAYA_SAPAAN
    elif tipe == "chat":
        teks, gaya = otak.jawab_pertanyaan(isi, user)
        if not teks:
            # Chat tidak dikenali -> TIDAK dibalas (anti ribut), kecuali diizinkan
            if config.HANYA_JAWAB_YANG_COCOK:
                return ""
            teks = f"Halo {user}!"
    elif tipe == "mawar":
        import random
        teks = f"Wah {user}, terima kasih untuk mawarnya! " \
               f"{random.choice(config.IMBUHAN_MAWAR)}"
        gaya = config.GAYA_TERIMA
    elif tipe == "joinclub":
        teks = khodam.cek_khodam(user)
        gaya = config.GAYA_KHODAM
    elif tipe == "follow":
        teks = f"Terima kasih {user} sudah follow aku!"
        gaya = config.GAYA_TERIMA
        set_gesture("hand", "right")
    elif tipe == "share":
        teks = f"Terima kasih {user} sudah membagikan live ini!"
        gaya = config.GAYA_TERIMA
    elif tipe == "gift":
        teks, gaya, effect = otak.respon_gift(user, isi, koin)
        # Gestur ikut gift besar: makin mahal, makin rame gesturnya
        if koin >= config.KOIN_ULANG_TAHUN:
            set_gesture("wave", "left")
        elif koin >= config.KOIN_DOA:
            set_gesture("hand", "right")
        elif koin >= config.KOIN_GOMBALAN:
            set_gesture("point", "right")
    else:
        teks = f"Terima kasih {user}!"

    # Masukkan ke antrian (diproses berurutan, tidak tumpang tindih)
    if _antrian_tes is not None and teks:
        _antrian_tes.put((teks, gaya, effect))
    return teks


if __name__ == "__main__":
    import config
    import suara
    suara.set_server(sys.modules[__name__])
    set_trigger_handler(_default_handler)
    threading.Thread(target=_worker_tes, daemon=True).start()
    print(f"Server avatar berjalan di http://127.0.0.1:{PORT}/")
    print("Buka URL di atas, klik 'Aktifkan Suara', pakai Panel Test.")
    srv = start_server()
    # Buat suara pembuka (opening.mp3)
    import asyncio  # noqa: F401
    try:
        import edge_tts
        asyncio.run(edge_tts.Communicate(
            "Sistem aktif, halo aku Robo!", config.VOICE
        ).save(os.path.join(suara.AUDIO_DIR, "opening.mp3")))
    except Exception as e:
        print("opening gagal:", e)
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        srv.shutdown()
