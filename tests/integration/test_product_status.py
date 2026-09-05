from decimal import Decimal

import pytest

from domain.enums.status import StatusEnum
from domain.exceptions import (
    InvalidProductCategoryError,
    InvalidProductStatusTransitionError,
    ProductNotFoundError,
    ProductValidationError,
)
from domain.inventory.product import Product
from models.inventory_models.product_model import ProductModel
from services.inventory.category_service import CategoryService
from services.inventory.product_service import ProductService


pytestmark = pytest.mark.integration


def create_product(
    db_session,
    category_id: int,
    *,
    name: str = "Status Product",
    status: StatusEnum = StatusEnum.ACTIVE,
) -> ProductModel:
    product = ProductModel(
        category_id=category_id,
        product_name=name,
        cost_price=Decimal("10.00"),
        sale_value=Decimal("15.00"),
        available_quantity=3,
        product_status=status,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


def test_change_product_status_allows_active_to_inactive(
    db_session,
    category_factory,
):
    category = category_factory()
    product = create_product(db_session, category.category_id)

    updated_product = ProductService.change_product_status(
        product.product_id,
        StatusEnum.INACTIVE,
        db_session,
    )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product.product_id)

    assert updated_product.product_id == product.product_id
    assert persisted_product.product_status == StatusEnum.INACTIVE
    assert persisted_product.product_name == "STATUS PRODUCT"
    assert persisted_product.category_id == category.category_id
    assert persisted_product.cost_price == Decimal("10.00")
    assert persisted_product.sale_value == Decimal("15.00")
    assert persisted_product.available_quantity == 3


def test_change_product_status_allows_active_to_discontinued(
    db_session,
    category_factory,
):
    category = category_factory()
    product = create_product(db_session, category.category_id)

    ProductService.change_product_status(
        product.product_id,
        StatusEnum.DISCONTINUED,
        db_session,
    )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product.product_id)

    assert persisted_product.product_id == product.product_id
    assert persisted_product.product_status == StatusEnum.DISCONTINUED
    assert persisted_product.product_name == "STATUS PRODUCT"
    assert persisted_product.available_quantity == 3


@pytest.mark.parametrize("initial_status", [StatusEnum.INACTIVE, StatusEnum.DISCONTINUED])
def test_change_product_status_allows_reactivation_with_active_category(
    db_session,
    category_factory,
    initial_status,
):
    category = category_factory()
    product = create_product(
        db_session,
        category.category_id,
        status=initial_status,
    )

    ProductService.change_product_status(
        product.product_id,
        StatusEnum.ACTIVE,
        db_session,
    )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product.product_id)

    assert persisted_product.product_id == product.product_id
    assert persisted_product.product_status == StatusEnum.ACTIVE
    assert persisted_product.category_id == category.category_id
    assert persisted_product.available_quantity == 3


@pytest.mark.parametrize("status", [StatusEnum.ACTIVE, StatusEnum.INACTIVE, StatusEnum.DISCONTINUED])
def test_change_product_status_is_idempotent(
    db_session,
    category_factory,
    status,
):
    category = category_factory()
    product = create_product(
        db_session,
        category.category_id,
        status=status,
    )

    ProductService.change_product_status(
        product.product_id,
        status,
        db_session,
    )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product.product_id)

    assert persisted_product.product_id == product.product_id
    assert persisted_product.product_status == status
    assert persisted_product.product_name == "STATUS PRODUCT"
    assert persisted_product.category_id == category.category_id
    assert persisted_product.cost_price == Decimal("10.00")
    assert persisted_product.sale_value == Decimal("15.00")
    assert persisted_product.available_quantity == 3


@pytest.mark.parametrize(
    ("initial_status", "requested_status"),
    [
        (StatusEnum.INACTIVE, StatusEnum.DISCONTINUED),
        (StatusEnum.DISCONTINUED, StatusEnum.INACTIVE),
    ],
)
def test_change_product_status_rejects_invalid_transition(
    db_session,
    category_factory,
    initial_status,
    requested_status,
):
    category = category_factory()
    product = create_product(
        db_session,
        category.category_id,
        status=initial_status,
    )

    with pytest.raises(InvalidProductStatusTransitionError):
        ProductService.change_product_status(
            product.product_id,
            requested_status,
            db_session,
        )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product.product_id)

    assert persisted_product.product_id == product.product_id
    assert persisted_product.product_status == initial_status
    assert persisted_product.available_quantity == 3


def test_change_product_status_rejects_reactivation_with_inactive_category(
    db_session,
    category_factory,
):
    category = category_factory(status=StatusEnum.INACTIVE)
    product = create_product(
        db_session,
        category.category_id,
        status=StatusEnum.INACTIVE,
    )

    with pytest.raises(InvalidProductCategoryError):
        ProductService.change_product_status(
            product.product_id,
            StatusEnum.ACTIVE,
            db_session,
        )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product.product_id)

    assert persisted_product.product_id == product.product_id
    assert persisted_product.product_status == StatusEnum.INACTIVE
    assert persisted_product.category_id == category.category_id


def test_change_product_status_rejects_missing_product(db_session):
    with pytest.raises(ProductNotFoundError, match="Product not found."):
        ProductService.change_product_status(
            999999,
            StatusEnum.INACTIVE,
            db_session,
        )

    assert db_session.query(ProductModel).count() == 0


def test_change_product_status_rejects_unknown_status(
    db_session,
    category_factory,
):
    category = category_factory()
    product = create_product(db_session, category.category_id)

    with pytest.raises(ProductValidationError):
        ProductService.change_product_status(
            product.product_id,
            "UNKNOWN",
            db_session,
        )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product.product_id)

    assert persisted_product.product_id == product.product_id
    assert persisted_product.product_status == StatusEnum.ACTIVE


@pytest.mark.parametrize(
    ("status", "can_add_stock", "can_sell"),
    [
        (StatusEnum.ACTIVE, True, True),
        (StatusEnum.INACTIVE, False, False),
        (StatusEnum.DISCONTINUED, False, True),
    ],
)
def test_product_capabilities_follow_status(
    category_factory,
    status,
    can_add_stock,
    can_sell,
):
    category_model = category_factory()
    category = CategoryService.to_domain_category(category_model)
    product = Product(
        name="Capability Product",
        category=category,
        cost_price=Decimal("10.00"),
        sale_value=Decimal("15.00"),
        status=status,
    )

    assert product.can_add_stock() is can_add_stock
    assert product.can_sell() is can_sell
