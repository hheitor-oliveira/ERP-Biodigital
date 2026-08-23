from models.base import Base
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

class StockItemModel(Base):
  
  __tablename__ = 'stock_item'
  
  stock_item_id: Mapped[int] = mapped_column(
    primary_key = True,
    autoincrement = True
  )
  
  product_id: Mapped[int] = mapped_column(
    ForeignKey('product.product_id'),
    nullable = False
  )
  
  stock_id: Mapped[int] = mapped_column(
    ForeignKey('stock.stock_id'),
    nullable = False
  )
  
  quantity: Mapped[int] = mapped_column(
    nullable = False
  )
  
__table_args__ = (
        CheckConstraint(
            "quantity >= 0",
            name="stock_item_quantity_check"
        )
)