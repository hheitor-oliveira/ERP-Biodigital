# lib's import
import typing
from domain.enums.status import StatusEnum

class Category:
  def __init__(self,
               name: str,
               id: int | None = None,
               status: StatusEnum = StatusEnum.ACTIVE):
    
    self._id = id
    self._name = name
    self._status = status
    
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def id(self) -> int | None:
    return self._id
  
  @property
  def status(self) -> StatusEnum:
    return self._status
  
  @classmethod
  def restore(cls,
              name: str,
              id: int | None) -> typing.Self:
    
    category = object.__new__(cls)
    
    category._name = name
    category._id = id
    
    return category