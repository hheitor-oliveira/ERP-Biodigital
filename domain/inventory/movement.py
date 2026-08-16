# lib's imports
from datetime import datetime

# internal imports
from domain.enums.movement_type import MovementType
from domain.users.app_user import SystemUser
from domain.inventory.movement_item import MovementItem


class Movement:
    """
    Classe principal responsável por representar o registro de uma movimentação de produtos realizada no sistema.
    """

    def __init__(self,
                 user: SystemUser,
                 movement_type: MovementType,
                 movement_date: datetime,
                 items: list[MovementItem],
                 id: int | None = None
                 ):

        self._id = id
        self._items = items
        self._user = user
        self._movement_type = movement_type
        self._movement_date: datetime = movement_date

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def user(self) -> SystemUser:
        return self._user

    @property
    def items(self) -> list[MovementItem]:
        return self._items

    @property
    def movement_type(self) -> MovementType:
        return self._movement_type

    @property
    def movement_date(self) -> datetime:
        return self._movement_date
