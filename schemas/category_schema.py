from pydantic import BaseModel, ConfigDict
from domain.enums.status import StatusEnum

class CategoryCreateSchema(BaseModel):
  
  name: str

class CategoryResponseSchema(BaseModel):
  
  model_config = ConfigDict(from_attributes=True)
  
  category_id: int
  category_name: str
  category_status: StatusEnum