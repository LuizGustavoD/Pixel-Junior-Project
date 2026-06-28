from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from infra.config.settings import Settings

settings = Settings()

DATABASE_URL = settings.DATABASE_URL
if not DATABASE_URL:
    DATABASE_URL = (
        f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
