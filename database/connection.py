import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError('As credenciais passadas estão inválidas. Conexão não realizada.')

engine = create_engine(DATABASE_URL)