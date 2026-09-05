from decimal import Decimal

from sqlalchemy import CheckConstraint, Enum as SQLEnum
from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from domain.enums.status import StatusEnum
from models.base import Base


class ProductModel(Base):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.category_id"),
        nullable=False,
    )

    available_quantity: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        server_default="0",
    )

    product_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    cost_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    sale_value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    product_status: Mapped[StatusEnum] = mapped_column(
        SQLEnum(StatusEnum),
        nullable=False,
        default=StatusEnum.ACTIVE,
        server_default="ACTIVE",
    )

    __table_args__ = (
        CheckConstraint(
            "cost_price >= 0",
            name="product_cost_price_check",
        ),
        CheckConstraint(
            "sale_value >= 0",
            name="product_sale_value_check",
        ),
        CheckConstraint(
            "available_quantity >= 0",
            name="product_available_quantity_check",
        ),
    )