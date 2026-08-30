from pydantic import BaseModel, ConfigDict
from domain.enums.status import StatusEnum


class CategoryCreateSchema(BaseModel):
  name: str


class CategoryRenameSchema(BaseModel):
  name: str


class CategoryStatusUpdateSchema(BaseModel):
  status: StatusEnum


class CategoryResponseSchema(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  name: str
  status: StatusEnum