README - TWITTER AUTO TOOL
=============================

📌 DESKRIPSI:
Script Python ini dibuat untuk mengotomatiskan interaksi di platform Twitter/X menggunakan login cookies. Tersedia beberapa fitur utama yang bisa digunakan untuk banyak akun sekaligus, seperti:
1. Auto Follow
2. Auto Retweet
3. Auto Komentar Massal
4. Validasi & Format Cookies

⚙️ FITUR UTAMA:
----------------------------------
✅ Menu 0 - Validasi Cookies:
   - Memformat cookies mentah dari file `cookies.txt` menjadi `cookies.json`.
   - Format `cookies.txt`: JSON per akun, dipisahkan oleh 1 baris kosong.

✅ Menu 1 - Auto Follow:
   - Memfollow akun Twitter/X dari daftar username/profil yang kamu masukkan.

✅ Menu 2 - Auto Retweet:
   - Me-retweet postingan yang kamu masukkan (bisa banyak sekaligus).

✅ Menu 3 - Auto Komentar Massal:
   - Setiap akun memberikan komentar berbeda (berdasarkan urutan) ke satu/lebih postingan target.
   - Komentar diambil dari file `komentar.txt` (blok komentar per akun dipisah 1 baris kosong).

🗃️ STRUKTUR FILE YANG DIPERLUKAN:
----------------------------------
1. `cookies.txt`       ➜ File cookies mentah (JSON per akun dipisahkan baris kosong).
2. `cookies.json`      ➜ Hasil dari Menu 0 (cookie yang valid).
3. `komentar.txt`      ➜ Komentar untuk Menu 3 (tiap blok komentar = 1 akun).
4. `chromedriver.exe`  ➜ Pastikan Chrome Driver cocok dengan versi Google Chrome.

📦 DEPENDENSI YANG WAJIB DIPASANG:
----------------------------------
Install semua kebutuhan dengan perintah berikut:

pip install selenium

🧠 CARA MENJALANKAN:
----------------------------------
1. Jalankan script dengan: 
   python namascript.py

2. Ikuti petunjuk menu di terminal:
   - Gunakan dulu Menu 0 untuk mengubah `cookies.txt` ➜ `cookies.json`
   - Gunakan Menu 1, 2, atau 3 sesuai kebutuhan

🛠️ CATATAN PENTING:
----------------------------------
- Script ini bekerja secara **headless** (tanpa membuka browser secara nyata).
- Pastikan `cookies.txt` valid dan hasil export dari browser (gunakan ekstensi seperti EditThisCookie).
- Jangan gunakan akun utama sebelum diuji dulu.
- Tidak menjamin akun bebas dari suspend jika digunakan berlebihan/spam.

📁 CONTOH FORMAT `cookies.txt`:
----------------------------------
[
  { "name": "auth_token", "value": "xxxx", ... },
  { "name": "ct0", "value": "xxxx", ... },
  ...
]

⏱️ JEDA OTOMATIS:
----------------------------------
- Jeda antar akun: 1–2 menit (acak)
- Jeda antar aksi (follow/retweet/komentar): 20–45 detik (acak)

💬 KONTAK:
----------------------------------
Jika ada kendala atau ingin kustomisasi script, silakan hubungi pembuat.

