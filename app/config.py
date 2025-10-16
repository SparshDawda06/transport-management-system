import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Database connection - try MySQL first, fallback to SQLite
    DB_USER = os.getenv("MYSQL_USER", "root")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    DB_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    DB_PORT = os.getenv("MYSQL_PORT", "3306")
    DB_NAME = os.getenv("MYSQL_DB", "transport_mgmt")
    
    # Use SQLite for now (MySQL not available)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "..", "instance", "transport_mgmt.db")}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session/cookies
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # File uploads
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(os.getcwd(), "uploads"))
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB


class ProductionConfig(Config):
    DEBUG = False
    
    # Production database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f'sqlite:///{os.path.join(os.path.dirname(__file__), "..", "instance", "transport_mgmt.db")}'
    )
    
    # Security settings
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    
    # File upload settings
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "/tmp/uploads")


class DevelopmentConfig(Config):
    DEBUG = True
