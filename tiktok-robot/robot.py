# ==========================================================
#  ROBOT HOST LIVE TIKTOK
#  Menangkap chat & gift dari live TikTok lalu robot merespon
#  dengan suara (Edge-TTS) + avatar bergerak di OBS.
#
#  Cara pakai:
#    1. Ubah TIKTOK_USERNAME di config.py
#    2. Jalankan:  python robot.py
# ==========================================================

import random
import threading
import time
from queue import Queue

from TikTokLive import TikTokLiveClient
from TikTokLive.events import (
    ConnectEvent,
    DisconnectEvent,
    CommentEvent,
    GiftEvent,
    JoinEvent,
    FollowEvent,
    ShareEvent,
)

import config
import khodam
import otak
import server
import suara

# ----------------------------------------------------------
#  SISTEM ANTRIAN SUARA
# ----------------------------------------------------------
_antrian = Queue()
_terakhir_ucap = 0.0  # waktu ucapan terakhir (untuk sapaan berkala)


def _worker_suara():
    """Proses antrian ucapan satu per satu (anti tubrukan)."""
    global _terakhir_ucap
    while True:
        item = _antrian.get()
        if item is None:
            break
        teks, gaya, effect = item
        try:
            suara.ucapkan(teks, gaya=gaya, effect=effect)
        except Exception as e:
            print(f"[WORKER ERROR] {e}")
        finally:
            _terakhir_ucap = time.time()
        _antrian.task_done()


def katakan(teks: str, gaya: str = "", effect: str = ""):
    """Masukkan ucapan ke antrian."""
    if not teks or not teks.strip():
        return
    print(f"[ROBOT] {teks}")
    if _antrian.qsize() < config.MAKS_ANTRIAN:
        _antrian.put((teks, gaya, effect))
    else:
        print("[ROBOT] (antrian penuh, dilewat)")


# ----------------------------------------------------------
#  LOGIKA RESPON -> (teks, gaya)
# ----------------------------------------------------------
def _cocok(nama_gift: str, daftar: list) -> bool:
    nama_gift = (nama_gift or "").lower()
    return any(g.lower() in nama_gift for g in daftar)


def _is_join_club(nama_gift: str) -> bool:
    return _cocok(nama_gift, config.GIFT_JOIN_CLUB)


def respon(tipe: str, user: str, isi: str = "", koin: int = 0):
    """Kembalikan (teks, gaya, effect) untuk sebuah kejadian."""
    if tipe == "join":
        if config.FITUR_SAPA_PENONTON:
            return f"{user} baru masuk. Halo, selamat datang!", config.GAYA_SAPAAN, ""
        return "", "", ""

    if tipe == "chat":
        if not config.FITUR_BACA_CHAT:
            return "", "", ""
        teks, gaya = otak.jawab_pertanyaan(isi, user)
        return teks, gaya, ""

    if tipe == "follow":
        return f"Terima kasih {user} sudah follow aku!", config.GAYA_TERIMA, ""

    if tipe == "share":
        return f"Terima kasih {user} sudah membagikan live ini!", config.GAYA_TERIMA, ""

    if tipe == "joinclub":
        if config.FITUR_JOIN_CLUB:
            return khodam.cek_khodam(user), config.GAYA_KHODAM, ""
        return "", "", ""

    if tipe == "gift":
        # Mawar dengan koin kecil -> terima kasih + imbuhan.
        # Mawar dengan koin besar -> ikut jenjang tier (gombalan/doa/ultah).
        if (config.FITUR_GIFT_MAWAR and _cocok(isi, config.GIFT_MAWAR)
                and koin < config.KOIN_GOMBALAN):
            imbuhan = random.choice(config.IMBUHAN_MAWAR)
            return f"Wah {user}, terima kasih untuk mawarnya! {imbuhan}", config.GAYA_TERIMA, ""
        return otak.respon_gift(user, isi, koin)

    return "", "", ""


# ----------------------------------------------------------
#  SAPAAN BERKALA (saat tidak ada chat yang cocok)
# ----------------------------------------------------------
SAPAAN_RUTIN = [
    "Halo kawan, yang sudah mampir jangan lupa tinggalin komentar ya!",
    "Ada yang mau ngobrol? Tulis di komentar, aku baca semuanya!",
    "Terima kasih yang sudah dukung live ini. Aku tunggu kamu terus ya!",
    "Jangan lupa follow biar tidak ketinggalan live seru berikutnya!",
]


def _loop_sapaan():
    """Kalau cukup lama sepi, robot menyapa berkala."""
    while True:
        time.sleep(5)
        if not config.SAPAAN_BERKALA:
            continue
        sepi = (time.time() - _terakhir_ucap) >= config.JEDA_SAPAAN_BERKALA
        if sepi and _antrian.qsize() == 0:
            katakan(random.choice(SAPAAN_RUTIN), config.GAYA_SAPAAN)


