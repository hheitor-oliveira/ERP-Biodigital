from sqlalchemy.orm import Session # type: ignore
from database.connection import SessionLocal

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
