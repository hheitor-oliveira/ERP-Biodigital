from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_EXPIRE_TIME = int(os.getenv("TOKEN_EXPIRE_TIME")) # type: ignore