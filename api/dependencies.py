from database.connection import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
