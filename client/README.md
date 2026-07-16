# Client Application - Sistem Notifikasi Email

## Deskripsi Proyek

Aplikasi client berbasis Python yang memungkinkan pengguna mengirimkan notifikasi email dengan aman. Aplikasi ini mengintegrasikan keamanan kredensial menggunakan file `.env` dan mendukung pengiriman email melalui SMTP Gmail.

## Fitur Utama

- **Keamanan Kredensial**: Menyimpan kredensial sensitif di file `.env` yang tidak tersimpan di repository
- **Pengiriman SMTP**: Integrasi dengan Gmail SMTP untuk mengirimkan email
- **Database SQLite**: Menyimpan history dan data pengguna secara lokal
- **Interface User-Friendly**: Aplikasi yang mudah digunakan

## Struktur Folder Proyek

```
client/
├── README.md                 # Dokumentasi proyek ini
├── requirements.txt          # Daftar library Python yang diperlukan
├── .env.example             # Template file konfigurasi (gunakan sebagai referensi)
├── config.py                # File konfigurasi aplikasi
├── main.py                  # File utama aplikasi
├── database.py              # Modul manajemen database SQLite
├── email_sender.py          # Modul pengiriman email via SMTP
├── utils.py                 # Fungsi utility dan helper
└── data/
    └── app.db               # File database SQLite (otomatis dibuat)
```

## Requirements

Proyek ini memerlukan Python 3.8+ dan beberapa library berikut:

```
python-dotenv==1.0.0
smtplib (built-in)
sqlite3 (built-in)
```

Untuk daftar lengkap, lihat file `requirements.txt`

## Database

Aplikasi menggunakan **SQLite** sebagai database lokal. SQLite dipilih karena:

- **Lightweight**: Tidak memerlukan server terpisah
- **Portabel**: Data tersimpan dalam satu file (`app.db`)
- **Mudah Setup**: Tidak perlu konfigurasi kompleks
- **Built-in**: Sudah tersedia di Python standard library

Database menyimpan:
- Data pengguna yang terdaftar
- History pengiriman email
- Log aktivitas aplikasi

Database akan otomatis dibuat pada folder `data/` saat pertama kali aplikasi dijalankan.

## 🚀 Langkah-Langkah Instalasi

### 1. Clone atau Download Repository
```bash
cd client/
```

### 2. Buat Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup File `.env`
Salin file `.env.example` menjadi `.env`:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

## Panduan Konfigurasi `.env`

File `.env` mengandung semua kredensial sensitif. Ikuti langkah berikut:

### Langkah 1: Dapatkan Google App Password

**PENTING**: Google tidak memperbolehkan menggunakan password email biasa untuk aplikasi pihak ketiga. Anda harus membuat **Google App Password**:

1. Buka https://myaccount.google.com/
2. Klik **Security** di menu sebelah kiri
3. Aktifkan **2-Step Verification** jika belum aktif
4. Cari opsi **App passwords** (muncul setelah 2FA diaktifkan)
5. Pilih **Mail** dan **Windows Computer** (atau device Anda)
6. Google akan generate password 16 karakter - **COPY password ini**

### Langkah 2: Edit File `.env`

Buka file `.env` dengan text editor dan isi dengan template berikut:

```env
# Email Configuration
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_16_character_app_password_here

# Database
DATABASE_PATH=data/app.db

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

### Penjelasan Setiap Variabel:

| Variabel | Deskripsi | Contoh |
|----------|-----------|--------|
| `EMAIL_ADDRESS` | Email Gmail Anda | `myemail@gmail.com` |
| `EMAIL_PASSWORD` | **Google App Password** (bukan password biasa) | `abcd efgh ijkl mnop` |
| `DATABASE_PATH` | Path folder database | `data/app.db` |
| `DEBUG` | Mode debug (True/False) | `True` |
| `LOG_LEVEL` | Level logging | `INFO` |

### Penting:

- **JANGAN** gunakan password email biasa - gunakan **Google App Password**
- **JANGAN** commit file `.env` ke repository (sudah di `.gitignore`)
- Simpan `.env` file dengan aman dan jangan bagikan kredensial
- Untuk user lain, mereka perlu membuat `.env` mereka sendiri dengan App Password mereka

## Cara Menjalankan Program

### 1. Pastikan Virtual Environment Aktif
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Jalankan Aplikasi
```bash
python main.py
```

### 3. Ikuti Instruksi di Terminal

Program akan menampilkan menu interaktif:
- Pilihan untuk mengirim email
- Melihat history pengiriman
- Manage user
- Setting aplikasi

### 4. Troubleshooting

**Jika muncul error "ModuleNotFoundError":**
```bash
pip install -r requirements.txt
```

**Jika email tidak terkirim:**
- Pastikan `.env` sudah dikonfigurasi dengan benar
- Gunakan **Google App Password**, bukan password biasa
- Pastikan 2FA Gmail sudah diaktifkan
- Periksa koneksi internet

**Jika database error:**
```bash
# Hapus database yang corrupted
rm data/app.db

# Database akan dibuat ulang saat program dijalankan
python main.py
```

## Catatan Tambahan

- Aplikasi membuat folder `data/` otomatis jika belum ada
- Semua log tersimpan di terminal
- Setiap pengiriman email tercatat di database

---

**Dibuat untuk: UAS 2 - Jaringan Komputer**