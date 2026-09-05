from domain.inventory.product import Product
from domain.enums.status import StatusEnum
from models.inventory_models.category_model import CategoryModel
from models.inventory_models.product_model import ProductModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Sequence


ProductWithCategory = tuple[ProductModel, CategoryModel]


class ProductRepository:
    @classmethod
    def create_product(
        cls,
        product: Product,
        session: Session,
    ) -> ProductModel:
        product_model = ProductModel(
            product_name=product.name,
            category_id=product.category.id,
            cost_price=product.cost_price,
            sale_value=product.sale_value,
            available_quantity=product.available_quantity,
            product_status=product.status,
        )

        try:
            session.add(product_model)
            session.commit()
            session.refresh(product_model)
        except SQLAlchemyError:
            session.rollback()
            raise

        return product_model

    @classmethod
    def list_products(
        cls,
        session: Session,
        *,
        name: str | None = None,
        category_id: int | None = None,
        status: StatusEnum | None = None,
    ) -> Sequence[ProductWithCategory]:
        return cls._query_products_with_categories(
            session,
            product_name=name,
            category_id=category_id,
            status=status,
        )

    @classmethod
    def _query_products_with_categories(
        cls,
        session: Session,
        *,
        product_id: int | None = None,
        product_name: str | None = None,
        category_id: int | None = None,
        status: StatusEnum | None = None,
    ) -> Sequence[ProductWithCategory]:
        query = (
            select(ProductModel, CategoryModel)
            .join(
                CategoryModel,
                ProductModel.category_id == CategoryModel.category_id,
            )
            .order_by(ProductModel.product_id)
        )

        if product_id is not None:
            query = query.where(ProductModel.product_id == product_id)

        if product_name is not None:
            query = query.where(ProductModel.product_name == product_name)

        if category_id is not None:
            query = query.where(ProductModel.category_id == category_id)

        if status is not None:
            query = query.where(ProductModel.product_status == status)

        return session.execute(query).tuples().all()

    @classmethod
    def find_product_by_id(
        cls,
        product_id: int,
        session: Session,
    ) -> ProductWithCategory | None:
        result = cls._query_products_with_categories(
            session,
            product_id=product_id,
        )
        return result[0] if result else None

    @classmethod
    def find_product_by_canonical_name(
        cls,
        name: str,
        session: Session,
    ) -> ProductWithCategory | None:
        result = cls._query_products_with_categories(
            session,
            product_name=name,
        )
        return result[0] if result else None

    @classmethod
    def find_products_by_category(
        cls,
        category_id: int,
        session: Session,
    ) -> Sequence[ProductWithCategory]:
        return cls._query_products_with_categories(
            session,
            category_id=category_id,
        )

    @classmethod
    def find_products_by_status(
        cls,
        status: StatusEnum,
        session: Session,
    ) -> Sequence[ProductWithCategory]:
        return cls._query_products_with_categories(
            session,
            status=status,
        )