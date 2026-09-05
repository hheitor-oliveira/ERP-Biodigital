from decimal import Decimal

from fastapi import HTTPException
import pytest

from api.dependencies import get_authenticated_user, verify_access_token
from domain.enums.status import StatusEnum
from models.inventory_models.product_model import ProductModel
from models.user_model.user_model import UserModel


pytestmark = pytest.mark.contract


@pytest.fixture()
def authenticated_user() -> UserModel:
    return UserModel(
        user_id=1,
        user_name="Contract User",
        user_email="contract@example.com",
        user_password="hashed-password",
        admin=False,
    )


@pytest.fixture()
def authenticated_client(client, app, authenticated_user: UserModel):
    app.dependency_overrides[get_authenticated_user] = (
        lambda: authenticated_user
    )
    yield client
    app.dependency_overrides.pop(get_authenticated_user, None)


def unauthenticated_request() -> None:
    raise HTTPException(
        status_code=401,
        detail="Acesso negado, verifique a validade do token.",
    )


def test_create_product_returns_canonical_representation(
    authenticated_client,
    category_factory,
):
    category = category_factory()

    response = authenticated_client.post(
        "/product",
        json={
            "name": "  Example   Product  ",
            "category_id": category.category_id,
            "cost_price": "10.00",
            "sale_value": "15.00",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": response.json()["id"],
        "name": "EXAMPLE PRODUCT",
        "category": {
            "id": category.category_id,
            "name": "CATEGORIA VÁLIDA",
            "status": "ACTIVE",
        },
        "cost_price": "10.00",
        "sale_value": "15.00",
        "status": "ACTIVE",
        "available_quantity": 0,
    }


def test_product_endpoints_require_bearer_authentication(client, app):
    app.dependency_overrides[verify_access_token] = unauthenticated_request
    try:
        create_response = client.post(
            "/product",
            json={
                "name": "Unauthorized Product",
                "category_id": 1,
                "cost_price": "10.00",
                "sale_value": "15.00",
            },
        )
        list_response = client.get("/product")
        detail_response = client.get("/product/1")

        assert create_response.status_code == 401
        assert list_response.status_code == 401
        assert detail_response.status_code == 401
    finally:
        app.dependency_overrides.pop(verify_access_token, None)


def test_list_products_returns_empty_array_for_empty_catalog(
    authenticated_client,
):
    response = authenticated_client.get("/product")

    assert response.status_code == 200
    assert response.json() == []


def test_list_products_returns_complete_representations(
    authenticated_client,
    category_factory,
):
    category = category_factory()
    create_response = authenticated_client.post(
        "/product",
        json={
            "name": "  Listed   Product  ",
            "category_id": category.category_id,
            "cost_price": "10.00",
            "sale_value": "15.00",
        },
    )

    product_id = create_response.json()["id"]
    response = authenticated_client.get("/product")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": product_id,
            "name": "LISTED PRODUCT",
            "category": {
                "id": category.category_id,
                "name": "CATEGORIA VÁLIDA",
                "status": "ACTIVE",
            },
            "cost_price": "10.00",
            "sale_value": "15.00",
            "status": "ACTIVE",
            "available_quantity": 0,
        }
    ]


def test_get_product_returns_complete_representation(
    authenticated_client,
    category_factory,
):
    category = category_factory()
    create_response = authenticated_client.post(
        "/product",
        json={
            "name": "  Detail   Product  ",
            "category_id": category.category_id,
            "cost_price": "12.50",
            "sale_value": "20.00",
        },
    )

    product = create_response.json()
    response = authenticated_client.get(f"/product/{product['id']}")

    assert response.status_code == 200
    assert response.json() == product


def test_list_products_filters_by_case_insensitive_name(
    authenticated_client,
    category_factory,
):
    category = category_factory()
    for name in ("Blue Widget", "Red Widget"):
        response = authenticated_client.post(
            "/product",
            json={
                "name": name,
                "category_id": category.category_id,
                "cost_price": "10.00",
                "sale_value": "15.00",
            },
        )
        assert response.status_code == 201

    response = authenticated_client.get(
        "/product",
        params={"name": "blue   widget"},
    )

    assert response.status_code == 200
    assert [product["name"] for product in response.json()] == ["BLUE WIDGET"]


def test_list_products_filters_by_category_and_status(
    authenticated_client,
    category_factory,
    db_session,
):
    active_category = category_factory(name="Active Category")
    inactive_category = category_factory(
        name="Inactive Category",
        status=StatusEnum.INACTIVE,
    )

    first_response = authenticated_client.post(
        "/product",
        json={
            "name": "Active Category Product",
            "category_id": active_category.category_id,
            "cost_price": "10.00",
            "sale_value": "15.00",
        },
    )
    assert first_response.status_code == 201

    inactive_product = ProductModel(
        category_id=inactive_category.category_id,
        product_name="INACTIVE PRODUCT",
        cost_price=Decimal("20.00"),
        sale_value=Decimal("25.00"),
        available_quantity=0,
        product_status=StatusEnum.INACTIVE,
    )
    db_session.add(inactive_product)
    db_session.commit()

    response = authenticated_client.get(
        "/product",
        params={
            "category_id": inactive_category.category_id,
            "status": "INACTIVE",
        },
    )

    assert response.status_code == 200
    assert [product["name"] for product in response.json()] == ["INACTIVE PRODUCT"]


def test_list_products_combines_filters_and_returns_empty_array_for_no_match(
    authenticated_client,
    category_factory,
):
    category = category_factory()
    create_response = authenticated_client.post(
        "/product",
        json={
            "name": "Filtered Product",
            "category_id": category.category_id,
            "cost_price": "10.00",
            "sale_value": "15.00",
        },
    )
    assert create_response.status_code == 201

    response = authenticated_client.get(
        "/product",
        params={"name": "Other Product", "category_id": category.category_id},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_product_returns_not_found_for_unknown_identifier(
    authenticated_client,
):
    response = authenticated_client.get("/product/999999")

    assert response.status_code == 404
    assert "detail" in response.json()


def test_create_product_rejects_invalid_payload(
    authenticated_client,
    category_factory,
):
    category = category_factory()

    response = authenticated_client.post(
        "/product",
        json={
            "name": "   ",
            "category_id": category.category_id,
            "cost_price": "-1.00",
            "sale_value": "15.00",
        },
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_create_product_rejects_missing_and_inactive_categories(
    authenticated_client,
    category_factory,
):
    missing_category_response = authenticated_client.post(
        "/product",
        json={
            "name": "Missing Category Product",
            "category_id": 999999,
            "cost_price": "10.00",
            "sale_value": "15.00",
        },
    )
    inactive_category = category_factory(status=StatusEnum.INACTIVE)
    inactive_category_response = authenticated_client.post(
        "/product",
        json={
            "name": "Inactive Category Product",
            "category_id": inactive_category.category_id,
            "cost_price": "10.00",
            "sale_value": "15.00",
        },
    )

    assert missing_category_response.status_code == 404
    assert inactive_category_response.status_code == 400


def test_create_product_rejects_duplicate_canonical_name(
    authenticated_client,
    category_factory,
):
    category = category_factory()
    payload = {
        "name": "  Duplicate   Product ",
        "category_id": category.category_id,
        "cost_price": "10.00",
        "sale_value": "15.00",
    }

    first_response = authenticated_client.post("/product", json=payload)
    duplicate_response = authenticated_client.post(
        "/product",
        json={**payload, "name": "duplicate product"},
    )

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
