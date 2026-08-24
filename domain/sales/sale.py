# lib's imports
from datetime import datetime
from decimal import Decimal

# internals imports
from domain.users.app_user import AppUser
from domain.sales.sale_item import SaleItem
from domain.sales.sale_payment import SalePayment

class Sale:
    '''Classe responsável por representar uma venda no sistema, além de representar operações relacionadas a uma venda.
    Essa classe possui o conceito de State Machine.'''
    def __init__(self,
                 id: int,
                 items: list[SaleItem],
                 sale_payment: list[SalePayment],
                 user: AppUser,
                 total_value: Decimal,
                 discount_type: int,
                 discount_value: Decimal,
                 sale_date: datetime):

        self._id = id
        self._items = items
        self._sale_payment = sale_payment
        self._user = user
        self._total_value = total_value
        self._discount_type = discount_type
        self._discount_value = discount_value
        self._sale_date = sale_date