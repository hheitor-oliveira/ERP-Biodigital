# internal imports
from domain.inventory.product import Product

class MovementItem:
  """
  Classe responsável por representar cada item individualmente no sistema, para permitir a movimentação de vários itens na mesma movimentação. (Movement <- MovementItem)
  """
  def __init__(self,
               product: Product,
               quantity: int,
               id: int | None = None
               ) -> None:
    
    self._id = id
    self._product = product
    self._quantity = quantity
    
  @property
  def id(self) -> int | None:
    return self._id
  
  @property
  def quantity(self) -> int:
    return self._quantity
  
  @property
  def product(self) -> Product:
    return self.product
