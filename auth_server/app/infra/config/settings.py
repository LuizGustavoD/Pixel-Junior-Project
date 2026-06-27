from dataclasses import dataclass
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_DIR = os.path.dirname(BASE_DIR)

@dataclass
class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_default_secret_key")
    JWT_EXPIRES_IN_MINUTES: int = int(os.getenv("JWT_EXPIRES_IN_MINUTES", 60))
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "RS256")
    
    PRIVATE_KEY_PATH: str = os.getenv("JWT_PRIVATE_KEY_PATH", os.path.join(PROJECT_DIR, "resources", "private", "private_key.pem"))
    PUBLIC_KEY_PATH: str = os.getenv("JWT_PUBLIC_KEY_PATH", os.path.join(PROJECT_DIR, "resources", "public_key.pem"))

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_NAME: str = os.getenv("DB_NAME", "auth_db")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
