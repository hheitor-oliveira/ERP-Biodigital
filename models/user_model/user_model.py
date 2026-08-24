from models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class UserModel(Base):
  
  __tablename__ = 'app_user'
  
  user_id: Mapped[int] = mapped_column(
    primary_key = True,
    autoincrement = True
  )
  
  user_name: Mapped[str] = mapped_column(
    String(100),
    nullable = False,
  )
  
  user_email: Mapped[str] = mapped_column(
    String(256),
    nullable = False,
    unique = True
  )
  
  user_password: Mapped[str] = mapped_column(
    nullable = False
  )
  
  admin: Mapped[bool] = mapped_column(
    server_default = 'FALSE',
    nullable = False
  )