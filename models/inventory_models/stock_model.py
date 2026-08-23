from models.base import Base
from domain.enums.status import StatusEnum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class StockModel(Base):
  
  __tablename__ = 'stock'
  
  stock_id: Mapped[int] = mapped_column(
    primary_key = True,
    autoincrement = True
  )
  
  stock_name: Mapped[str] = mapped_column(
    String(100),
    nullable = False,
    unique = True,
  )
  
  stock_status: Mapped[StatusEnum] = mapped_column(
    SQLEnum(StatusEnum),
    nullable = False,
    server_default = 'ACTIVE'
  )
  
  stock_description: Mapped[str] = mapped_column(
    String(500),
    nullable = True,
    server_default = 'Not defined.'
  )