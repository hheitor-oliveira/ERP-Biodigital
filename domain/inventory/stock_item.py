# internal's imports
from domain.inventory.product import Product
from domain.inventory.stock import Stock

class StockItem:
  
  def __init__(self,
               stock: Stock,
               quantity: int = 1,
               products: list[Product] | None = None,
               id: int | None = None,
              ):
    
    self._products = products
    self._quantity = quantity
    self._id = id
    self._stock = stock
  
  @property
  def quantity(self) -> int:
    return self._quantity
  
  @property 
  def stock(self) -> Stock:
    return self.stock
  
  @property
  def products(self) -> list[Product] | None:
    return self._products
  
  @property
  def id(self) -> int | None:
    return self._id