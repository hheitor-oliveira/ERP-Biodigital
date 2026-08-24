from fastapi import APIRouter, Depends
from schemas.user_schema import CreateUserSchema
from services.users.user_service import UserService
from sqlalchemy.orm import Session
from api.dependencies import get_session

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/create_user")
async def criar_usuario(user: CreateUserSchema,
                        session: Session = Depends(get_session)
                        ):

  user_service = UserService(session)
  user_service.create_user(user.name, user.email, user.password)
