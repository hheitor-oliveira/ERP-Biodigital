from models.base import Base
from sqlalchemy import CheckConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from domain.enums.status import StatusEnum


class CategoryModel(Base):
  __tablename__ = 'category'
  
  category_id: Mapped[int] = mapped_column(
    primary_key = True,
    autoincrement = True
  )
  
  category_name: Mapped[str] = mapped_column(
    String(32),
    nullable = False,
    unique = True
  )
  
  category_status: Mapped[StatusEnum] = mapped_column(
    SQLEnum(StatusEnum),
    nullable = False,
    server_default = 'ACTIVE'
  )
  
  __table_args__ = (
    CheckConstraint(
      "length(category_name) BETWEEN 5 AND 32",
      name="category_name_length_check"
    ),
  )