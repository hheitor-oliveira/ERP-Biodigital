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
    self.id = id
    self.product = product
    self.quantity = quantity
