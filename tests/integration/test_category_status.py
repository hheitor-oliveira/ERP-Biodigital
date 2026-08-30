import pytest
from decimal import Decimal

from domain.enums.status import StatusEnum
from models.inventory_models.product_model import ProductModel
from repository.inventory.category_repository import CategoryRepository
from services.inventory.category_service import CategoryService


@pytest.mark.integration
def test_inactivate_category_preserves_linked_product_association(
    db_session,
    category_factory,
):
    category = category_factory(name="Categoria de Produto")
    product = ProductModel(
        category_id=category.category_id,
        product_name="Produto Associado",
        cost_price=Decimal("10.00"),
        sale_value=Decimal("15.00"),
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    updated_category = CategoryService.change_category_status(
        category.category_id,
        StatusEnum.INACTIVE,
        db_session,
    )

    assert updated_category.category_id == category.category_id
    assert updated_category.category_status == StatusEnum.INACTIVE

    db_session.expire_all()
    persisted_category = CategoryRepository.find_category_by_id(
        category.category_id,
        db_session,
    )
    persisted_product = db_session.get(ProductModel, product.product_id)

    assert persisted_category.category_status == StatusEnum.INACTIVE
    assert persisted_product.category_id == category.category_id


@pytest.mark.integration
def test_change_category_status_returns_not_found_for_missing_category(client):
    response = client.patch(
        "/category/999/status",
        json={"status": "INACTIVE"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found."}


@pytest.mark.integration
def test_change_category_status_rejects_unknown_status(client, category_factory):
    category = category_factory()

    response = client.patch(
        f"/category/{category.category_id}/status",
        json={"status": "UNKNOWN"},
    )

    assert response.status_code == 422
