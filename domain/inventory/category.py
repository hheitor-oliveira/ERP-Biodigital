from typing import Self
from typing import Any

class Category:
  def __init__(self,
               name: str,
               id: Any | int = None):
    self._id = id
    self._name = name
    
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def id(self) -> int:
    return self._id
  
  @classmethod
  def restore(cls,
              name: str,
              id: int | None) -> Self:
    
    category = object.__new__(cls)
    
    category._name = name
    category._id = id
    
    return category