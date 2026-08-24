# internal's imports
from domain.inventory.stock_item import StockItem
from domain.enums.status import StatusEnum

class Stock:
  
  def __init__(self,
               name: str,
               description: str,
               products: list[StockItem] | None = None,
               id: int | None = None,
               status: StatusEnum = StatusEnum.ACTIVE):
    
    self._name = name
    self._products = products
    self._status = status
    self._description = description
    self._id = id
    
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def description(self) -> str:
    return self._description
  
  @property
  def status(self) -> StatusEnum:
    return self._status
  
  @property
  def products(self) -> list[StockItem] | None:
    return self._products
  
  @property
  def id(self) -> int | None:
    return self._id