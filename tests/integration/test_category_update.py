import pytest

from repository.inventory.category_repository import CategoryRepository
from services.inventory.category_service import CategoryService


@pytest.mark.integration
def test_rename_category_updates_and_persists_normalized_name(
    db_session,
    category_factory,
):
    category = category_factory(name="Categoria Antiga")

    updated_category = CategoryService.rename_category(
        category.category_id,
        "  Categoria Nova  ",
        db_session,
    )

    assert updated_category.category_id == category.category_id
    assert updated_category.category_name == "CATEGORIA NOVA"

    db_session.expire_all()
    persisted_category = CategoryRepository.find_category_by_id(
        category.category_id,
        db_session,
    )

    assert persisted_category.category_name == "CATEGORIA NOVA"


@pytest.mark.integration
def test_rename_category_rejects_name_already_used_by_another_category(
    db_session,
    category_factory,
):
    category_factory(name="Categoria Existente")
    category_to_rename = category_factory(name="Categoria Original")

    with pytest.raises(ValueError, match="already exists"):
        CategoryService.rename_category(
            category_to_rename.category_id,
            "  categoria existente  ",
            db_session,
        )


@pytest.mark.integration
def test_rename_category_endpoint_rejects_name_shorter_than_five_characters(
    client,
    category_factory,
):
    category = category_factory()

    response = client.put(
        f"/category/{category.category_id}/rename",
        json={"name": "ABCD"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Category name must be between 5 and 32 characters."
    }
