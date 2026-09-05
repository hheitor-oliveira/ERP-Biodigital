from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
)

from domain.enums.status import StatusEnum
from domain.inventory.category import Category
from models.inventory_models.product_model import ProductModel


_MAX_MONEY_VALUE = Decimal("99999999.99")


def validate_money(value: Decimal) -> Decimal:
    if not value.is_finite():
        raise ValueError("Monetary value must be finite.")

    if value < Decimal("0"):
        raise ValueError("Monetary value cannot be negative.")

    if value > _MAX_MONEY_VALUE:
        raise ValueError(
            "Monetary value must be less than or equal to 99999999.99."
        )

    exponent = value.as_tuple().exponent
    decimal_places = -exponent if isinstance(exponent, int) else 0

    if decimal_places > 2:
        raise ValueError(
            "Monetary value cannot have more than two decimal places."
        )

    return value


def validate_product_name(name: str) -> str:
    if not name.strip():
        raise ValueError("Product name cannot be blank.")

    if len(name) > 100:
        raise ValueError(
            "Product name must be at most 100 characters long."
        )

    return name


class ProductMoneySchema(BaseModel):
    cost_price: Decimal
    sale_value: Decimal

    @field_validator("cost_price", "sale_value")
    @classmethod
    def validate_prices(cls, value: Decimal) -> Decimal:
        return validate_money(value)


class CreateProductSchema(ProductMoneySchema):
    name: str
    category_id: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return validate_product_name(value)


class ProductQueryFilterSchema(BaseModel):
    name: str | None = None
    category_id: int | None = None
    status: StatusEnum | None = None

    @field_validator("name")
    @classmethod
    def validate_query_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return validate_product_name(value)


class UpdateProductSchema(BaseModel):
    name: str | None = None
    category_id: int | None = Field(default=None, gt=0)
    cost_price: Decimal | None = None
    sale_value: Decimal | None = None

    @field_validator("name")
    @classmethod
    def validate_update_name(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("Product name cannot be null.")

        validate_product_name(value)
        return " ".join(value.split()).upper()

    @field_validator("cost_price", "sale_value")
    @classmethod
    def validate_update_prices(cls, value: Decimal | None) -> Decimal | None:
        if value is None:
            raise ValueError("Monetary values cannot be null.")

        return validate_money(value)

    def has_updates(self) -> bool:
        return any(
            value is not None
            for value in (
                self.name,
                self.category_id,
                self.cost_price,
                self.sale_value,
            )
        )


class ProductStatusUpdateSchema(BaseModel):
    status: StatusEnum


class CategoryResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(validation_alias="category_id")
    name: str = Field(validation_alias="category_name")
    status: StatusEnum = Field(validation_alias="category_status")


class ProductResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int = Field(validation_alias="product_id")
    name: str = Field(validation_alias="product_name")
    category: CategoryResponseSchema
    cost_price: Decimal
    sale_value: Decimal
    status: StatusEnum = Field(validation_alias="product_status")
    available_quantity: int

    @field_serializer("cost_price", "sale_value")
    def serialize_money(self, value: Decimal) -> str:
        return f"{value:.2f}"

    @classmethod
    def from_model(
        cls,
        product_model: ProductModel,
        category: Category,
    ) -> "ProductResponseSchema":
        if product_model.product_id is None:
            raise ValueError("Persisted product must have an identifier.")

        if category.id is None:
            raise ValueError("Persisted category must have an identifier.")

        return cls(
            id=product_model.product_id,
            name=product_model.product_name,
            category=CategoryResponseSchema(
                id=category.id,
                name=category.name,
                status=category.status,
            ),
            cost_price=product_model.cost_price,
            sale_value=product_model.sale_value,
            status=product_model.product_status,
            available_quantity=product_model.available_quantity,
        )