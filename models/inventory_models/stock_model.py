from models.base import Base
from models.model_enums import ModelStatusEnum
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
  
  stock_status: Mapped[ModelStatusEnum] = mapped_column(
    SQLEnum(ModelStatusEnum),
    nullable = False,
    server_default = 'ACTIVE'
  )
  
  stock_description: Mapped[str] = mapped_column(
    String(500),
    nullable = True,
    server_default = 'Not defined.'
  )