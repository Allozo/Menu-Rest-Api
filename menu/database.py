from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .dependencies import get_db_settings


# База данных SQLite по умолчанию
if getenv("DB_ENGINE") is None:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
# База данных PostgreSQL (передать переменную окружения DB_ENGINE=POSTGRESQL)
if getenv("DB_ENGINE") == "POSTGRESQL":
    settings = get_db_settings()
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.username}:{settings.password}@{settings.service}/{settings.database}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

assert engine is not None, "Не указана база данных."

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
