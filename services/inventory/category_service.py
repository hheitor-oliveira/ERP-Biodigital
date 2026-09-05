from __future__ import annotations

from sqlalchemy.orm import Session

from domain.enums.status import StatusEnum
from domain.exceptions import InvalidProductCategoryError
from domain.inventory.category import Category
from models.inventory_models.category_model import CategoryModel
from repository.inventory.category_repository import CategoryRepository


class CategoryService:
    @staticmethod
    def normalize_name(name: str) -> str:
        return " ".join(name.strip().split()).upper()

    @staticmethod
    def validate_name(name: str) -> str:
        normalized_name = CategoryService.normalize_name(name)

        if not normalized_name:
            raise ValueError("Category name is required.")

        if len(normalized_name) < 5 or len(normalized_name) > 32:
            raise ValueError("Category name must be between 5 and 32 characters.")

        return normalized_name

    @staticmethod
    def ensure_category_name_is_available(
        name: str,
        session: Session,
        exclude_id: int | None = None,
    ) -> None:
        normalized_name = CategoryService.validate_name(name)
        existing_category = CategoryRepository.find_category_by_normalized_name(
            normalized_name,
            session,
        )

        if existing_category is None:
            existing_category = next(
                (
                    category
                    for category in CategoryRepository.find_all_categories(session)
                    if CategoryService.normalize_name(category.category_name)
                    == normalized_name
                ),
                None,
            )

        if existing_category is not None and existing_category.category_id != exclude_id:
            raise ValueError("Category name already exists.")

    @staticmethod
    def create_category(name: str, session: Session) -> CategoryModel:
        CategoryService.ensure_category_name_is_available(name, session)
        normalized_name = CategoryService.validate_name(name)

        category = Category(name=normalized_name)
        return CategoryRepository.create_category(category, session)

    @staticmethod
    def to_domain_category(category_model: CategoryModel) -> Category:
        return Category.restore(
            name=category_model.category_name,
            id=category_model.category_id,
            status=category_model.category_status,
        )

    @staticmethod
    def require_active_category(
        category_model: CategoryModel | None,
    ) -> Category:
        if category_model is None:
            raise InvalidProductCategoryError("Category not found.")

        category = CategoryService.to_domain_category(category_model)

        if category.status != StatusEnum.ACTIVE:
            raise InvalidProductCategoryError(
                "Product requires an active category."
            )

        return category

    @staticmethod
    def to_domain_category_list(category_models: list[CategoryModel]) -> list[Category]:
        return [
            CategoryService.to_domain_category(category_model)
            for category_model in category_models
        ]

    @staticmethod
    def list_all_categories(session: Session) -> list[Category]:
        category_models = CategoryRepository.find_all_categories(session)
        return CategoryService.to_domain_category_list(list(category_models))

    @staticmethod
    def rename_category(
        category_id: int,
        new_name: str,
        session: Session,
    ) -> CategoryModel:
        category_model = CategoryRepository.find_category_by_id(category_id, session)
        if category_model is None:
            raise ValueError("Category not found.")

        CategoryService.ensure_category_name_is_available(
            new_name,
            session,
            exclude_id=category_id,
        )
        normalized_name = CategoryService.validate_name(new_name)
        return CategoryRepository.update_category_name(
            category_model,
            normalized_name,
            session,
        )

    @staticmethod
    def change_category_status(
        category_id: int,
        new_status: StatusEnum,
        session: Session,
    ) -> CategoryModel:
        category_model = CategoryRepository.find_category_by_id(category_id, session)
        if category_model is None:
            raise ValueError("Category not found.")

        return CategoryRepository.update_category_status(
            category_model,
            new_status,
            session,
        )