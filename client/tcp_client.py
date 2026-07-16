import socket
import os
import sys
from config import SERVER_HOST, TCP_PORT


def upload_file(filepath):
    if not os.path.exists(filepath):
        print(f"File '{filepath}' tidak ditemukan di komputer kamu.")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    print(f"Menghubungkan ke server {SERVER_HOST}:{TCP_PORT} ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, TCP_PORT))
        s.sendall(f"UPLOAD {filename} {filesize}\n".encode())

        sent = 0
        with open(filepath, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                s.sendall(data)
                sent += len(data)

        response = s.recv(1024)
        print(f"Terkirim {sent} bytes. Respons server:", response.decode().strip())


def download_file(filename, save_as=None):
    save_as = save_as or filename
    print(f"Menghubungkan ke server {SERVER_HOST}:{TCP_PORT} ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, TCP_PORT))
        s.sendall(f"DOWNLOAD {filename}\n".encode())

        header = b""
        while not header.endswith(b"\n"):
            header += s.recv(1)

        response = header.decode().strip()
        if response.startswith("ERROR"):
            print("Gagal:", response)
            return

        filesize = int(response.split(" ")[1])
        received = 0
        with open(save_as, "wb") as f:
            while received < filesize:
                data = s.recv(4096)
                if not data:
                    break
                f.write(data)
                received += len(data)

        print(f"File '{filename}' berhasil diunduh ke komputer kamu ({received} bytes)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Cara pakai: python tcp_client.py [upload|download] <nama_file>")
        sys.exit(1)

    action = sys.argv[1]
    filename = sys.argv[2]

    if action == "upload":
        upload_file(filename)
    elif action == "download":
        download_file(filename)
    else:
        print("Perintah tidak dikenali. Gunakan 'upload' atau 'download'.")
