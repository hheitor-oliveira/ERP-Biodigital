from models.base import Base
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column


class MovementItemModel(Base):

    __tablename__ = 'movement_item'

    movement_item_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    movement_id: Mapped[int] = mapped_column(
        ForeignKey('movement.movement_id'),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.product_id'),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "quantity >= 0",
            name="movement_item_quantity_check"
        ),
    )
