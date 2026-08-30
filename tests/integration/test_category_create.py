import pytest

from models.inventory_models.category_model import CategoryModel


@pytest.mark.integration
def test_create_category_endpoint_returns_active_category(client, db_session):
    response = client.post("/category/create", json={"name": "Categoria Válida"})

    assert response.status_code == 200

    payload = response.json()
    assert payload["name"] == "CATEGORIA VÁLIDA"
    assert payload["status"] == "ACTIVE"
    assert payload["id"] is not None

    stored_category = db_session.query(CategoryModel).one()
    assert stored_category.category_name == "CATEGORIA VÁLIDA"
    assert stored_category.category_status.name == "ACTIVE"


@pytest.mark.integration
def test_create_category_endpoint_rejects_name_shorter_than_five_characters(
    client,
):
    response = client.post("/category/create", json={"name": "ABCD"})

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Category name must be between 5 and 32 characters."
    }
