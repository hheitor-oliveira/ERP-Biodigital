# lib's imports
from decimal import Decimal
from typing import Any

# internal import's
from domain.enums.status import Status
from domain.inventory.category import Category

class Product:
    """
    A classe responsável por representar um produto do sistema e realizar operações relacionadas ao produto:
    """
    def __init__(self,
                 name: str,
                 category: Category,
                 cost_price: Decimal,
                 sale_value: Decimal,
                 available_quantity: int = 0,
                 status: Status = Status.ACTIVE,
                 id: int | None = None
                 ):
    
        self._id = id
        self._name = name
        self._category = category
        self._available_quantity = available_quantity
        self._sale_value = sale_value
        self._cost_price = cost_price
        self._status = status

    @classmethod
    def restore(cls,
                id: int,
                name: str,
                category: Category,
                available_quantity: int,
                sale_value: Decimal,
                cost_price: Decimal,
                status: str):
        
        product = object.__new__(cls)
        
        product._id = id
        product._name = name
        product._category = category
        product._available_quantity = available_quantity
        product._sale_value = sale_value
        product._cost_price = cost_price
        product._status = status
        
        return product

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def category(self) -> Category:
        return self._category
    
    @property
    def cost_price(self) -> Decimal:
        return self._cost_price
    
    @property
    def sale_value(self) -> Decimal:
        return self._sale_value
    
    @property
    def available_quantity(self) -> int:
        return self._available_quantity
    
    @property
    def status(self) -> Status:
        return self._status

    @property
    def id(self) -> int | None:
        return self._id

    def add_stock(self, 
                  quantity: int) -> None:
        self._available_quantity += quantity
    
    def change_name(self,
                    new_name: str) -> None:
        self._name = new_name
        
    def change_sale_value(self,
                          new_sale_value: Decimal) -> None:
        self._sale_value = new_sale_value
        
    def change_cost_price(self,
                          new_cost_price: Decimal) -> None:
        self._cost_price = new_cost_price
        
    def change_status(self,
                          new_status: Status) -> Any:
        self._status = new_status
        
    def change_category(self,
                        new_category: Category):
        self._category = new_category
        