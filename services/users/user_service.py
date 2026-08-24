from repository.users.user_repository import UserRepository
from sqlalchemy.orm import Session
from domain.users.app_user import AppUser
from config.security import pwd_context

class UserService:
    
    def create_user(self,
                    name: str,
                    email: str,
                    password: str,
                    session: Session
                    ):
        
        password_hash = pwd_context.hash(password) # type: ignore
        
        user = AppUser(name, email, password_hash) # type: ignore
        
        UserRepository.create_user(user, session)