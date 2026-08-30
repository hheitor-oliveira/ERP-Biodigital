from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.enums.status import StatusEnum
from domain.inventory.category import Category
from models.inventory_models.category_model import CategoryModel


class CategoryRepository:
    @classmethod
    def create_category(
        cls,
        category: Category,
        session: Session,
    ) -> CategoryModel:
        category_model = CategoryModel(
            category_name=category.name,
            category_status=category.status,
        )
        session.add(category_model)
        session.commit()
        session.refresh(category_model)
        return category_model

    @classmethod
    def find_all_categories(cls, session: Session) -> Sequence[CategoryModel]:
        query = select(CategoryModel).order_by(CategoryModel.category_name)
        result = session.execute(query)
        return result.scalars().all()

    @classmethod
    def find_category_by_id(
        cls,
        id: int,
        session: Session,
    ) -> CategoryModel | None:
        query = select(CategoryModel).where(CategoryModel.category_id == id)
        result = session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    def find_category_by_normalized_name(
        cls,
        name: str,
        session: Session,
    ) -> CategoryModel | None:
        query = select(CategoryModel).where(CategoryModel.category_name == name)
        result = session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    def update_category_name(
        cls,
        category_model: CategoryModel,
        new_name: str,
        session: Session,
    ) -> CategoryModel:
        category_model.category_name = new_name
        session.commit()
        session.refresh(category_model)
        return category_model

    @classmethod
    def update_category_status(
        cls,
        category_model: CategoryModel,
        new_status: StatusEnum,
        session: Session,
    ) -> CategoryModel:
        category_model.category_status = new_status
        session.commit()
        session.refresh(category_model)
        return category_model