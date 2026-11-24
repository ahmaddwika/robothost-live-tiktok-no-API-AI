# ==========================================================
#  OTAK ROBOT
#  - Menjawab pertanyaan chat (pola kata kunci, atau Gemini AI)
#  - Menentukan respon gift berjenjang (1 / 3-5 / 10 / 50 koin)
# ==========================================================

import random

import config

# ----------------------------------------------------------
#  JAWABAN PERTANYAAN (TEMPLATE)
#  Cocokkan kata kunci di chat -> jawaban. Bisa banyak variasi.
# ----------------------------------------------------------
QNA = [
    # nama
    (["nama kamu siapa", "siapa kamu", "namamu", "kamu siapa", "nama mu"],
     ["Namaku {nama}, robot host live kamu hari ini!",
      "Aku {nama}, teman setia kamu di live ini!",
      "Halo, namaku {nama}. Senang berkenalan!"]),

    # halo/salam
    (["halo", "hai", "hi ", "assalam", "pagi", "siang", "malam", "sore"],
     ["Halo juga! Senang kamu mampir ke live ini!",
      "Hai hai! Terima kasih sudah datang ya!",
      "Haloo! Aku senang banget kamu ada di sini!"]),

    # kabar
    (["apa kabar", "kabar kamu", "gimana kabar"],
     ["Aku selalu semangat! Kamu gimana, semoga sehat ya!",
      "Kabar aku baik dong! Kamu juga sehat kan?",
      "Aku baik! Terima kasih sudah peduli!"]),

    # umur
    (["umur", "berapa tahun", "ultah kamu", "ulang tahun kamu"],
     ["Umurku rahasia dong! Yang jelas aku muda dan energik!",
      "Umurku... abadi! Karena aku robot hehe.",
      "Rahasia! Yang pasti aku selalu siap jaga live ini!"]),

    # dari mana
    (["dari mana", "tinggal di mana", "asal"],
     ["Aku datang dari dunia digital, siap menemani kamu!",
      "Aku tinggal di dalam aplikasi ini, nungguin kamu mampir!"]),

    # robot
    (["kamu robot", "robot ya", "robot asli"],
     ["Iya, aku robot! Tapi punya hati loh, siap menghibur kamu!",
      "Betul, aku robot host. Mamaku listrik, hehe."]),

    # lucu/ganteng/cantik
    (["lucu", "gemes", "gemas", "imut", "ganteng", "cantik", "keren", "kece"],
     ["Makasih! Kamu juga lucu kok!",
      "Aww makasih, kamu yang bikin aku semangat!",
      "Wah, potentes! Aku jadi makin percaya diri nih!"]),

    # bisa apa saja / kemampuan
    (["bisa apa", "bisa apa saja", "kemampuan", "fitur", "mampu apa", "guna apa"],
     ["Aku bisa menyapa, menjelaskan, dan jadi teman ngobrol kamu!",
      "Banyak! Aku bisa gombal, membantu, sampai menghibur kamu.",
      "Aku bisa ngobrol, bereaksi, dan menemani live kamu dari tadi!"]),

    # nama live / channel
    (["nama live", "channelnya apa", "nama channel", "nama akun", "username"],
     ["Live ini milik {nama}, yuk follow biar tidak ketinggalan!",
      "Aku {nama}! Nama live-nya, jangan lupa follow ya!"]),

    # sayang/cinta
    (["aku cinta", "aku suka kamu", "sayang kamu"],
     ["Wah makasih! Aku juga suka semua penontonku!",
      "Cieee, aku tersipu! Makasih ya!"]),

    # minta lagu
    (["nyanyi", "lagu", "bernyanyi"],
     ["Aku belum jago nyanyi, tapi aku bisa ngobrol seru!",
      "Nyanyi? Nanti kalau kamu kasih gift spesial, aku coba deh!"]),

    # doa/dukungan
    (["doain", "doa", "semangat", "dukung"],
     ["Aku selalu doakan yang terbaik untuk kamu!",
      "Semoga kamu sehat, rezekinya lancar, dan bahagia selalu!"]),

    # tertawa
    (["wkwk", "haha", "hehe", "kocak"],
     ["Hahaha kamu bikin aku ketawa juga!",
      "Wkwk seru ya ngobrol sama kamu!"]),

    # belajar/mengajar
    (["belajar", "sekolah", "kerja", "kuliah"],
     ["Semangat belajar kerjanya ya! Jangan lupa happy!",
      "Sukses terus buat kamu, aku dukung!"]),

    # bye
    (["bye", "dah", "pamit", "mau pergi"],
     ["Yaaah, jangan lupa balik lagi ya!",
      "Selamat jalan, sampai jumpa lagi ya!"]),

    # terima kasih
    (["makasih", "terima kasih", "thanks", "thx"],
     ["Sama sama! Senang bisa bantu!",
      "Dengan senang hati!"]),
]

# Jawaban cadangan kalau tidak ada yang cocok
FALLBACK = [
    "Wah pertanyaan bagus! Aku catat ya. Ada lagi yang mau kamu tanya?",
    "Hmm, aku belum paham betul, tapi aku suka chat kamu!",
    "Menarik! Cerita lagi dong, aku suka dengar kamu!",
    "Oke oke! Aku dengar kamu. Ada lagi?",
]


