from fastapi import HTTPException
import pytest

from api.dependencies import get_authenticated_user, verify_access_token
from domain.enums.status import StatusEnum
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
            "name": category.category_name,
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

        assert create_response.status_code == 401
        assert list_response.status_code == 401
    finally:
        app.dependency_overrides.pop(verify_access_token, None)


def test_list_products_returns_empty_array_for_empty_catalog(
    authenticated_client,
):
    response = authenticated_client.get("/product")

    assert response.status_code == 200
    assert response.json() == []


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

    assert response.status_code == 400
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
