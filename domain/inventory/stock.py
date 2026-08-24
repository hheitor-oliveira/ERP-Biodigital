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
  
  @classmethod
  def restore(cls,
              id: int,
              name: str,
              description: str,
              products: list[StockItem],
              status: StatusEnum
              ):
    
    stock = object.__new__(cls)
    
    stock._id = id
    stock._name = name
    stock._description = description
    stock._products = products
    stock._status = status
    
    return stock
   
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
  
  def change_name(self, new_name: str):
    self._name = new_name
    
  def change_description(self, new_description: str):
    self._description = new_description
    
  def change_status(self, new_status: StatusEnum):
    self._status = new_status
    
  def add_product(self, product: StockItem):
    if self._products is None:
        self._products = []
    self._products.append(product)
    
  def remove_product(self, product: StockItem):
    if product.id is None:
        raise TypeError('Produto não encontrado.')

    if self._products is None:
        self._products = []

    for stock_item in self._products:
        if stock_item.product.id == product.id:
            self._products.remove(stock_item)
            return

    raise ValueError('Produto não encontrado no estoque.')