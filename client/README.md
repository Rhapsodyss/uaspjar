# SERVER (jalankan di VirtualBox Ubuntu)

Folder ini berisi semua yang perlu jalan di **VM VirtualBox Ubuntu**:
- `app.py` — web server Flask (login, register, verifikasi email, dashboard)
- `tcp_server.py` — server TCP untuk file transfer
- `udp_server.py` — server UDP untuk streaming video
- `email_utils.py` — pengirim email verifikasi

## 1. Copy folder ini ke VM

Bisa lewat shared folder VirtualBox, `scp`, atau `git clone` kalau kamu push ke GitHub dulu.

## 2. Cek IP VM (penting, dipakai nanti oleh client di VS Code)

Di dalam VM Ubuntu, jalankan:
```bash
ip a
```
Cari alamat IP di adapter jaringan (biasanya `enp0s3` atau `eth0`), contoh: `192.168.1.105`.
Catat IP ini — nanti dipakai di `client/config.py`.

**Penting:** Set Network Adapter VM ke **Bridged Adapter** (Settings > Network di VirtualBox),
supaya VM dapat IP di jaringan lokal yang sama dengan laptop kamu, dan bisa diakses langsung.

## 3. Install dependency & jalankan

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Edit `email_utils.py`, isi `SENDER_EMAIL` dan `SENDER_PASSWORD` (App Password Gmail).

Cukup jalankan **satu perintah saja** — web server, TCP server, dan UDP server
akan otomatis menyala bersamaan (TCP & UDP jalan sebagai background thread di
dalam proses yang sama):

```bash
python3 app.py
```

Kamu akan melihat log seperti ini menandakan ketiganya sudah aktif:
```
[TCP] Server berjalan di 0.0.0.0:9000
[MAIN] TCP server (9000) & UDP server (9001) berjalan di background
[UDP] Server streaming berjalan di 0.0.0.0:9001
* Running on http://0.0.0.0:5000
```

## 4. Buka web dari browser (bisa dari VM sendiri atau dari laptop host)

Dari laptop host (di luar VM), buka:
```
http://<IP_VM>:5000
```
Contoh: `http://192.168.1.105:5000`

## 5. Firewall (jika perlu)

Kalau tidak bisa diakses dari luar VM, buka port di firewall Ubuntu:
```bash
sudo ufw allow 5000
sudo ufw allow 9000
sudo ufw allow 9001
```

## 6. Deploy publik dengan Cloudflare Tunnel (opsional)

Lihat instruksi lengkap di README utama project (bagian Cloudflare Tunnel).
Tunnel ini expose `app.py` (port 5000) ke internet lewat domain kamu.
