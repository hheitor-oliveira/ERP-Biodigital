from models.base import Base
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from domain.enums.status import StatusEnum

class CategoryModel(Base):
  
  __tablename__ = 'category'
  
  category_id: Mapped[int] = mapped_column(
    primary_key = True
  )
  
  category_name: Mapped[str] = mapped_column(
    String(100),
    nullable = False
  )
  
  category_status: Mapped[StatusEnum] = mapped_column(
    SQLEnum(StatusEnum),
    nullable = False,
    server_default = 'ACTIVE'
  )