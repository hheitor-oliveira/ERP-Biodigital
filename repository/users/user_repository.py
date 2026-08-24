from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_model.user_model import UserModel
from schemas.user_schema import CreateUserSchema
from api.api import pwd_context

class UserRepository():
  
  @classmethod
  def create_user(cls, user_schema: CreateUserSchema, session: Session):
    
    UserAlreadyExists = session.query(UserModel).filter(UserModel.user_email == user_schema.email).all()
    
    if len(UserAlreadyExists) > 0:
      raise HTTPException(status_code=400,
                          detail='O e-mail inserido já está cadastrado na plataforma. Se este e-mail for seu, realize login.')
    else:
      
      password_hash = pwd_context.hash(user_schema.password) # type: ignore
      
      user_model = UserModel(
        user_name = user_schema.name,
        user_email = user_schema.email,
        user_password = password_hash
      )
      
      session.add(user_model)
      session.commit()
      
      raise HTTPException(status_code = 200,
                          detail = 'Usuário cadastrado com sucesso')
    