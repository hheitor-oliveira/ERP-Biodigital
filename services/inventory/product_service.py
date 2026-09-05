from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.enums.status import StatusEnum
from domain.exceptions import (
    DuplicateProductNameError,
    ProductNotFoundError,
)
from domain.inventory.product import Product
from models.inventory_models.category_model import CategoryModel
from models.inventory_models.product_model import ProductModel
from repository.inventory.category_repository import CategoryRepository
from repository.inventory.product_repository import ProductRepository, ProductWithCategory
from schemas.product_schema import ProductResponseSchema
from services.inventory.category_service import CategoryService


class ProductService:
    @classmethod
    def delete_product(
        cls,
        product_id: int,
        session: Session,
    ) -> None:
        ProductRepository.delete_product(product_id, session)

    @staticmethod
    def _to_domain_product(
        product_model: ProductModel,
        category_model: CategoryModel,
    ) -> Product:
        category = CategoryService.to_domain_category(category_model)

        if product_model.product_id is None:
            raise ValueError("Persisted product must have an identifier.")

        return Product.restore(
            id=product_model.product_id,
            name=product_model.product_name,
            category=category,
            available_quantity=product_model.available_quantity,
            sale_value=product_model.sale_value,
            cost_price=product_model.cost_price,
            status=product_model.product_status,
        )

    @classmethod
    def _to_response(
        cls,
        product_with_category: ProductWithCategory,
    ) -> ProductResponseSchema:
        product_model, category_model = product_with_category
        product = cls._to_domain_product(product_model, category_model)

        return ProductResponseSchema.from_model(
            product_model=product_model,
            category=product.category,
        )

    @classmethod
    def create_product(
        cls,
        name: str,
        category_id: int,
        cost_price: Decimal,
        sale_value: Decimal,
        session: Session,
    ) -> ProductModel:
        category_model = CategoryRepository.find_category_by_id(
            category_id,
            session,
        )
        category = CategoryService.require_active_category(category_model)

        product = Product(
            name=name,
            category=category,
            cost_price=cost_price,
            sale_value=sale_value,
            available_quantity=0,
            status=StatusEnum.ACTIVE,
        )

        try:
            return ProductRepository.create_product(product, session)
        except IntegrityError as exc:
            raise DuplicateProductNameError(
                "A product with this canonical name already exists."
            ) from exc

    @classmethod
    def update_product(
        cls,
        product_id: int,
        *,
        name: str | None = None,
        category_id: int | None = None,
        cost_price: Decimal | None = None,
        sale_value: Decimal | None = None,
        session: Session,
    ) -> ProductModel:
        product_row = ProductRepository.find_product_by_id(product_id, session)

        if product_row is None:
            raise ProductNotFoundError("Product not found.")

        product_model, category_model = product_row

        if category_id is None:
            category = CategoryService.to_domain_category(category_model)
        else:
            replacement_category_model = CategoryRepository.find_category_by_id(
                category_id,
                session,
            )
            category = CategoryService.require_active_category(
                replacement_category_model,
            )

        prospective_product = Product(
            id=product_id,
            name=product_model.product_name if name is None else name,
            category=category,
            cost_price=(
                product_model.cost_price
                if cost_price is None
                else cost_price
            ),
            sale_value=(
                product_model.sale_value
                if sale_value is None
                else sale_value
            ),
            available_quantity=product_model.available_quantity,
            status=product_model.product_status,
        )

        try:
            return ProductRepository.update_product(
                product_model,
                prospective_product,
                session,
            )
        except IntegrityError as exc:
            raise DuplicateProductNameError(
                "A product with this canonical name already exists."
            ) from exc

    @classmethod
    def change_product_status(
        cls,
        product_id: int,
        new_status: StatusEnum,
        session: Session,
    ) -> ProductModel:
        product_row = ProductRepository.find_product_by_id(
            product_id,
            session,
        )

        if product_row is None:
            raise ProductNotFoundError("Product not found.")

        product_model, category_model = product_row
        product = cls._to_domain_product(product_model, category_model)
        product.change_status(new_status)

        return ProductRepository.update_product_status(
            product_model,
            product.status,
            session,
        )

    @classmethod
    def list_products(
        cls,
        session: Session,
        *,
        name: str | None = None,
        category_id: int | None = None,
        status: StatusEnum | None = None,
    ) -> list[ProductResponseSchema]:
        product_rows = ProductRepository.list_products(
            session,
            name=name,
            category_id=category_id,
            status=status,
        )
        return [cls._to_response(row) for row in product_rows]

    @classmethod
    def find_product_by_id(
        cls,
        product_id: int,
        session: Session,
    ) -> ProductResponseSchema | None:
        product_row = ProductRepository.find_product_by_id(
            product_id,
            session,
        )

        if product_row is None:
            return None

        return cls._to_response(product_row)