import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# =========================
# Environment Helpers
# =========================

def env_str(name, default=""):
    value = os.getenv(name)

    if value is None or value.strip() == "":
        return default

    return value.strip()


def env_int(name, default):
    value = os.getenv(name)

    if value is None or value.strip() == "":
        return default

    try:
        return int(value)
    except ValueError:
        return default


def env_bool(name, default):
    value = os.getenv(name)

    if value is None or value.strip() == "":
        return default

    return value.strip().lower() in (
        "1",
        "true",
        "yes",
        "on"
    )


# =========================
# Database
# =========================

DATABASE = env_str(
    "DATABASE",
    os.path.join(BASE_DIR, "resume_analyzer.db")
)


# =========================
# Upload Folder
# =========================

UPLOAD_FOLDER = env_str(
    "UPLOAD_FOLDER",
    os.path.join(BASE_DIR, "uploads", "resumes")
)


# =========================
# Security
# =========================

SECRET_KEY = env_str(
    "SECRET_KEY",
    ""
)


# =========================
# Allowed Resume Files
# =========================

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}


# =========================
# Admin Login
# =========================

ADMIN_USERNAME = env_str(
    "ADMIN_USERNAME",
    ""
)

ADMIN_PASSWORD = env_str(
    "ADMIN_PASSWORD",
    ""
)


# =========================
# Email Configuration
# =========================

MAIL_SERVER = env_str(
    "MAIL_SERVER",
    "smtp.gmail.com"
)

MAIL_PORT = env_int(
    "MAIL_PORT",
    587
)

MAIL_USE_TLS = env_bool(
    "MAIL_USE_TLS",
    True
)

MAIL_USERNAME = env_str(
    "MAIL_USERNAME",
    ""
)

MAIL_PASSWORD = env_str(
    "MAIL_PASSWORD",
    ""
)

MAIL_DEFAULT_SENDER = env_str(
    "MAIL_DEFAULT_SENDER",
    MAIL_USERNAME
)