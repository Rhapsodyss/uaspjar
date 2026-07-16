# Aplikasi Pengiriman Email SMTP

Aplikasi Python ini dirancang untuk mengirim email melalui layanan SMTP. Proyek ini menekankan keamanan kredensial dengan memanfaatkan file `.env` dan mendukung proses pengiriman email menggunakan konfigurasi server SMTP.

## Fitur Utama

- Keamanan kredensial dengan penyimpanan variabel sensitif di file `.env`
- Pengiriman email menggunakan protokol SMTP
- Konfigurasi sederhana untuk email pengirim, password aplikasi, dan detail server SMTP

## Struktur Folder Proyek

- `client/`
  - `README.md` - dokumentasi proyek
  - file Python utama dan modul pendukung lainnya
- `.env` - file konfigurasi kredensial yang tidak boleh di-commit ke repositori

## Instalasi & Setup Virtual Environment

1. Buka terminal di direktori `client/`.
2. Buat virtual environment:
   ```bash
   python -m venv venv
   ```
3. Aktifkan virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS / Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```

## Konfigurasi `.env`

Buat file bernama `.env` di dalam folder `client/` dan isi dengan variabel berikut:

```env
EMAIL_ADDRESS=alamat_email_anda@gmail.com
EMAIL_PASSWORD=password_aplikasi_google
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

Penjelasan:
- `EMAIL_ADDRESS`: alamat email yang akan digunakan sebagai pengirim.
- `EMAIL_PASSWORD`: password aplikasi khusus Google App Password. Jangan gunakan password email biasa.
- `SMTP_SERVER`: alamat server SMTP, misalnya `smtp.gmail.com` untuk Gmail.
- `SMTP_PORT`: port SMTP, biasanya `587` untuk TLS.

Catatan penting:
- Jika menggunakan Gmail, aktifkan verifikasi dua langkah terlebih dahulu.
- Buat Google App Password di akun Google Anda, lalu gunakan App Password tersebut pada `EMAIL_PASSWORD`.
- Jangan simpan password atau file `.env` ke dalam repositori publik.

## Menjalankan Program

Setelah virtual environment aktif dan `.env` terkonfigurasi:

```bash
python nama_program.py
```

Gantilah `nama_program.py` dengan file entry point aplikasi Python yang sesuai di dalam folder `client/`.

Jika semuanya benar, aplikasi akan membaca konfigurasi dari `.env` dan mengirim email melalui SMTP.
