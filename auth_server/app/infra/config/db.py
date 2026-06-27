from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infra.config.settings import Settings


DATABASE_URL = Settings.DATABASE_URL
if not DATABASE_URL:
    DATABASE_URL = (
        f"mysql+pymysql://{Settings.DB_USER}:{Settings.DB_PASSWORD}"
        f"@{Settings.DB_HOST}:{Settings.DB_PORT}/{Settings.DB_NAME}"
    )

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)