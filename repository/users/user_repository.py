from sqlalchemy.orm import Session
from models.user_model.user_model import UserModel
from domain.users.app_user import AppUser

class UserRepository:
    
    @classmethod
    def create_user(cls,
                    user: AppUser,
                    session: Session):
        
        user_model = UserModel(
            user_name = user.name,
            user_email = user.email,
            user_password = user.password,
            admin = user.admin
        )
        
        session.add(user_model)
        session.commit()