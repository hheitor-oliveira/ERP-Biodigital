from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user_model.user_model import UserModel
from schemas.user_schema import CreateUserSchema, LoginUserSchema
from services.users.user_service import UserService
from api.dependencies import get_session, get_access_token, pwd_context, verify_access_token
from datetime import timedelta

user_service = UserService()

auth_router = APIRouter(prefix='/auth', tags=['auth'])

def user_auth(email: str, password: str, session: Session = Depends(get_session)):
  
  query = select(UserModel).where(
    UserModel.user_email == email
  )
  
  result = session.execute(query)
  
  usuario = result.scalar_one_or_none()
  
  if not usuario:
    return False
  elif not pwd_context.verify(password, usuario.user_password): # type: ignore
    return False
  else:
    return usuario

  
@auth_router.post('/create_user')
async def create_user(user: CreateUserSchema, session: Session = Depends(get_session), user_model: UserModel = Depends(verify_access_token)):

  if not user_model.admin:
    raise HTTPException(status_code=401, detail='Acesso negado, você não tem permissão para realizar está operação')
  else:
    user_service.create_user(user.user_name,
                           user.user_email,
                           user.user_password,
                           user.admin,
                           session)
  
@auth_router.post('/login')
async def login(login_schema: LoginUserSchema ,session: Session = Depends(get_session)):
  
  usuario = user_auth(login_schema.user_email, login_schema.user_password, session)
  if not usuario:
    raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")
  else:
    access_token = get_access_token(usuario.user_id)
    refresh_token = get_access_token(usuario.user_id, duracao_token=timedelta(days=7))
    return {
      "access_token": access_token,
      "refresh_token": refresh_token,
      "token_type": "Bearer"
    }
    
@auth_router.get('/refresh')
async def use_refresh_token(usuario: UserModel = Depends(verify_access_token)):
  access_token = get_access_token(usuario.user_id)
  return {
        "access_token": access_token,
        "token_type": "Bearer"
      }                                                     
  
  
@auth_router.post('/login-form')
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
  
  usuario = user_auth(form_data.username, form_data.password, session)
  if not usuario:
    raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")
  else:
    access_token = get_access_token(usuario.user_id)
    return {
      "access_token": access_token,
      "token_type": "Bearer"
    }