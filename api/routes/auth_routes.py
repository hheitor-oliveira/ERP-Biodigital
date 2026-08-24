from fastapi import APIRouter, Depends
from schemas.user_schema import CreateUserSchema
from repository.users.user_repository import UserRepository
from sqlalchemy.orm import Session
from database.connection import open_session

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/create_user")
async def criar_usuario(user: CreateUserSchema,
                        session: Session = Depends(open_session)
                        ):
                          
  UserRepository.create_user(user, session)
  