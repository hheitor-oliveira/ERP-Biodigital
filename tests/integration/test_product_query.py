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


def create_product(
    authenticated_integration_client,
    category_id: int,
    *,
    name: str,
    cost_price: str = "10.00",
    sale_value: str = "15.00",
) -> dict[str, object]:
    response = authenticated_integration_client.post(
        "/product",
        json=product_payload(
            category_id,
            name=name,
            cost_price=cost_price,
            sale_value=sale_value,
        ),
    )

    assert response.status_code == 201
    return response.json()


def add_product(
    db_session,
    category_id: int,
    *,
    name: str,
    status: StatusEnum,
    cost_price: str = "10.00",
    sale_value: str = "15.00",
) -> ProductModel:
    product = ProductModel(
        category_id=category_id,
        product_name=name,
        cost_price=Decimal(cost_price),
        sale_value=Decimal(sale_value),
        available_quantity=0,
        product_status=status,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


def test_list_products_returns_empty_array_for_empty_catalog(
    authenticated_integration_client,
):
    response = authenticated_integration_client.get("/product")

    assert response.status_code == 200
    assert response.json() == []


def test_list_products_returns_complete_persisted_representation(
    authenticated_integration_client,
    category_factory,
):
    category = category_factory()
    product = create_product(
        authenticated_integration_client,
        category.category_id,
        name="  Listed   Product  ",
        cost_price="12.50",
        sale_value="20.00",
    )

    response = authenticated_integration_client.get("/product")

    assert response.status_code == 200
    assert response.json() == [product]


def test_get_product_returns_complete_persisted_representation(
    authenticated_integration_client,
    category_factory,
):
    category = category_factory()
    product = create_product(
        authenticated_integration_client,
        category.category_id,
        name="  Detail   Product  ",
        cost_price="12.50",
        sale_value="20.00",
    )

    response = authenticated_integration_client.get(f"/product/{product['id']}")

    assert response.status_code == 200
    assert response.json() == product


def test_list_products_filters_by_case_insensitive_canonical_name(
    authenticated_integration_client,
    category_factory,
):
    category = category_factory()
    create_product(
        authenticated_integration_client,
        category.category_id,
        name="Blue Widget",
    )
    create_product(
        authenticated_integration_client,
        category.category_id,
        name="Red Widget",
    )

    response = authenticated_integration_client.get(
        "/product",
        params={"name": "blue   widget"},
    )

    assert response.status_code == 200
    assert [product["name"] for product in response.json()] == ["BLUE WIDGET"]


def test_list_products_filters_by_category(
    authenticated_integration_client,
    category_factory,
):
    first_category = category_factory(name="First Category")
    second_category = category_factory(name="Second Category")
    create_product(
        authenticated_integration_client,
        first_category.category_id,
        name="First Category Product",
    )
    create_product(
        authenticated_integration_client,
        second_category.category_id,
        name="Second Category Product",
    )

    response = authenticated_integration_client.get(
        "/product",
        params={"category_id": first_category.category_id},
    )

    assert response.status_code == 200
    assert [product["name"] for product in response.json()] == [
        "FIRST CATEGORY PRODUCT"
    ]


def test_list_products_filters_by_status(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory()
    add_product(
        db_session,
        category.category_id,
        name="INACTIVE PRODUCT",
        status=StatusEnum.INACTIVE,
    )
    add_product(
        db_session,
        category.category_id,
        name="DISCONTINUED PRODUCT",
        status=StatusEnum.DISCONTINUED,
    )

    response = authenticated_integration_client.get(
        "/product",
        params={"status": "INACTIVE"},
    )

    assert response.status_code == 200
    assert [product["name"] for product in response.json()] == [
        "INACTIVE PRODUCT"
    ]


def test_list_products_combines_category_and_status_filters(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    matching_category = category_factory(name="Matching Category")
    other_category = category_factory(name="Other Category")
    add_product(
        db_session,
        matching_category.category_id,
        name="MATCHING INACTIVE PRODUCT",
        status=StatusEnum.INACTIVE,
    )
    add_product(
        db_session,
        matching_category.category_id,
        name="MATCHING ACTIVE PRODUCT",
        status=StatusEnum.ACTIVE,
    )
    add_product(
        db_session,
        other_category.category_id,
        name="OTHER INACTIVE PRODUCT",
        status=StatusEnum.INACTIVE,
    )

    response = authenticated_integration_client.get(
        "/product",
        params={
            "category_id": matching_category.category_id,
            "status": "INACTIVE",
        },
    )

    assert response.status_code == 200
    assert [product["name"] for product in response.json()] == [
        "MATCHING INACTIVE PRODUCT"
    ]


def test_list_products_returns_empty_array_for_combined_filters_without_match(
    authenticated_integration_client,
    category_factory,
    db_session,
):
    category = category_factory()
    add_product(
        db_session,
        category.category_id,
        name="FILTERED PRODUCT",
        status=StatusEnum.ACTIVE,
    )

    response = authenticated_integration_client.get(
        "/product",
        params={
            "name": "Other Product",
            "category_id": category.category_id,
            "status": "ACTIVE",
        },
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_product_returns_not_found_for_unknown_identifier(
    authenticated_integration_client,
):
    response = authenticated_integration_client.get("/product/999999")

    assert response.status_code == 404
    assert "detail" in response.json()
