from models.base import Base
from domain.enums.movement_type import MovementType
from sqlalchemy import Enum as SQLEnum
from datetime import datetime
from sqlalchemy import ForeignKey,DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

class MovementModel(Base):
  
  __tablename__ = 'movement'
  
  movement_id: Mapped[int] = mapped_column(
    primary_key = True,
    autoincrement = True
  )
  
  user_id: Mapped[int] = mapped_column(
    ForeignKey('app_user.user_id'),
    nullable = False
  )
  
  from_stock_id: Mapped[int] = mapped_column(
    ForeignKey('stock.stock_id'),
    nullable = False
  )
  
  to_stock_id: Mapped[int] = mapped_column(
    ForeignKey('stock.stock_id'),
    nullable = False
  )
  
  movement_type: Mapped[MovementType] = mapped_column(
    SQLEnum(MovementType),
    nullable = False
  )
  
  movement_date: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.current_timestamp(),
    nullable=False
  )
  
  