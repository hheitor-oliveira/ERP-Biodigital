from domain.inventory.product import Product
from models.inventory_models.product_model import ProductModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Sequence

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
    ) -> Sequence[ProductModel]:
        query = select(ProductModel)
        result = session.execute(query)
        products = result.scalars().all()

        return products