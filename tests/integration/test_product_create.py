from decimal import Decimal

import pytest

from api.dependencies import get_authenticated_user
from domain.enums.status import StatusEnum
from models.inventory_models.product_model import ProductModel
from models.user_model.user_model import UserModel


pytestmark = pytest.mark.integration


@pytest.fixture()
def authenticated_integration_client(client, app):
    authenticated_user = UserModel(
        user_id=1,
        user_name="Integration User",
        user_email="integration@example.com",
        user_password="hashed-password",
        admin=False,
    )

    app.dependency_overrides[get_authenticated_user] = (
        lambda: authenticated_user
    )
    yield client
    app.dependency_overrides.pop(get_authenticated_user, None)


def product_payload(
    category_id: int,
    *,
    name: str = "  Example   Product  ",
    cost_price: str = "10.00",
    sale_value: str = "15.00",
) -> dict[str, object]:
    return {
        "name": name,
        "category_id": category_id,
        "cost_price": cost_price,
        "sale_value": sale_value,
    }


def test_create_product_persists_valid_canonical_product(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory()

    response = authenticated_integration_client.post(
        "/product",
        json=product_payload(category.category_id),
    )

    assert response.status_code == 201
    assert response.json()["name"] == "EXAMPLE PRODUCT"
    assert response.json()["status"] == "ACTIVE"
    assert response.json()["available_quantity"] == 0

    stored_product = db_session.query(ProductModel).one()
    assert stored_product.product_name == "EXAMPLE PRODUCT"
    assert stored_product.category_id == category.category_id
    assert stored_product.cost_price == Decimal("10.00")
    assert stored_product.sale_value == Decimal("15.00")
    assert stored_product.product_status == StatusEnum.ACTIVE
    assert stored_product.available_quantity == 0


def test_create_product_rejects_missing_category(
    authenticated_integration_client,
    db_session,
):
    response = authenticated_integration_client.post(
        "/product",
        json=product_payload(999999),
    )

    assert response.status_code == 404
    assert db_session.query(ProductModel).count() == 0


def test_create_product_rejects_inactive_category(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory(status=StatusEnum.INACTIVE)

    response = authenticated_integration_client.post(
        "/product",
        json=product_payload(category.category_id),
    )

    assert response.status_code == 400
    assert db_session.query(ProductModel).count() == 0


@pytest.mark.parametrize(
    ("missing_field",),
    [
        ("name",),
        ("category_id",),
        ("cost_price",),
        ("sale_value",),
    ],
)
def test_create_product_rejects_missing_required_fields(
    authenticated_integration_client,
    category_factory,
    missing_field: str,
):
    category = category_factory()
    payload = product_payload(category.category_id)
    payload.pop(missing_field)

    response = authenticated_integration_client.post(
        "/product",
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("cost_price", "sale_value"),
    [
        ("-1.00", "15.00"),
        ("10.00", "-15.00"),
    ],
)
def test_create_product_rejects_negative_prices(
    authenticated_integration_client,
    category_factory,
    cost_price: str,
    sale_value: str,
):
    category = category_factory()

    response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            cost_price=cost_price,
            sale_value=sale_value,
        ),
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("cost_price", "sale_value"),
    [
        ("10.001", "15.00"),
        ("10.00", "15.001"),
    ],
)
def test_create_product_rejects_excessive_decimal_scale(
    authenticated_integration_client,
    category_factory,
    cost_price: str,
    sale_value: str,
):
    category = category_factory()

    response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            cost_price=cost_price,
            sale_value=sale_value,
        ),
    )

    assert response.status_code == 422


def test_create_product_rejects_duplicate_canonical_name(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory()

    first_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(category.category_id),
    )
    duplicate_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            name="example product",
            cost_price="20.00",
            sale_value="25.00",
        ),
    )

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert db_session.query(ProductModel).count() == 1
