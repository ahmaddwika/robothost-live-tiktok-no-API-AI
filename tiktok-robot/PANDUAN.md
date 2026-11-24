# Robot Host Live TikTok

Robot host live TikTok interaktif: menyapa penonton, membaca chat, merespon gift mawar,
dan cek khodam untuk Join Club. Suara memakai Edge-TTS (bahasa Indonesia).

## 1. Persyaratan
- Windows dengan Python 3.13 (sudah terpasang)
- Koneksi internet (untuk TTS)
- Akun TikTok yang sedang LIVE
- Software streaming: **OBS Studio** (gratis)

## 2. Konfigurasi
Buka `config.py`, ubah bagian penting:
- `TIKTOK_USERNAME` -> username TikTok TANPA tanda @
- `VOICE` -> `id-ID-ArdiNeural` (pria) atau `id-ID-GadisNeural` (wanita)
- `GIFT_MAWAR` -> samakan dengan nama gift mawar di TikTok
- `GIFT_JOIN_CLUB` -> samakan dengan nama gift Join Club

## 3. Menjalankan
Di folder `C:\tiktok-robot`:
```
python robot.py
```
Robot akan bicara "Sistem siap..." lalu mulai menyimak live.

Pastikan dulu akun sudah LIVE sebelum menjalankan.

## 4. Tampilan di OBS (penting!)
1. Buka OBS -> **Sources** -> **+** -> pilih **Browser**
2. centang **Local file**, isi URL: `http://127.0.0.1:8765/`
   - kalau pakai karakter 3D (VRM) -> otomatis pakai viewer 3D
   - kalau tanpa VRM -> otomatis pakai robot SVG
3. Ukuran: **1080 x 1920** (vertikal, buat TikTok) atau 1920x1080
4. Klik **Interact** di OBS -> klik "Aktifkan Suara" (WAJIB sekali,
   supaya browser boleh memutar audio)
5. Centang **"Shutdown source when not visible"** = OFF, **"Refresh browser when scene becomes active"** = ON

Tambahan: **Audio Output Capture** di OBS supaya suara robot masuk stream.
Atau pakai **VB-Audio Cable** untuk kualitas lebih bersih.

## 5. Fitur
| Fitur          | Pemicu            | Aksi robot                          |
|----------------|-------------------|-------------------------------------|
| Sapaan masuk   | Penonton join     | Menyapa & selamat datang            |
| Baca chat      | Komentar          | Menjawab pertanyaan yang dikenali   |
| Gift 1-2 koin  | Gift biasa        | Terima kasih                        |
| Gift 3-5 koin  | Gift sedang      | **Gombalan** (ganteng/cantik)       |
| Gift 10+ koin  | Gift besar        | **Doa** + efek partikel             |
| Gift 50+ koin  | Gift besar        | **Ucapan ultah** + mercon/konfeti   |
| Cek khodam     | Join Club/member  | Khodam kocak (acak)                 |
| Follow / Share | -                 | Ucapan terima kasih                 |
| Sapaan berkala | Live sepi 45 dtk | Robot menyapa sendiri               |

Gestur lengan otomatis ikut gift besar (3+ koin = tunjuk, 10+ = angkat tangan,
50+ = melambai). Untuk memicu manual, `POST /trigger` dengan body:
```json
{"tipe": "chat", "isi": "halo", "gesture": "wave", "side": "left"}
```
(`gesture`: `wave` | `point` | `hand`, `side`: `left` | `right`)

## 6. Mengubah khodam
Edit `khodam.py` -> `KHODAM_LIST`, `SIFAT_KHODAM`, `PENUTUP`, `REACT`.

## 7. Mengubah kata imbuhan mawar
Edit `IMBUHAN_MAWAR` di `config.py`.

## 8. Karakter 3D (VRM)
Taruh file `.vrm` di `C:\tiktok-robot\avatar\` -> restart -> otomatis dipakai.
Panduan lengkap (cara bikin/download karakter, troubleshooting):
lihat **PANDUAN-3D.md**.

## 9. Mengganti suara robot
`config.py` -> `VOICE`:
- `id-ID-ArdiNeural` (pria)
- `id-ID-GadisNeural` (wanita)

Gaya emosi diatur di `GAYA_SAPAAN`, `GAYA_GOMBALAN`, `GAYA_DOA`, dst.

## Catatan
- `TikTokLive` adalah library tidak resmi. Kadang TikTok mengubah sistemnya,
  jika library error, update dengan: `pip install -U TikTokLive`
- Jangan terlalu banyak ucapan bersamaan agar suara tidak tabrakan
  (diatur oleh `MAKS_ANTRIAN` di `config.py`).
- Robot HANYA menjawab chat yang cocok dengan pola di `otak.py`.
  Kalau tidak cocok -> tidak dijawab (anti ribut).