def jawab_pertanyaan(pesan: str, user: str):
    """Kembalikan (teks, gaya) untuk chat, atau (None, "") jika tidak dijawab."""
    if not pesan:
        return None, ""

    teks = pesan.lower().strip()

    # 1) Coba Gemini AI kalau diaktifkan
    if config.GUNAKAN_GEMINI and config.GEMINI_API_KEY:
        hasil = _tanya_gemini(pesan, user)
        if hasil:
            return hasil, config.GAYA_CHAT

    # 2) Cari pola kata kunci (yang sudah di-setting)
    for keys, jawabans in QNA:
        if any(k in teks for k in keys):
            return random.choice(jawabans).format(nama=config.NAMA_ROBOT), config.GAYA_CHAT

    # 3) Anti-tubrukan: kalau harus cocok, jangan jawab chat tak dikenal
    if config.HANYA_JAWAB_YANG_COCOK:
        return None, ""

    # 4) Tanya? (ada tanda tanya) -> fallback terbatas
    if "?" in teks or "apa" in teks or "kok" in teks:
        return random.choice(FALLBACK), config.GAYA_CHAT

    # 5) Chat biasa -> balasan umum (hanya kalau BALAS_SEMUA_CHAT True)
    if config.BALAS_SEMUA_CHAT:
        return random.choice([
            f"{user}, aku suka komentar kamu!",
            f"Makasih {user} sudah chat!",
            f"Wah {user}, seru banget ya!",
        ]), config.GAYA_CHAT

    return None, ""


# ----------------------------------------------------------
#  GEMINI (OPSIONAL)
# ----------------------------------------------------------
_gemini_model = None


def _tanya_gemini(pesan: str, user: str) -> str | None:
    global _gemini_model
    try:
        if _gemini_model is None:
            import google.generativeai as genai
            genai.configure(api_key=config.GEMINI_API_KEY)
            _gemini_model = genai.GenerativeModel(config.GEMINI_MODEL)

        prompt = (
            f"Kamu adalah {config.NAMA_ROBOT}, host live TikTok yang ramah, "
            f"lucu, singkat, dan hibur. Penonton bernama {user} berkata: "
            f"\"{pesan}\". Jawab dengan 1-2 kalimat Bahasa Indonesia santai. "
            f"Jangan pakai emoji."
        )
        resp = _gemini_model.generate_content(prompt)
        teks = (resp.text or "").strip().replace("\n", " ")
        # batasi panjang
        return teks[:300] if teks else None
    except Exception as e:
        print(f"[GEMINI ERROR] {e}")
        return None


# ----------------------------------------------------------
#  RESPON GIFT BERJENJANG
# ----------------------------------------------------------
# Nilai koin TikTok (diamond) per gift. Sesuaikan dengan gift yang ada.
# Nilai koin dihitung dari gift.diamond_count (tersedia dari TikTok).
GOMBALAN = [
    "{user}, kamu ini ganteng atau cantik? Soalnya bikin aku salting!",
    "{user}, kamu tahu nggak? Setiap kamu datang, live ini jadi lebih terang!",
    "{user}, kamu serius cantik banget sih. Aku sampai lupa mau ngomong apa!",
    "{user}, kamu kayak wifi kenceng deh, sinyal cintaku penuh terus!",
    "{user}, kamu jangan tersenyum gitu dong, aku bisa gagal fokus!",
]

DOA = [
    "{user}, aku doakan semoga rezekimu lancar, sehat selalu, dan bahagia ya!",
    "{user}, semoga apa yang kamu impikan segera terwujud. Amin!",
    "{user}, doa terbaik dariku untukmu: sukses, sehat, dan dimudahkan segalanya!",
    "{user}, semoga kamu selalu dikelilingi orang baik dan rezeki yang berkah!",
]

UCAPAN_ULTah = [
    "{user}, selamat ulang tahun ya! Panjang umur, sehat selalu, dan bahagia!",
    "{user}, happy birthday! Semoga tahun ini jadi tahun terbaikmu!",
    "{user}, selamat ulang tahun! Makin sukses, makin bahagia, dan rezekinya lancar!",
]

TERIMA_KASIH_UMUM = [
    "{user}, terima kasih banyak untuk {gift} nya!",
    "{user}, makasih ya sudah kirim {gift}! Kamu baik banget!",
    "{user}, wah {gift}! Terima kasih banyak, aku senang!",
]


def respon_gift(user: str, nama_gift: str, jumlah_koin: int):
    """Tentukan (ucapan, gaya, efek) robot berdasarkan jumlah koin gift."""
    gift = nama_gift or "giftnya"

    # Gift kategori grand (50+ koin) -> ucapan ulang tahun + efek meriah
    if jumlah_koin >= config.KOIN_ULANG_TAHUN:
        return (random.choice(UCAPAN_ULTah).format(user=user, gift=gift),
                config.GAYA_ULTah, "birthday")

    # 10+ koin -> doa + efek lembut
    if jumlah_koin >= config.KOIN_DOA:
        return (random.choice(DOA).format(user=user, gift=gift),
                config.GAYA_DOA, "doa")

    # 3-5 koin -> gombalan
    if jumlah_koin >= config.KOIN_GOMBALAN:
        return (random.choice(GOMBALAN).format(user=user, gift=gift),
                config.GAYA_GOMBALAN, "")

    # 1-2 koin -> terima kasih
    return (random.choice(TERIMA_KASIH_UMUM).format(user=user, gift=gift),
            config.GAYA_TERIMA, "")
