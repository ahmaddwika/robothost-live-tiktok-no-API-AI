# Panduan Karakter 3D (VRM)

Sistem ini mendukung 2 jenis avatar:
- **VRM 3D** (jika ada file `.vrm` di folder `avatar/`) -> dipakai otomatis
- **SVG robot** (fallback) -> dipakai kalau tidak ada file `.vrm`

> **Kredit wajib untuk model bawaan:** `avatar\seedsan.vrm` = "Seed-san" oleh
> **VirtualCast, Inc.**, lisensi [VRM Public License 1.0](https://vrm.dev/licenses/1.0/).
> Lisensi ini **memerlukan atribusi**. Tampilkan "Seed-san by VirtualCast, Inc."
> di layar (nameTag) atau di subtitle OBS.

## 1. Cara-nya

Letakkan file `.vrm` kamu di:
```
C:\tiktok-robot\avatar\
```
Lalu restart `python robot.py` (atau `python server.py`).

Otomatis: `http://127.0.0.1:8765/` akan pakai VRM.
Kalau mau paksa pakai SVG: buka `http://127.0.0.1:8765/svg`

Kalau ada lebih dari 1 file `.vrm`, akan muncul dropdown untuk pilih karakter.
File **pertama secara alfabetis** yang jadi default -> beri awalan angka
(`1_karakter.vrm`, `2_karakter.vrm`) bila punya beberapa.

## 2. Model yang sudah tersedia

| File | Karakter | Lisensi | Ekspresi |
|------|----------|---------|----------|
| `avatar\seedsan.vrm` | Seed-san (anime) | VRM Public License 1.0 (wajib kredit) | 18 preset lengkap + rahang |

Seed-san dipakai sebagai **model uji resmi** — lisensinya mengizinkan
penggunaan avatar & komersial, hanya wajib mencantumkan kredit.

## 3. Mendapatkan Karakter (Gratis & Legal)

### Opsi A — Bikin sendiri (RECOMMENDED)
**VRoid Studio** (free, Windows/macOS): https://vroid.com/en/studio

Keuntungan:
- Gratis, **boleh dipakai komersial** (untuk live & jualan)
- Kontrol penuh: bikin robot cewek/cowok, atur warna, Atlassian, rambut, dll
- Semua model hasil VRoid Studio punya **ekspresi wajah + rahang** -> lip-sync jalan perfect
- Cocok buat request "robot yang ngeselin tapi keren": bikin sendiri, atur epigen

Cara export:
1. Buka VRoid Studio -> New / load template
2. Desain karakter (warna kulit, rambut, mata, pakaian, mechanical parts)
3. Atur ekspresi: menu "Expressions" -> isi preset (aa, ih, oh, ee, ou, blink, happy)
4. Pastikan **"Jaw" bone** ada di menu humanoid (untuk lip-sync cadangan)
5. File -> Export -> **VRM 1.0** -> simpan ke `C:\tiktok-robot\avatar\`

### Opsi B — Download dari VRoid Hub
https://hub.vroid.com

- Cari tag: `#robot`, `#mecha`, `#android`, `#cool`
- **WAJIB cek "Conditions of Use"** di halaman model:
  - `Avatar Use: Allow` -> boleh dipakai untuk live
  - `Commercial use: Allow` -> boleh dipakai untuk monetisasi
  - `Attribution: Required` -> WAJIB tampilkan nama kreator (bisa di subtitle OBS)
  - `Redistribution: Do not allow` -> JANGAN bagikan file-nya

Contoh karakter robot yang bisa dicek:
- "Kaori Robot" (Sara.W) -> `hub.vroid.com` - boleh dipakai, wajib credit
- "Free Characters" series -> ada versi 0 JPY di BOOTH

### Opsi C — BOOTH
https://booth.pm - cari "VRM" + filter gratis. Banyak yang free (0 JPY).
Baca README/LICENSE model sebelum pakai.

### Opsi D — Animasi VRMA (opsional tapi Recommended)
**VRM Animation 7-Pack by VRoid Project** (free, di BOOTH):
https://booth.pm/ja/items/9945600
Berisi 7 animasi: Show full body, Greeting, Peace sign, Shoot, Spin, Model pose, Squat.
Simpan ke `C:\tiktok-robot\avatar\animasi\` kalau mau dipakai.

## 4. Yang sudah di-handle sistem

| Fitur | Cara kerja |
|-------|-----------|
| Lip-sync | Analisis audio real-time (energi + formant) -> ekspresi `aa` + bentuk vokal `ih/ee/oh/ou` |
| Kedip | `blink` acak tiap 2.5-6.5 detik, halus (tutup-buka) |
| Ekspresi mood | `happy` (nilai 0.55) saat server kirim mood `happy` (gaya bicara ceria/excited) |
| Gerak kepala | Rotasi kepala/neck/spine halus, ikut "nengok" |
| Gerak tangan | Ayunan lengan idle (sway ±0.07 rad) |
| Gestur lengan | `wave` (melambai), `point` (menunjuk ke depan), `hand` (angkat tangan) |
| Idle | Head sway + breathing kontinu |
| Efek | Confetti/mercon/kilat/banner untuk doa & ulang tahun |
| Kamera & cahaya | Studio 3 light, auto-frame karakter (ukur siluet asli) |

### Fallback
Kalau karakter kamu **tidak punya ekspresi wajah**, sistem otomatis
menggunakan rotasi **rahang (jaw bone)** untuk GERAKAN MULUT.
Kalau juga tidak ada jaw bone, karakter akan tetap bergerak tapi
mulutnya diam (pakai ekspresi `aa` kalau ada).

## 5. Troubleshooting

**Karakter tidak muncul / "Gagal memuat VRM"**
- Cek file ada di `C:\tiktok-robot\avatar\`
- Cek format: VRM 0.x atau VRM 1.0 (dua-duanya didukung)
- Buka console browser (F12) untuk lihat pesan error
- Cek juga terminal tempat server jalan

**Karakter kecil / kegedean**
- Tinggi karakter dinormalkan otomatis ke **1.55 unit** (dihitung dari bbox
  hasil skinning, bukan bounding box statis). Ubah `const scale = 1.55 / sizeY;`
  di `web\vrm.html` kalau mau ukuran lebih tinggi/lebih pendek.
- Ukuran di layar diatur **otomatis** oleh `frameCamera()`: karakter selalu
  occupy ~91% tinggi layar (target 93%, margin 8%), di portrait maupun landscape.

**Karakter terpotong / posisi**
- Auto-frame sudah menghitung pose gestur (A-pose, melambai, menunjuk) memakai
  **render siluet sungguhan**, jadi karakter tidak akan keluar frame saat
  bergerak. Kalau masih ada yang terpotong, turunkan `TARGET` di `frameCamera()`
  (default `0.93`, makin kecil = makin banyak ruang).
- Posisi horizontal dipusatkan ke **sumbu tubuh** (rata-rata bahu kiri/kanan)
  supaya wajah tetap di tengah, walau model asimetris (mis. lengan robot
  menjulur ke satu sisi).
- Framing dihitung **350 ms setelah model selesai dimuat** (skeleton VRM perlu
  siap dulu; kalau dihitung terlalu cepat, karakter jadi sangat lebar).
- Ada **auto-fit kontinu**: setiap ~0.7 detik siluet diukur lagi; kalau ada pose
  yang keluar frame kamera mundur, kalau ada ruang kosong kamera maju pelan.
  Karakter jadi ~91% tinggi layar dan tidak akan pernah terpotong.
- Kalau mau geser kamera manual, ubah `tx`/`ty` di `frameCamera()`
  (kamera selalu diarahkan ke titik itu).
**Lip-sync tidak jalan**
- Cek di VRoid Studio apakah ekspresi `aa` dan `oh` sudah diisi
- Cek apakah humanoid punya bone `jaw`
- Pastikan user sudah klik "Aktifkan Suara" (tanpa itu audio context = suspended)

**Mata tidak berkedip**
- Model harus punya preset `blink`. Kalau tidak, tambah ekspresi di VRoid Studio.

## 6. Catatan teknis (untuk yang mau modif)

Viewer pakai **three.js 0.186.1** + **@pixiv/three-vrm 3.5.5** (lokal, tanpa CDN).

Catatan penting: di three-vrm **v3**, class `VRMLoader` sudah dihapus.
Pola yang dipakai sekarang:

```js
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { VRMLoaderPlugin } from '@pixiv/three-vrm';

const loader = new GLTFLoader();
loader.register((parser) => new VRMLoaderPlugin(parser));

const gltf = await loader.loadAsync('/avatar/karakter.vrm');
const vrm = gltf.userData.vrm;   // <-- objek VRM ada di gltf.userData
scene.add(vrm.scene);
```

File lokal (semua ada di `web\vendor\`):
- `three.module.js`, `three.core.js` -> core three.js
- `three-vrm.module.js` -> @pixiv/three-vrm
- `three\addons\loaders\GLTFLoader.js` -> loader glTF/VRM
- `three\addons\utils\BufferGeometryUtils.js`, `SkeletonUtils.js` -> dependensi GLTFLoader

Import map di `web\vrm.html`:
```json
{
  "imports": {
    "three": "/vendor/three.module.js",
    "three/addons/": "/vendor/three/addons/",
    "@pixiv/three-vrm": "/vendor/three-vrm.module.js"
  }
}
```

Untuk debugging, `window.ROBOT_VRM` menyimpan objek VRM aktif (bisa dibuka
di console browser: `ROBOT_VRM.expressionManager.getValue('aa')`).

Handle debug lain di `web\vrm.html`:

| Handle | Isi |
|--------|------|
| `ROBOT_VRM` | objek VRM aktif (`humanoid`, `expressionManager`) |
| `ROBOT_CAMERA` | kamera aktif (+ `camera.userData.fitLog` = hasil auto-frame) |
| `ROBOT_THREE` | THREE, buat bbox/bprobe manual |
| `ROBOT_SCENE` / `ROBOT_RENDERER` | scene & renderer |
| `ROBOT_SILHOUETTE()` | bbox NDC siluet saat ini (untuk cek "utuh"/terpotong) |
| `ROBOT_POSEINFO` | hasil perhitungan sudut siku/lengan |
| `ROBOT_GESTURE('wave','left',2)` | paksa gestur tertentu (untuk tes) |

### Sumbu siku di VRM (penting!)

Di rig **normalized** three-vrm v3, rotasi bone diterapkan di rest frame:

- `lowerArm.rotation.x` -> **memutar lengan** (twist), posisi tangan TIDAK berubah
- `lowerArm.rotation.z` -> **sumbu lentur siku** yang benar (tangan naik/turun + ke arah dalam tubuh)

Arah "lipatan ke dalam tubuh" mengikuti arah lengan lowered:
`arah = Math.sign(zDown)` (kiri zDown = -1.57, kanan zDown = +1.57).
Nilai yang dipakai sistem: `elbowWave` kiri `-2.25`, kanan `+2.25`
(dihitung otomatis oleh `_cariSiku()` searching `|z| 0.05..2.6`).

Gestur `point` **tidak boleh** menaikkan lengan ke samping
(`zDown * 0.45`), karena itu membuat siluet jauh lebih lebar (1.28 vs 0.63)
dan karakter jadi kecil di layar. Cukup `upperArm.rotation.x = -0.70`
(lengan ke arah kamera) + siku lurus.

### Cara mengukur lebar karakter dengan benar

`Box3.setFromObject()` pada `SkinnedMesh` memakai geometri **T-pose statis**,
jadi TIDAK bisa dipakai untuk framing. Sistem memakai:
- `_bboxSkin()` -> `applyBoneTransform()` per vertex (bbox dunia asli)
- `_silhouette()` -> render ke RT + baca piksel (NDC bbox) = **paling akurat**

Auto-frame memakai `_silhouette()` untuk 5 pose (A-pose, melambai, melambai
dengan tangan atas, melambai dengan tangan bawah, menunjuk), lalu iterasi
jarak kamera sampai semua pose muat di 93% frame.

## 7. Credit (kalau diwajibkan lisensi)
Tambahkan nama kreator di subtitle OBS atau di `#nameTag` di `web\vrm.html`.
