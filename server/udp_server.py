import socket
import os
import time

HOST = "0.0.0.0"
PORT = 9001
VIDEO_DIR = "/home/juna/server/videos"

# Buffer size kecil standar MTU jaringan agar paket UDP tidak pecah/drop
BUFFER_SIZE = 4096

def start_server():
    # Pengecekan awal saat server dinyalakan
    print("=" * 60)
    print(f"Mengecek direktori video: {VIDEO_DIR}")
    if os.path.exists(VIDEO_DIR):
        print(f"Direktori ditemukan. Isi file saat ini: {os.listdir(VIDEO_DIR)}")
    else:
        print(f"[CRITICAL ERROR] Direktori '{VIDEO_DIR}' TIDAK DITEMUKAN!")
        print("[SOLUSI] Pastikan path absolutnya sudah benar sesuai perintah 'pwd' di Ubuntu.")
    print("=" * 60)

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"[UDP] Server streaming berjalan di {HOST}:{PORT}\n")

    while True:
        # Menunggu request dari Flask Windows
        data, addr = server.recvfrom(1024)
        filename = data.decode().strip()

        filepath = os.path.join(VIDEO_DIR, filename)
        print(f"[REQUEST] Client {addr} meminta video: '{filename}'")
        print(f"[CHECK] Mencari file di: {filepath}")

        # 1. Validasi apakah file video fisik benar-benar ada
        if not os.path.exists(filepath):
            print(f"[ERROR] File '{filename}' TIDAK ADA di folder server!")
            server.sendto(b"NOT_FOUND", addr)
            print("-" * 40)
            continue

        # 2. Ambil ukuran file dan kirim ke client
        filesize = os.path.getsize(filepath)
        print(f"[FOUND] File ditemukan! Ukuran: {filesize} bytes. Mengirim info size...")
        server.sendto(str(filesize).encode(), addr)

        # 3. Menunggu konfirmasi READY dari client
        print("[WAIT] Menunggu sinyal READY dari client...")
        try:
            server.settimeout(5.0) # Proteksi agar server tidak hang jika client putus
            ack, _ = server.recvfrom(1024)
            server.settimeout(None) # Reset timeout kembali normal

            if ack.decode().strip() != "READY":
                print(f"[CANCEL] Client mengirim ACK salah ({ack}), streaming dibatalkan.")
                print("-" * 40)
                continue
        except socket.timeout:
            print("[TIMEOUT] Client terlalu lama merespon, streaming dibatalkan.")
            server.settimeout(None)
            print("-" * 40)
            continue

        # 4. Memulai proses pengiriman data video via UDP
        print(f"[STREAM] Mulai menyemburkan paket {filename} ke {addr}...")

        sent_chunks = 0
        with open(filepath, "rb") as video:
            while True:
                chunk = video.read(BUFFER_SIZE)
                if not chunk:
                    break
                server.sendto(chunk, addr)
                sent_chunks += 1

                # Jeda tipis anti-drop (Sangat krusial untuk kestabilan UDP di VirtualBox)
                time.sleep(0.001)

        # 5. Kirim penanda akhir video
        server.sendto(b"END_VIDEO", addr)
        print(f"[SUCCESS] Streaming selesai! Total dikirim: {sent_chunks} paket.")
        print("-" * 40)

if __name__ == "__main__":
    start_server()