from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.enums.status import StatusEnum
from domain.exceptions import DuplicateProductNameError
from domain.inventory.product import Product
from models.inventory_models.product_model import ProductModel
from repository.inventory.category_repository import CategoryRepository
from repository.inventory.product_repository import ProductRepository
from services.inventory.category_service import CategoryService


class ProductService:
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
    def list_products(cls,
                      session: Session):

        product_list: list[Product] = []
        product_model_list = ProductRepository.list_products(session)

        for product_model in product_model_list:

            category_model = CategoryRepository.find_category_by_id(product_model.category_id, session)

            if category_model is None:
                raise UnboundLocalError('Categoria não encontrada.')

            category = CategoryService.to_domain_category(category_model)

            product = Product(
                product_model.product_name,
                category,
                product_model.cost_price,
                product_model.sale_value,
                product_model.available_quantity,
                product_model.product_status,
                product_model.product_id
            )

            product_list.append(product)

            if len(product_list) == 0:
                raise UnboundLocalError('Nenhum produto cadastrado')
            else:
                return product_list