# lib's import
import typing

class Category:
  def __init__(self,
               name: str,
               id: int | None = None):
    self._id = id
    self._name = name
    
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def id(self) -> int | None:
    return self._id
  
  @classmethod
  def restore(cls,
              name: str,
              id: int | None) -> typing.Self:
    
    category = object.__new__(cls)
    
    category._name = name
    category._id = id
    
    return category