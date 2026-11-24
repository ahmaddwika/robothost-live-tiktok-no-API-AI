# ==========================================================
#  MODE TEST / SIMULASI (TANPA LIVE)
#  Mensimulasikan chat & gift supaya bisa lihat reaksi robot
#  tanpa harus live TikTok.
#
#  Cara pakai:
#    1. Ubah SKENARIO di bawah sesuai keinginan
#    2. Jalankan:  python test_simulasi.py
# ==========================================================

import random
import threading
import time

import config
import khodam
import server
import suara

# ==========================================================
#  SKENARIO SIMULASI
#  Setiap baris = satu kejadian. Tipe: "join", "chat", "mawar",
#  "joinclub", "follow", "share", "gift"
# ==========================================================
SKENARIO = [
    ("join",     "Budi",            ""),
    ("chat",     "Siti",            "Halo robot, kamu siapa?"),
    ("mawar",    "Andi",            "Rose"),
    ("chat",     "Rina",            "Robotnya lucu banget!"),
    ("joinclub", "Dewi",            "Join Club"),
    ("follow",   "Eko",             ""),
    ("mawar",    "Fajar",           "Rose"),
    ("gift",     "Gita",            "Galaxy"),
    ("share",    "Hana",            ""),
    ("joinclub", "Indra",           "Join Club"),
]

# Jeda antar kejadian (detik)
JEDA = 2.0


# ----------------------------------------------------------
#  LOGIKA REAKSI (sama seperti di robot.py)
# ----------------------------------------------------------
def reaksi(tipe: str, user: str, isi: str) -> str:
    if tipe == "join":
        if config.FITUR_SAPA_PENONTON:
            return f"{user} baru masuk. Halo, selamat datang!"
        return ""

    if tipe == "chat":
        if config.FITUR_BACA_CHAT:
            return f"{user} berkata: {isi}. Oke, aku dengar ya!"
        return ""

    if tipe == "mawar":
        if config.FITUR_GIFT_MAWAR:
            imbuhan = random.choice(config.IMBUHAN_MAWAR)
            return f"Wah {user}, terima kasih untuk mawarnya! {imbuhan}"
        return ""

    if tipe == "joinclub":
        if config.FITUR_JOIN_CLUB:
            return khodam.cek_khodam(user)
        return ""

    if tipe == "follow":
        return f"Terima kasih {user} sudah follow aku!"

    if tipe == "share":
        return f"Terima kasih {user} sudah membagikan live ini!"

    if tipe == "gift":
        return f"Terima kasih {user} untuk {isi}!"

    return ""


def main():
    print("=" * 55)
    print("  MODE TEST / SIMULASI - TANPA LIVE")
    print("=" * 55)
    print(f"  Suara : {config.VOICE}")
    print(f"  Total kejadian: {len(SKENARIO)}")
    print("-" * 55)
    print(f"  Avatar: buka http://127.0.0.1:{server.PORT}/ di browser")
    print("  (biarkan terbuka, robot akan bicara & mulut bergerak)")
    print("-" * 55)

    server.start_server()
    suara.set_server(server)

    suara.ucapkan(f"Halo semuanya! Aku {config.NAMA_ROBOT}, host live hari ini.")

    for i, (tipe, user, isi) in enumerate(SKENARIO, 1):
        teks = reaksi(tipe, user, isi)
        if not teks:
            print(f"[{i}] ({tipe}) dilewat (fitur nonaktif)")
            continue
        print(f"[{i}] ({tipe}) -> {teks}")
        suara.ucapkan(teks)
        time.sleep(JEDA)

    print("-" * 55)
    print("  SIMULASI SELESAI.")
    print("=" * 55)


if __name__ == "__main__":
    main()
