from sqlalchemy.orm import Session
from repository.inventory.product_repository import ProductRepository
from domain.inventory.product import Product

class ProductService:
  '''Responsável por coordenar todos os processos da Classe Product no sistema.'''

  @staticmethod
  def get_all_products(session: Session):
    '''Retorna todos os produtos cadastrados no sistema.'''

    try:
      products = ProductRepository.get_all_products(session)

    except Exception as e:
      raise RuntimeError(f'Erro ao buscar produtos: {str(e)}')

    return products