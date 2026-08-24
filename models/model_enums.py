import enum

class ModelStatusEnum(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DISCONTINUED = "DISCONTINUED"

class ModelMovementTypeEnum(enum.Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    TRANSFER = "TRANSFER"