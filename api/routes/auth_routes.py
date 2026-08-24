from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user_schema import CreateUserSchema
from services.users.user_service import UserService
from api.dependencies import get_session

user_service = UserService()

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.post('/create_user')
async def create_user(user: CreateUserSchema,
                      session: Session = Depends(get_session)):
  
  user_service.create_user(user.name,
                           user.email,
                           user.password,
                           session)