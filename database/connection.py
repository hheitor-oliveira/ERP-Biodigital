from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL


def connection():
    if DATABASE_URL is None:
        raise RuntimeError("DATABASE_URL não configurada")

    return create_engine(DATABASE_URL)


db = connection()

SessionLocal = sessionmaker(bind=db)