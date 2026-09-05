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


@pytest.fixture()
def non_admin_integration_client(client, app):
    authenticated_user = UserModel(
        user_id=2,
        user_name="Integration Non-Admin User",
        user_email="integration-non-admin@example.com",
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

    assert response.status_code == 422
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


def test_update_product_name_preserves_omitted_fields(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory()
    create_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            name="Original Product",
            cost_price="12.50",
            sale_value="20.00",
        ),
    )
    product_id = create_response.json()["id"]

    response = authenticated_integration_client.patch(
        f"/product/{product_id}",
        json={"name": "  Updated   Product  "},
    )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product_id)

    assert response.status_code == 200
    assert response.json()["name"] == "UPDATED PRODUCT"
    assert response.json()["category"]["id"] == category.category_id
    assert response.json()["cost_price"] == "12.50"
    assert response.json()["sale_value"] == "20.00"
    assert persisted_product.product_name == "UPDATED PRODUCT"
    assert persisted_product.category_id == category.category_id
    assert persisted_product.cost_price == Decimal("12.50")
    assert persisted_product.sale_value == Decimal("20.00")


def test_update_product_multiple_fields_returns_complete_representation(
    authenticated_integration_client,
    category_factory,
):
    original_category = category_factory(name="Original Category")
    replacement_category = category_factory(name="Replacement Category")
    create_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            original_category.category_id,
            name="Original Product",
        ),
    )
    product_id = create_response.json()["id"]

    response = authenticated_integration_client.patch(
        f"/product/{product_id}",
        json={
            "name": "  Updated   Product  ",
            "category_id": replacement_category.category_id,
            "cost_price": "12.50",
            "sale_value": "20.00",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": product_id,
        "name": "UPDATED PRODUCT",
        "category": {
            "id": replacement_category.category_id,
            "name": "REPLACEMENT CATEGORY",
            "status": "ACTIVE",
        },
        "cost_price": "12.50",
        "sale_value": "20.00",
        "status": "ACTIVE",
        "available_quantity": 0,
    }


def test_non_admin_cannot_update_product(
    non_admin_integration_client,
    category_factory,
):
    category = category_factory()
    create_response = non_admin_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            name="Protected Product",
        ),
    )
    product_id = create_response.json()["id"]

    response = non_admin_integration_client.patch(
        f"/product/{product_id}",
        json={"name": "Unauthorized Update"},
    )

    assert response.status_code == 401


@pytest.mark.parametrize(
    "payload",
    [
        {"cost_price": "-1.00"},
        {"sale_value": "10.001"},
    ],
    ids=["negative-price", "excessive-precision"],
)
def test_update_product_rejects_invalid_prices(
    authenticated_integration_client,
    category_factory,
    payload,
):
    category = category_factory()
    create_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            name="Price Product",
        ),
    )
    product_id = create_response.json()["id"]

    response = authenticated_integration_client.patch(
        f"/product/{product_id}",
        json=payload,
    )

    assert response.status_code == 422


def test_update_product_rejects_duplicate_canonical_name(
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
    assert second_product.product_name == "SECOND PRODUCT"


def test_update_product_rejects_missing_category_without_changes(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory()
    create_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category.category_id,
            name="Category Product",
        ),
    )
    product_id = create_response.json()["id"]

    response = authenticated_integration_client.patch(
        f"/product/{product_id}",
        json={"category_id": 999999},
    )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product_id)

    assert response.status_code == 404
    assert persisted_product.product_id == product_id
    assert persisted_product.product_name == "CATEGORY PRODUCT"
    assert persisted_product.category_id == category.category_id


def test_update_product_rejects_inactive_category_without_changes(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    active_category = category_factory(name="Active Category")
    inactive_category = category_factory(
        name="Inactive Category",
        status=StatusEnum.INACTIVE,
    )
    create_response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            active_category.category_id,
            name="Category Product",
        ),
    )
    product_id = create_response.json()["id"]

    response = authenticated_integration_client.patch(
        f"/product/{product_id}",
        json={"category_id": inactive_category.category_id},
    )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product_id)

    assert response.status_code == 400
    assert persisted_product.product_id == product_id
    assert persisted_product.category_id == active_category.category_id


def test_update_product_preserves_identifier_and_state_after_atomic_failure(
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
            cost_price="10.00",
            sale_value="15.00",
        ),
    )
    product_id = create_response.json()["id"]

    response = authenticated_integration_client.patch(
        f"/product/{product_id}",
        json={"name": "Changed Product", "cost_price": "-1.00"},
    )

    db_session.expire_all()
    persisted_product = db_session.get(ProductModel, product_id)

    assert response.status_code == 422
    assert persisted_product.product_id == product_id
    assert persisted_product.product_name == "ATOMIC PRODUCT"
    assert persisted_product.cost_price == Decimal("10.00")
    assert persisted_product.sale_value == Decimal("15.00")
    assert persisted_product.category_id == category.category_id
    assert persisted_product.product_status == StatusEnum.ACTIVE
    assert persisted_product.available_quantity == 0
