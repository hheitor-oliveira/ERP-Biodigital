from sqlalchemy.orm import Session
from sqlalchemy import select
from models.inventory_models.product_model import ProductModel
from domain.inventory.product import Product
from typing import Sequence

class ProductRepository:
    
    @classmethod
    def create_product(cls,
                    product: Product,
                    session: Session):
      
      product_model = ProductModel(
        product_name = product.name,
        category_id = product.category.id,
        cost_price = product.cost_price,
        sale_value = product.sale_value,
      )
      
      session.add(product_model)
      session.commit()
      
    @classmethod
    def list_products(cls,
                      session: Session) -> Sequence[ProductModel]:
      
      query = select(ProductModel)
      result = session.execute(query)
      products = result.scalars().all()
      
      return products