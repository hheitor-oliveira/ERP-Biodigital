import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError('As credenciais passadas estão inválidas. Conexão não realizada.')

engine = create_engine(DATABASE_URL)

def get_session():
    session = sessionmaker(bind=engine)
    return session()