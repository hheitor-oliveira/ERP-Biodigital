from enum import Enum

class MovementType(Enum):
  '''Classe do tipo ENUM responsável por representar os tipos de movimentação do sistema.'''
  INPUT = "INPUT"
  OUTPUT = "OUTPUT"
  TRANSFER = "TRANSFER"