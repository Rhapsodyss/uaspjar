import sqlite3
import os
import socket
import threading
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Response
import udp_client
from flask import Response, stream_with_context
from flask import Response, send_file
import io 

from email_utils import send_verification_email

app = Flask(__name__)
app.secret_key = "ganti-dengan-secret-key-yang-aman"  # PENTING: ganti saat production

# Serializer untuk membuat token verifikasi email yang aman & ada masa berlaku
serializer = URLSafeTimedSerializer(app.secret_key)

DB_PATH = "users.db"


def init_db():
    """Membuat tabel users jika belum ada."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_verified INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    if "user_email" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        hashed_pw = generate_password_hash(password)

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (email, password, is_verified) VALUES (?, ?, 0)",
                (email, hashed_pw),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Email sudah terdaftar.", "error")
            conn.close()
            return redirect(url_for("register"))
        conn.close()

        # Buat token verifikasi & kirim email
        token = serializer.dumps(email, salt="email-verify")
        verify_link = url_for("verify_email", token=token, _external=True)
        send_verification_email(email, verify_link)

        flash("Registrasi berhasil! Cek email kamu untuk verifikasi.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/verify/<token>")
def verify_email(token):
    try:
        # max_age dalam detik (1 jam)
        email = serializer.loads(token, salt="email-verify", max_age=3600)
    except Exception:
        return "Link verifikasi tidak valid atau sudah kadaluarsa.", 400

    conn = get_db()
    conn.execute("UPDATE users SET is_verified = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    flash("Email berhasil diverifikasi! Silakan login.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user is None or not check_password_hash(user["password"], password):
            flash("Email atau password salah.", "error")
            return redirect(url_for("login"))

        if user["is_verified"] == 0:
            flash("Email belum diverifikasi. Cek inbox kamu.", "error")
            return redirect(url_for("login"))

        session["user_email"] = email
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_email", None)
    return redirect(url_for("login"))


def login_required(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_email" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", email=session["user_email"])


@app.route("/upload", methods=["GET"])
@login_required
def upload_page():
    files = os.listdir("uploads") if os.path.exists("uploads") else []
    return render_template("upload.html", files=files)


@app.route("/upload_action", methods=["POST"])
@login_required
def upload_action():
    file = request.files.get("file")
    if not file:
        flash("Tidak ada file dipilih.", "error")
        return redirect(url_for("upload_page"))

    # --- PERIKSA BARIS INI ---
    # Pastikan variabel safe_filename dibuat menggunakan fungsi secure_filename
    safe_filename = secure_filename(file.filename)
    
    if not safe_filename:
        flash("Nama file tidak valid.", "error")
        return redirect(url_for("upload_page"))

    # Folder temporary untuk menyimpan file sebelum ditembak via TCP
    temp_path = os.path.join("uploads", "_tmp_" + safe_filename)
    file.save(temp_path)
    filesize = os.path.getsize(temp_path)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Pastikan IP ini sudah sesuai dengan IP Ubuntu VirtualBox Anda
            s.connect(("10.210.242.190", 9000)) 
            
            # Sekarang safe_filename sudah aman digunakan di sini
            s.sendall(f"UPLOAD {safe_filename} {filesize}\n".encode())
            
            with open(temp_path, "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    s.sendall(chunk)
            response = s.recv(1024).decode().strip()
            
        os.remove(temp_path)
        flash(f"File berhasil dikirim via TCP. Respons server: {response}", "success")
    except ConnectionRefusedError:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        flash("Gagal terhubung ke TCP server di Ubuntu. Pastikan IP benar dan port terbuka.", "error")

    return redirect(url_for("upload_page"))


@app.route("/download/<filename>")
@login_required
def download_action(filename):
    return send_from_directory("uploads", filename, as_attachment=True)


@app.route("/stream")
@login_required
def stream_page():
    # Karena video ada di Ubuntu, kita hardcode saja daftar video yang tersedia 
    # atau nanti bisa disesuaikan dengan kebutuhan Anda.
    videos = ["video1.mp4"] 
    return render_template("stream.html", videos=videos)

SERVER_HOST = "10.210.242.190" 
UDP_PORT = 9001
BUFFER_SIZE = 4096

@app.route("/videos/<filename>")
@login_required
def serve_video(filename):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(3.0) 

    print(f"[Flask Proxy] Meminta video '{filename}' via UDP...")
    client.sendto(filename.encode(), (SERVER_HOST, UDP_PORT))

    try:
        data, addr = client.recvfrom(1024)
        response = data.decode().strip()

        if response == "NOT_FOUND":
            return "File tidak ditemukan di server Ubuntu", 404
        
        client.sendto(b"READY", addr)
    except Exception as e:
        return f"Gagal jabat tangan dengan UDP Server: {e}", 500

    video_buffer = bytearray()

    # Mengumpulkan seluruh paket UDP
    while True:
        try:
            data, addr = client.recvfrom(BUFFER_SIZE)
            if data == b"END_VIDEO":
                print("[Flask Proxy] Seluruh paket UDP selesai diterima!")
                break
            video_buffer.extend(data)
        except socket.timeout:
            print("[Flask Proxy] Timeout terlampaui saat menerima paket.")
            break

    if len(video_buffer) == 0:
        return "Gagal memuat data video (Data 0 Bytes)", 500

    print(f"[Flask Proxy] Total data di RAM: {len(video_buffer)} bytes. Mengirim dengan send_file...")

    # --- PERBAIKAN DI SINI ---
    # Mengubah bytearray di RAM menjadi object file virtual (stream)
    video_stream = io.BytesIO(bytes(video_buffer))
    
    # Menggunakan send_file bawaan Flask karena secara otomatis menangani
    # Content-Length, HTTP Range, dan buffer yang ramah bagi browser modern.
    return send_file(
        video_stream,
        mimetype="video/mp4",
        as_attachment=False,
        download_name=filename
    )

if __name__ == "__main__":
    init_db()
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("videos", exist_ok=True)

    # Thread TCP/UDP dihapus dari sini agar tidak error NameError lagi

    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
