from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .dependencies import get_db_settings


# База данных PostgreSQL
# settings = get_db_settings()
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.username}:{settings.password}@{settings.service}/{settings.database}"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


# База данных SQLite -- расскомментировать блок ниже (и закомментировать блок выше), если хотим использовать БД sqlite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
