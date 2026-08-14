from enum import Enum

class ProductStatus(Enum):
  '''Classe do tipo ENUM responsável por representar os status existentes dos produtos do sistema.'''
  ACTIVE = "ACTIVE"
  INACTIVE = "INACTIVE"
  DISCONTINUED = "DISCONTINUED"
  