# ==========================================================
#  FITUR CEK KHODAM (VERSI KOCOK)
#  Dipakai saat ada gift "Join Club" / member baru
# ==========================================================

import random

# Khodam absurd & lucu. Tambah sesuai selera.
KHODAM_LIST = [
    ("Macan Putih", "galak tapi jago masak rendang"),
    ("Naga Hijau", "suka nge-game sampai subuh"),
    ("Kucing Sakti", "hobinya rebahan tapi rezeki lancar"),
    ("Garuda Emas", "kalau ngopi gak pake gula"),
    ("Elang Hitam", "jago nyanyi tapi sumbang"),
    ("Harimau Tembok", "takut ketinggian tapi hobi bolos"),
    ("Biawak Sakti", "suka jajan seblak level 10"),
    ("Kadal Naga", "penyayang tapi galak kalau lapar"),
    ("Ayam Jago Sakti", "bangunnya jam 12 siang"),
    ("Ikan Mas Ajaib", "hobinya foto pakai filter lucu"),
    ("Kelelawar Gaib", "suka nonton drakor sampai nangis"),
    ("Cicak Terbang", "doanya cepet dikabul tapi ngeselin"),
    ("Semut Raksasa", "rajin banget tapi pelit traktir"),
    ("Tuyul Baik Hati", "dulu jahat sekarang tobat"),
    ("Genderuwo Ramah", "suka bagi-bagi takjil"),
    ("Pocong Rajin", "langganan telat tapi kerja keras"),
    ("Kuntilanak Baik", "rambutnya wangi conditioner"),
    ("Jin Botol", "kalau dipanggil malah minta makan"),
    ("Naga Bonar", "jago debat tapi lupa jawaban"),
    ("Dewa Petir", "suka matikan lampu pas lagi kencan"),
    ("Raja Iblis Kasihan", "hatinya lembut dong"),
    ("Malaikat Pelindung", "tapi mood-nya suka drama"),
    ("Kucing Oyen Gaib", "berani banget ngerebut nasi"),
    ("Babi Ngepet Jadi", "sadis tapi sekarang bertaubat"),
    ("Sapi Terbang", "bunyi ngibrit doang kerjanya"),
    ("Kambing Sakti", "kepalanya keras tapi hatinya lembut"),
    ("Monyet Gaib", "rajin manjat tapi takut jatuh"),
    ("Buaya Putih", "janjinya manis tapi nggak ditepatin"),
    ("Ular Naga", "suka gaya kalau difoto"),
    ("Penyu Sakti", "lambat tapi pasti sampai"),
    ("Bebek Gaib", "bunyinya wkwkwk terus"),
    ("Ubur-ubur Sakti", "bikin keset tiap lewat"),
    ("Kepiting Lucu", "jalan miring tapi doanya lurus"),
    ("Siput Super", "pelan tapi disayang ibu"),
    ("Tikus Berdasi", "kerjanya rajin tapi suka ngendap"),
]

# Kalimat penutup komedi
PENUTUP = [
    "Sumpah ini khodam langka, jangan dilepas!",
    "Khodam elit banget, kalau difoto bisa muncul katanya.",
    "Hoki kamu hari ini kayaknya naga bunyi nih!",
    "Awas, khodam ini kalau ngambek susah dipanggil lagi.",
    "Cieeee punya khodam keren, jangan sombong ya!",
    "Khodam ini kayaknya lagi capek cari rezeki buat kamu.",
    "Kalau kamu menang undian, ingat-ingat aku ya!",
    "Khodam ini asli gak boong, hasil ramalan robot.",
]

# React lucu saat khodam disebut
REACT = [
    "Waduh...",
    "Ehem ehem...",
    "Tunggu sebentar, aku terawang dulu...",
    "Aku buka mata bathinku ya...",
]


def cek_khodam(username: str) -> str:
    """Kembalikan kalimat hasil cek khodam kocak untuk username."""
    khodam, sifat = random.choice(KHODAM_LIST)
    penutup = random.choice(PENUTUP)
    react = random.choice(REACT)
    return (
        f"{react} {username}, khodam kamu adalah {khodam}, {sifat}. {penutup}"
    )
