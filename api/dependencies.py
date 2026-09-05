from database.connection import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user_model.user_model import UserModel
from config.settings import TOKEN_EXPIRE_TIME, SECRET_KEY, ALGORITHM # type: ignore

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_access_token(sub: int, duracao_token: timedelta=timedelta(TOKEN_EXPIRE_TIME)):
    
    expire = datetime.now(timezone.utc) + duracao_token
    dic_info = { # type: ignore
        "sub": str(sub), 
        "expire": int(expire.timestamp())
    }

    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM) # type: ignore

    return encoded_jwt

def verify_access_token(token: str = Depends(oauth2_schema), session: Session  = Depends(get_session)):
    
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM) # type: ignore
        sub = int(dic_info.get("sub")) # type: ignore
    except JWTError:
        raise HTTPException(status_code=401, detail='Acesso negado, verifique a validade do token.')
    
    query = select(UserModel).where(
        UserModel.user_id == sub
    )
    result = session.execute(query)
    usuario = result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=401, detail='Acesso negado')
    return usuario


def get_authenticated_user(
    user_model: UserModel = Depends(verify_access_token),
) -> UserModel:
    return user_model


def get_admin_user(
    user_model: UserModel = Depends(get_authenticated_user),
) -> UserModel:
    if not user_model.admin:
        raise HTTPException(
            status_code=401,
            detail='Acesso negado, você não tem permissão para realizar está operação',
        )
    return user_model