from dataclasses import dataclass
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_DIR = os.path.dirname(BASE_DIR)

@dataclass
class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_default_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "RS256")
    PUBLIC_KEY_PATH: str = os.getenv("JWT_PUBLIC_KEY_PATH", os.path.join(PROJECT_DIR, "../auth_server/resources/public_key.pem"))

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_USER: str = os.getenv("DB_USER", "auth_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "auth_password")
    DB_NAME: str = os.getenv("DB_NAME", "auth_db")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Storage Settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", os.path.join(PROJECT_DIR, "data"))
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024)) # 10MB default

    # Auth Server integration
    AUTH_SERVER_URL: str = os.getenv("AUTH_SERVER_URL", "http://localhost:5000")
