from enum import Enum

class Method(Enum):
  '''Classe do tipo ENUM responsável por representar as formas de pagamento do sistema.'''
  PIX = "PIX"
  CREDIT_CARD = "CREDIT_CARD"
  DEBIT_CARD = "DEBIT_CARD"
  CASH = "CASH"
  OTHER = "OTHER"