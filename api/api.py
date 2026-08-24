from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

app = FastAPI()

from api.routes.inventory_routes import inventory_router
from api.routes.auth_routes import auth_router

app.include_router(inventory_router)
app.include_router(auth_router)