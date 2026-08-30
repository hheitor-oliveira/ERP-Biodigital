import pytest

from domain.enums.status import StatusEnum
from domain.inventory.category import Category
from repository.inventory.category_repository import CategoryRepository
from services.inventory.category_service import CategoryService


@pytest.mark.contract
def test_validate_name_accepts_valid_category_name():
    assert CategoryService.validate_name("  Categoria Válida  ") == "CATEGORIA VÁLIDA"


@pytest.mark.contract
@pytest.mark.parametrize("invalid_name", ["", "   ", "\n\t "])
def test_validate_name_rejects_blank_or_whitespace_names(invalid_name):
    with pytest.raises(ValueError, match="Category name is required."):
        CategoryService.validate_name(invalid_name)


@pytest.mark.contract
@pytest.mark.parametrize(
    "invalid_name",
    [
        "abcd",
        "a" * 33,
    ],
)
def test_validate_name_rejects_out_of_range_lengths(invalid_name):
    with pytest.raises(ValueError, match="Category name must be between 5 and 32 characters."):
        CategoryService.validate_name(invalid_name)


@pytest.mark.contract
def test_create_category_persists_active_category(db_session):
    category = Category(name="Categoria Válida")

    created_model = CategoryRepository.create_category(category, db_session)

    assert created_model.category_name == "CATEGORIA VÁLIDA"
    assert created_model.category_status == StatusEnum.ACTIVE


@pytest.mark.contract
def test_duplicate_category_name_is_rejected(category_factory, db_session):
    category_factory(name="CATEGORIA VÁLIDA")

    with pytest.raises(ValueError, match="Category name already exists."):
        CategoryService.ensure_category_name_is_available("categoria válida", db_session)
