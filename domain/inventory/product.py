# lib's imports
from decimal import Decimal

# internal import's
from domain.enums.status import StatusEnum
from domain.exceptions import (
    InvalidProductCategoryError,
    InvalidProductStatusTransitionError,
    ProductValidationError,
)
from domain.inventory.category import Category


def normalize_product_name(name: str) -> str:
    canonical_name = " ".join(name.split()).upper()

    if not canonical_name:
        raise ProductValidationError("Product name cannot be blank.")

    return canonical_name


_MAX_MONEY_VALUE = Decimal("99999999.99")


def validate_product_money(value: Decimal, field_name: str) -> Decimal:
    if not isinstance(value, Decimal): # type: ignore
        raise ProductValidationError(
            f"{field_name} must be a Decimal value."
        )

    exponent = value.as_tuple().exponent
    decimal_places = -exponent if isinstance(exponent, int) else 0

    if (
        not value.is_finite()
        or value < Decimal("0")
        or value > _MAX_MONEY_VALUE
        or decimal_places > 2
    ):
        raise ProductValidationError(
            f"{field_name} must be a non-negative Decimal "
            "with at most two decimal places."
        )

    return value


def validate_product_quantity(quantity: int) -> int:
    if isinstance(quantity, bool) or not isinstance(quantity, int): # type: ignore
        raise ProductValidationError(
            "Product available quantity must be an integer."
        )

    if quantity < 0:
        raise ProductValidationError(
            "Product available quantity cannot be negative."
        )

    return quantity


def validate_product_status(status: StatusEnum) -> StatusEnum:
    if not isinstance(status, StatusEnum): # type: ignore
        raise ProductValidationError(
            "Product status must be a valid StatusEnum value."
        )

    return status


class Product:
    """
    A classe responsável por representar um produto do sistema e realizar operações relacionadas ao produto:
    """
    def __init__(self,
                 name: str,
                 category: Category,
                 cost_price: Decimal,
                 sale_value: Decimal,
                 available_quantity: int = 0,
                 status: StatusEnum = StatusEnum.ACTIVE,
                 id: int | None = None
                 ) -> None:

        self._id = id
        self._name = normalize_product_name(name)
        self._category = category
        self._available_quantity = validate_product_quantity(
            available_quantity
        )
        self._sale_value = validate_product_money(sale_value, "Sale value")
        self._cost_price = validate_product_money(cost_price, "Cost price")
        self._status = validate_product_status(status)

    @classmethod
    def restore(cls,
                id: int,
                name: str,
                category: Category,
                available_quantity: int,
                sale_value: Decimal,
                cost_price: Decimal,
                status: StatusEnum) -> Product:

        product = object.__new__(cls)

        product._id = id
        product._name = normalize_product_name(name)
        product._category = category
        product._available_quantity = validate_product_quantity(
            available_quantity
        )
        product._sale_value = validate_product_money(
            sale_value,
            "Sale value",
        )
        product._cost_price = validate_product_money(
            cost_price,
            "Cost price",
        )
        product._status = validate_product_status(status)

        return product

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def category(self) -> Category:
        return self._category
    
    @property
    def cost_price(self) -> Decimal:
        return self._cost_price
    
    @property
    def sale_value(self) -> Decimal:
        return self._sale_value
    
    @property
    def available_quantity(self) -> int:
        return self._available_quantity
    
    @property
    def status(self) -> StatusEnum:
        return self._status

    @property
    def id(self) -> int | None:
        return self._id

    def add_stock(self, 
                  quantity: int) -> None:
        validated_quantity = validate_product_quantity(quantity)
        self._available_quantity = validate_product_quantity(
            self._available_quantity + validated_quantity
        )
    
    def change_name(self, new_name: str) -> None:
        self._name = normalize_product_name(new_name)
        
    def change_sale_value(self, new_sale_value: Decimal) -> None:
        self._sale_value = validate_product_money(
            new_sale_value,
            "Sale value",
        )
        
    def change_cost_price(self, new_cost_price: Decimal) -> None:
        self._cost_price = validate_product_money(
            new_cost_price,
            "Cost price",
        )
        
    def change_status(self, new_status: StatusEnum) -> None:
        validated_status = validate_product_status(new_status)

        if validated_status == self._status:
            return

        allowed_transitions = {
            StatusEnum.ACTIVE: {
                StatusEnum.INACTIVE,
                StatusEnum.DISCONTINUED,
            },
            StatusEnum.INACTIVE: {StatusEnum.ACTIVE},
            StatusEnum.DISCONTINUED: {StatusEnum.ACTIVE},
        }

        if validated_status not in allowed_transitions[self._status]:
            raise InvalidProductStatusTransitionError(
                f"Cannot change product status from "
                f"{self._status.value} to {validated_status.value}."
            )

        if (
            validated_status == StatusEnum.ACTIVE
            and self._category.status != StatusEnum.ACTIVE
        ):
            raise InvalidProductCategoryError(
                "Product can only be reactivated with an active category."
            )

        self._status = validated_status
        
    def change_category(self, new_category: Category) -> None:
        self._category = new_category

    def can_add_stock(self) -> bool:
        return self._status == StatusEnum.ACTIVE

    def can_sell(self) -> bool:
        return self._status in {
            StatusEnum.ACTIVE,
            StatusEnum.DISCONTINUED,
        }
        