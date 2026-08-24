from sqlalchemy.orm import Session
from models.user_model.user_model import UserModel


class UserRepository:

    def __init__(self, session: Session):
        self._session = session

    def find_by_email(self, email: str) -> UserModel | None:
        return self._session.query(UserModel).filter(
            UserModel.user_email == email
        ).first()

    def save(self, user_model: UserModel) -> None:
        self._session.add(user_model)
        self._session.commit()
