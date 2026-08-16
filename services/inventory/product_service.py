# lib's import's
from decimal import Decimal

# internal import's
from domain.inventory.product import Product
from domain.inventory.category import Category
from repository.inventory.product_repository import ProductRepository

class ProductService:
  '''Responsável por coordenar todos os processos da Classe Product no sistema.'''
  
  def __init__(self):
    self._product_repository = ProductRepository()
  
  def create_product(self, 
                     name: str,
                     category: Category,
                     cost_price: Decimal,
                     sale_value: Decimal) -> Product:
    
    product = Product(name, category, cost_price, sale_value)
    
    self._product_repository.save(product)
    
    return product
  
  def save_information(self, product: Product) -> None:
    
    self._product_repository.save_a_edit(product)

  def list_products(self) -> list[Product]:
     
     products = self._product_repository.reconstruct()
     
     return products
   