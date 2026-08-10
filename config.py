import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR, "resume_analyzer.db")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "resumes")

SECRET_KEY = "resume_analyzer_secret_key"

ALLOWED_EXTENSIONS = {"pdf", "docx"}

# Admin Login Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# =========================
# Email Configuration
# =========================

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "mk684996@gmail.com"
MAIL_PASSWORD = "oxwd auxg wfbl pdib"
MAIL_DEFAULT_SENDER = MAIL_USERNAME