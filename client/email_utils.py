import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Import library untuk membaca .env
from dotenv import load_dotenv

# Memuat variabel dari file .env ke environment variable sistem
load_dotenv()

# ==== KONFIGURASI EMAIL ====
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Mengambil nilai dari .env
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


def send_verification_email(to_email: str, verify_link: str):
    """Mengirim email berisi link verifikasi ke user."""
    # Pastikan kredensial berhasil terbaca
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("[EMAIL] Gagal mengirim: Kredensial EMAIL tidak ditemukan di .env")
        return

    subject = "Verifikasi Akun Kamu"
    body = f"""
    Halo,

    Terima kasih sudah mendaftar. Klik link di bawah ini untuk verifikasi akun kamu:

    {verify_link}

    Link ini berlaku selama 1 jam.

    Jika kamu tidak merasa mendaftar, abaikan email ini.
    """

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # enkripsi koneksi
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"[EMAIL] Verifikasi terkirim ke {to_email}")
    except Exception as e:
        print(f"[EMAIL] Gagal mengirim email: {e}")