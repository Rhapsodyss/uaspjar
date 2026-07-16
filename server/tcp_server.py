from email import header
import socket
import os
import threading

HOST = "0.0.0.0"
PORT = 9000
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def handle_client(conn: socket.socket, addr):
    print(f"[TCP] Koneksi baru dari {addr}")
    try:

        header = b""
        while not header.endswith(b"\n"):
            chunk = conn.recv(1)
            if not chunk:
                return
            header += chunk

        command = header.decode().strip().split(" ")

        if command[0] == "UPLOAD":
            if len(command) != 3:
                conn.sendall(b"ERROR invalid_upload_format\n")
                return
            filename = command[1]
            try:
                filesize = int(command[2])
            except ValueError:
                conn.sendall(b"ERROR invalid_filesize\n")
                return
            filepath = os.path.join(UPLOAD_DIR, filename)

            received = 0
            with open(filepath, "wb") as f:
                while received < filesize:
                    data = conn.recv(4096)
                    if not data:
                        break
                    f.write(data)
                    received += len(data)

            print(f"[TCP] File '{filename}' diterima ({received} bytes)")
            conn.sendall(b"OK\n")

        elif command[0] == "DOWNLOAD":
            filename = command[1]
            filepath = os.path.join(UPLOAD_DIR, filename)

            if not os.path.exists(filepath):
                conn.sendall(b"ERROR file_not_found\n")
                return

            filesize = os.path.getsize(filepath)
            conn.sendall(f"SIZE {filesize}\n".encode())

            with open(filepath, "rb") as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    conn.sendall(data)

            print(f"[TCP] File '{filename}' dikirim ke {addr}")

    except Exception as e:
        print(f"[TCP] Error: {e}")
    finally:
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[TCP] Server berjalan di {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()


if __name__ == "__main__":
    start_server()