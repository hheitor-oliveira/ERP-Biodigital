from sqlalchemy.orm import Session
from models.inventory_models.product_model import ProductModel
from domain.inventory.product import Product

class ProductRepository:
    
    @classmethod
    def create_user(cls,
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