import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///galvan_auth.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret")
    ACCESS_EXPIRES_SECONDS = int(os.getenv("ACCESS_EXPIRES_SECONDS", 60 * 15))
    REFRESH_EXPIRES_SECONDS = int(os.getenv("REFRESH_EXPIRES_SECONDS", 60 * 60 * 24 * 7))
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    EMAIL_FROM = os.getenv("EMAIL_FROM")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    SUPERADMIN_EMAIL = os.getenv("SUPERADMIN_EMAIL", "superadmin@example.com")
    SUPERADMIN_PASSWORD = os.getenv("SUPERADMIN_PASSWORD", "SuperAdminPass123!")
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
