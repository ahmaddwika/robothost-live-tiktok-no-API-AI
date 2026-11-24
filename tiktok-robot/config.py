# ==========================================================
#  KONFIGURASI ROBOT HOST LIVE TIKTOK
#  Ubah bagian ini sesuai kebutuhanmu
# ==========================================================

# --- Akun TikTok yang sedang LIVE ---
# Tulis username TANPA tanda @
# PENTING: isi username HANYA kalau mau真的 live.
# Kalau HUBUNGKAN_LIVE = False, robot TIDAK konek ke TikTok sama sekali
# (aman untuk test lokal).
TIKTOK_USERNAME = "username_kamu"

# --- Mode test (aman, tidak menyentuh live TikTok) ---
# False = robot konek ke live sungguhan (butuh akun sedang LIVE)
# True  = hanya jalankan server + panel test di browser, TANPA konek TikTok
HUBUNGKAN_LIVE = False

# --- Suara Robot (Edge-TTS) ---
# Pilihan suara bahasa Indonesia:
#   id-ID-ArdiNeural   -> pria (robot cowok)
#   id-ID-GadisNeural  -> wanita (robot cewek)
VOICE = "id-ID-ArdiNeural"

# Kecepatan bicara. 0 = normal. Contoh: 10 lebih cepat, -10 lebih lambat
VOICE_RATE = "+5%"

# Nada suara. Contoh: +2 lebih tinggi (robot), -2 lebih berat
VOICE_PITCH = "+2Hz"

# Volume suara. +0% normal, bisa juga +10%, -10%
VOICE_VOLUME = "+0%"

# --- Emosi Suara (SSML) ---
# Aktifkan gaya bicara emosional (server Microsoft mendukung style).
GUNAKAN_SSML = True

# Gaya emosi tiap situasi (style Edge-TTS):
#   cheerful, friendly, excited, empathetic, sad, angry, calm, ...
GAYA_SAPAAN   = "cheerful"     # saat menyapa penonton
GAYA_CHAT     = "friendly"     # saat menjawab chat biasa
GAYA_GOMBALAN = "cheerful"     # saat menggombal
GAYA_DOA      = "empathetic"   # saat mendoakan
GAYA_ULTah    = "excited"      # saat ucapan ulang tahun
GAYA_TERIMA   = "friendly"     # saat terima kasih gift biasa
GAYA_KHODAM   = "excited"      # saat cek khodam

# --- Perilaku Robot ---
# Robot hanya menjawab chat/pertanyaan yang COCOK dengan pola di otak.py.
# Chat yang tidak dikenali TIDAK dijawab (mencegah tubrukan/ribut).
HANYA_JAWAB_YANG_COCOK = True

# Kalau tidak ada chat yang cocok, robot mengucapkan sapaan berkala
SAPAAN_BERKALA = True
JEDA_SAPAAN_BERKALA = 45   # detik

# Roboto jawab SEMUA chat atau hanya sebagian?
# Kalau True, hanya chat yang diawali "!" yang dibalas (biar tidak ribut)
CHAT_HANYA_JIKA_DIAWALI = False
PREFIX_CHAT = ""

# Jeda minimal antar ucapan (detik) supaya suara tidak tabrakan
JEDA_ANTAR_UCAPAN = 0.5

# Berapa lama robot dianggap "sibuk" saat sedang bicara
# (mencegah tumpang tindih suara)
MAKS_ANTRIAN = 3

# --- Fitur ---
FITUR_SAPA_PENONTON = True      # Sapa penonton yang baru masuk
FITUR_BACA_CHAT     = True      # Baca & balas chat
FITUR_GIFT_MAWAR    = True      # Ucapan terima kasih untuk gift mawar
FITUR_JOIN_CLUB     = True      # Cek khodam untuk Join Club / member baru

# --- Interaksi Gift Berjenjang (berdasarkan jumlah koin/diamond) ---
# Threshold jumlah koin untuk pindah tingkat ucapan
KOIN_GOMBALAN     = 3    # >= 3 koin  -> gombalan (ganteng/cantik)
KOIN_DOA          = 10   # >= 10 koin -> doa
KOIN_ULANG_TAHUN  = 50   # >= 50 koin -> ucapan ulang tahun

# Balas semua chat dengan komentar ringan? (kalau bukan pertanyaan)
BALAS_SEMUA_CHAT = True

# --- Otak: Gemini AI (opsional, untuk jawaban lebih pintar) ---
# Isi API key dari https://aistudio.google.com/ (gratis)
GUNAKAN_GEMINI  = False
GEMINI_API_KEY  = ""
GEMINI_MODEL    = "gemini-1.5-flash"

# --- Nama Gift untuk "Join Club" ---
# Nama gift yang memicu fitur cek khodam (cocokkan dengan nama gift TikTok)
# Contoh: "Join Club", "Membership", "Subscribe"
GIFT_JOIN_CLUB = ["Join Club", "Membership", "Member", "Subscribe"]

# --- Nama Gift "mawar" ---
# Cocokkan dengan nama gift di TikTok. Beberapa kemungkinan:
GIFT_MAWAR = ["Rose", "Mawar", "rose", "mawar", "Flower"]

# Kata imbuhan setelah ucapan terima kasih mawar (dipilih acak)
IMBUHAN_MAWAR = [
    "kamu baik banget!",
    "semoga rezekimu lancar ya!",
    "makasih banyak ya cantik.",
    "kamu luar biasa!",
    "terus dukung aku ya!",
    "semoga harimu menyenangkan!",
    "kamu memang penonton setia.",
]

# --- Nama robot (dipakai di sapaan) ---
NAMA_ROBOT = "Robo"
