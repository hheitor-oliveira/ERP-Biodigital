from enum import Enum

class UserRoles(Enum):
  '''Classe do tipo ENUM responsável por representar os cargos existentes no sistema.'''
  ADMIN = "ADMIN"
  TECHNIQUE = "TECHNIQUE"
  ATTENDANT = "ATTENDANT"
  