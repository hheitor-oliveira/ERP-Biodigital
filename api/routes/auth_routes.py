from fastapi import APIRouter
from schemas.user_schema import CreateUserSchema

auth_router = APIRouter(prefix='auth', tags=['auth'])

@auth_router.post('/create_user')
async def create_user(user: CreateUserSchema):
  return