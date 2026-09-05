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
        admin=True,
    )

    app.dependency_overrides[get_authenticated_user] = (
        lambda: authenticated_user
    )
    yield client
    app.dependency_overrides.pop(get_authenticated_user, None)


def product_payload(
    category_id: int,
    *,
    name: str,
    cost_price: str = "10.00",
    sale_value: str = "15.00",
) -> dict[str, object]:
    return {
        "name": name,
        "category_id": category_id,
        "cost_price": cost_price,
        "sale_value": sale_value,
    }


def test_delete_product_rejects_and_preserves_row(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory()
    create_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            name="Preserved Product",
        ),
    )
    product_id = create_response.json()["id"]

    delete_response = authenticated_integration_client.delete(
        f"/product/{product_id}"
    )
    query_response = authenticated_integration_client.get(
        f"/product/{product_id}"
    )

    persisted_product = db_session.get(ProductModel, product_id)

    assert delete_response.status_code == 405
    assert query_response.status_code == 200
    assert query_response.json()["id"] == product_id
    assert persisted_product is not None
    assert persisted_product.product_id == product_id


def test_failed_update_preserves_product_state(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory()
    create_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            name="Atomic Product",
        ),
    )
    product_id = create_response.json()["id"]

    response = authenticated_integration_client.patch(
        f"/product/{product_id}",
        json={"name": "Changed Product", "cost_price": "-1.00"},
    )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product_id)

    assert response.status_code == 400
    assert persisted_product.product_id == product_id
    assert persisted_product.product_name == "ATOMIC PRODUCT"
    assert persisted_product.cost_price == Decimal("10.00")
    assert persisted_product.sale_value == Decimal("15.00")
    assert persisted_product.category_id == category.category_id
    assert persisted_product.product_status == StatusEnum.ACTIVE
    assert persisted_product.available_quantity == 0


def test_duplicate_name_update_preserves_identifier_and_row(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory()
    first_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            name="First Product",
        ),
    )
    second_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            name="Second Product",
        ),
    )
    first_product_id = first_response.json()["id"]
    second_product_id = second_response.json()["id"]

    response = authenticated_integration_client.patch(
        f"/product/{second_product_id}",
        json={"name": " first   product "},
    )

    db_session.expire_all()
    first_product = db_session.get(ProductModel, first_product_id)
    second_product = db_session.get(ProductModel, second_product_id)

    assert response.status_code == 409
    assert first_product.product_id == first_product_id
    assert second_product.product_id == second_product_id
    assert first_product.product_name == "FIRST PRODUCT"
    assert second_product.product_name == "SECOND PRODUCT"
    assert db_session.query(ProductModel).count() == 2


def test_update_of_missing_product_does_not_create_row(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory()

    response = authenticated_integration_client.patch(
        "/product/999999",
        json=product_payload(
            category.category_id,
            name="Nonexistent Product",
        ),
    )

    assert response.status_code == 404
    assert db_session.query(ProductModel).count() == 0
