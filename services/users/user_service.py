from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_model.user_model import UserModel
from config.security import pwd_context


class UserService:

    def __init__(self, session: Session):
        self._session = session

    def create_user(self, name: str, email: str, password: str):

        user_already_exists = self._session.query(UserModel).filter(
            UserModel.user_email == email
        ).all()

        if len(user_already_exists) > 0:
            raise HTTPException(
                status_code=400,
                detail='O e-mail inserido já está cadastrado na plataforma. Se este e-mail for seu, realize login.'
            )

        password_hash = pwd_context.hash(password) # type: ignore

        user_model = UserModel(
            user_name=name,
            user_email=email,
            user_password=password_hash
        )

        self._session.add(user_model)
        self._session.commit()

        raise HTTPException(
            status_code=200,
            detail='Usuário cadastrado com sucesso'
        )
