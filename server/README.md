# README

## Deskripsi

Repository ini berisi dua server sederhana:

- `tcp_server.py`: server TCP untuk menerima koneksi dan berkomunikasi dengan client.
- `udp_server.py`: server UDP untuk menerima dan mengirim pesan tanpa koneksi.

## Requirements

- Python 3.8 atau lebih baru
- Tidak ada dependensi eksternal selain library standar Python

Jika Anda ingin menggunakan virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## Cara Menjalankan

### Menjalankan TCP Server

```bash
python tcp_server.py
```

Secara default server akan mendengarkan pada alamat dan port yang sudah ditentukan di dalam file. Periksa kode `tcp_server.py` jika Anda ingin mengubah host/port.

### Menjalankan UDP Server

```bash
python udp_server.py
```

Server UDP akan menunggu pesan dari client pada alamat dan port yang ditentukan di dalam file.

## Catatan

- Pastikan port yang dipakai tidak bentrok dengan aplikasi lain.
- Jika ingin menguji, jalankan server terlebih dahulu baru jalankan client.
