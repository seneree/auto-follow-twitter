
# 🐦 Auto Follow Twitter (X.com) via Selenium Headless

Script Python untuk melakukan auto-follow akun Twitter (X.com) menggunakan cookies login dan Selenium dalam mode headless (tanpa membuka browser). Cocok untuk penggunaan massal dan otomatisasi airdrop/farming sosial.

---

## ✨ Fitur

- 🔁 Auto-follow akun X (Twitter) dengan banyak akun (multi-cookie).
- 🧼 Membersihkan `cookies.txt` menjadi `cookies.json` siap pakai.
- 🤖 Headless: tidak membuka jendela browser (otomatis di background).
- 🔐 Menghindari deteksi bot dengan rotasi User-Agent dan manipulasi `webdriver`.
- 📋 Menu CLI sederhana dan interaktif.

---

## 🧩 Struktur File

| File             | Keterangan                                                  |
|------------------|-------------------------------------------------------------|
| `twitter.py`     | Script utama auto-follow dan pembersih cookies.             |
| `cookies.txt`    | File input cookies mentah (1 blok JSON per akun, dipisah enter). |
| `cookies.json`   | Hasil pembersihan cookie, siap dipakai untuk follow.        |

---

## ⚙️ Cara Menjalankan

### 1. Install Python dan Modul yang Dibutuhkan

Pastikan Python 3.8+ sudah terinstall. Lalu jalankan:

```bash
pip install selenium
```

### 2. Download ChromeDriver

- Cek versi Google Chrome kamu: buka `chrome://settings/help`
- Download driver yang cocok dari: https://chromedriver.chromium.org/downloads
- Letakkan `chromedriver.exe` di folder project atau folder PATH

### 3. Jalankan Script

```bash
python twitter.py
```

Ikuti menu yang muncul di terminal.

---

## 📝 Format Cookies.txt

Isi file `cookies.txt` seperti ini, **1 akun per blok JSON**, dipisah enter:

```
[
  {"name": "auth_token", "value": "xxxx", "domain": ".x.com"},
  {"name": "ct0", "value": "yyyy", "domain": ".x.com"}
]

[
  {"name": "auth_token", "value": "zzzz", "domain": ".x.com"},
  {"name": "ct0", "value": "wwww", "domain": ".x.com"}
]
```

Setelah dibersihkan, file `cookies.json` akan berisi array cookie dalam format Python dict per akun.

---

## 🛡️ Catatan Penting

- Jangan gunakan akun utama! Gunakan akun dummy atau farming.
- Pastikan cookies valid dan belum kadaluarsa.
- Jangan share file `cookies.txt` atau `cookies.json` ke publik.