# ----------------------------------------------------------
#  CLIENT TIKTOK
# ----------------------------------------------------------
class _ClientDummy:
    """Dipakai saat mode test: dekorator .on() jadi no-op,
    jadi TIDAK ada koneksi ke live TikTok sama sekali."""

    def on(self, _event):
        def deco(fn):
            return fn
        return deco


# Hanya dibuat kalau HUBUNGKAN_LIVE = True, supaya mode test
# tidak pernah menyentuh koneksi live TikTok sama sekali.
if config.HUBUNGKAN_LIVE:
    client = TikTokLiveClient(unique_id="@" + config.TIKTOK_USERNAME)
else:
    client = _ClientDummy()


@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"[+] Terhubung ke live @{config.TIKTOK_USERNAME}")
    katakan(f"Halo semuanya! Aku {config.NAMA_ROBOT}, host live hari ini. "
            f"Selamat datang di live kita!", config.GAYA_SAPAAN)


@client.on(DisconnectEvent)
async def on_disconnect(event: DisconnectEvent):
    print("[-] Terputus dari live.")


@client.on(JoinEvent)
async def on_join(event: JoinEvent):
    user = event.user.nickname or event.user.unique_id
    teks, gaya, effect = respon("join", user)
    katakan(teks, gaya, effect)


@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    user = event.user.nickname or event.user.unique_id
    teks, gaya, effect = respon("follow", user)
    katakan(teks, gaya, effect)


@client.on(ShareEvent)
async def on_share(event: ShareEvent):
    user = event.user.nickname or event.user.unique_id
    teks, gaya, effect = respon("share", user)
    katakan(teks, gaya, effect)


@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    user = event.user.nickname or event.user.unique_id
    pesan = event.comment
    if config.CHAT_HANYA_JIKA_DIAWALI:
        if not pesan.startswith(config.PREFIX_CHAT):
            return
        pesan = pesan[len(config.PREFIX_CHAT):].strip()
    teks, gaya, effect = respon("chat", user, pesan)
    katakan(teks, gaya, effect)


@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    nama_gift = getattr(event.gift, "name", "")
    user = event.user.nickname or event.user.unique_id
    koin = getattr(event.gift, "diamond_count", 0) or 0
    repeat = getattr(event, "repeat_count", 1) or 1
    total_koin = koin * repeat

    if config.FITUR_JOIN_CLUB and _is_join_club(nama_gift):
        teks, gaya, effect = respon("joinclub", user)
        katakan(teks, gaya, effect)
        return

    teks, gaya, effect = respon("gift", user, nama_gift, total_koin)
    katakan(teks, gaya, effect)


# ----------------------------------------------------------
#  MAIN
# ----------------------------------------------------------
def main():
    print("=" * 55)
    print(f"  ROBOT HOST LIVE TIKTOK - {config.NAMA_ROBOT}")
    print("=" * 55)
    if config.HUBUNGKAN_LIVE:
        print(f"  Target live : @{config.TIKTOK_USERNAME}")
    else:
        print("  MODE TEST   : TIDAK konek ke TikTok (HUBUNGKAN_LIVE = False)")
        print("                -> pakai panel test di browser untuk mencoba")
    print(f"  Suara       : {config.VOICE} (emosi {'ON' if config.GUNAKAN_SSML else 'OFF'})")
    print("-" * 55)

    server.start_server()
    suara.set_server(server)
    server.set_trigger_handler(lambda t, u, i, k=0: _trigger_live(t, u, i, k))
    print(f"  Avatar      : http://127.0.0.1:{server.PORT}/  (OBS)")
    print("-" * 55)

    threading.Thread(target=_worker_suara, daemon=True).start()
    if config.HUBUNGKAN_LIVE:
        threading.Thread(target=_loop_sapaan, daemon=True).start()

    katakan(f"Sistem siap. Aku {config.NAMA_ROBOT}, siap menemani live kamu.",
            config.GAYA_SAPAAN)

    if not config.HUBUNGKAN_LIVE:
        print("\n[TEST] Server jalan. Buka http://127.0.0.1:8765/ di browser,")
        print("[TEST] klik 'Aktifkan Suara', lalu pakai panel test.")
        print("[TEST] Tekan Ctrl+C untuk berhenti.\n")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[!] Dihentikan oleh user.")
        finally:
            _antrian.put(None)
        return

    try:
        client.run()
    except KeyboardInterrupt:
        print("\n[!] Dihentikan oleh user.")
    except Exception as e:
        print(f"[ERROR] {e}")
        print("\nCek: pastikan username benar & akun sedang LIVE.")
    finally:
        _antrian.put(None)


def _trigger_live(tipe, user, isi, koin=0):
    """Dipanggil panel test di browser."""
    teks, gaya, effect = respon(tipe, user, isi, koin)
    if teks:
        katakan(teks, gaya, effect)
    return teks


if __name__ == "__main__":
    main()
