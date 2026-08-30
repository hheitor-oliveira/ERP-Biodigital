from domain.inventory.product import Product
from domain.inventory.category import Category
from decimal import Decimal
from repository.inventory.category_repository import CategoryRepository
from sqlalchemy.orm import Session
from repository.inventory.product_repository import ProductRepository

class ProductService():
  
  @classmethod
  def create_product(cls,
                     name: str,
                     category_id: int,
                     cost_price: Decimal,
                     sale_value: Decimal,
                     session: Session
                     ):
    
    category_model = CategoryRepository.find_category_by_id(category_id, session)
    
    if category_model is None:
      raise UnboundLocalError('Categoria não existe.')
    else:
      category = Category(category_model.category_name,
                          category_model.category_id,
                          category_model.category_status)
    
    product = Product(name,
                    category,
                    cost_price,
                    sale_value,
                    )
    
    ProductRepository.create_user(product, session)
    
  @classmethod
  def list_products(cls,
                    session: Session):
    
    product_list: list[Product] = []
    product_model_list = ProductRepository.list_products(session)
    
    for product_model in product_model_list:
      
      category_model = CategoryRepository.find_category_by_id(product_model.category_id, session)
          
      if category_model is None:
        raise UnboundLocalError('Categoria não encontrada.')
      else:
        category = Category(category_model.category_name,
                            category_model.category_id,
                            category_model.category_status)
      
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