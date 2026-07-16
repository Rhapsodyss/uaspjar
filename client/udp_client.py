import socket
from config import SERVER_HOST, UDP_PORT

# DIUBAH: Harus sama dengan BUFFER_SIZE server
BUFFER_SIZE = 4096 

def generator_udp_stream(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(3) 

    client.sendto(filename.encode(), (SERVER_HOST, UDP_PORT))

    try:
        data, addr = client.recvfrom(1024)
        response = data.decode().strip()

        if response == "NOT_FOUND":
            return
        
        client.sendto(b"READY", addr)
    except Exception:
        return

    while True:
        try:
            data, addr = client.recvfrom(BUFFER_SIZE)
            if data == b"END_VIDEO":
                break
            yield data
        except socket.timeout:
            break