import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def connection():
    database_url = os.getenv("DATABASE_URL")

    if database_url is None:
        raise RuntimeError("DATABASE_URL não configurada")

    return create_engine(database_url)


db = connection()

SessionLocal = sessionmaker(bind=db)


def open_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()