from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from domain.enums.status import StatusEnum

class CreateProductSchema(BaseModel):
  
  product_name: str
  category_id: int
  cost_price: Decimal
  sale_value: Decimal

class CategoryResponse(BaseModel):
  
  model_config = ConfigDict(from_attributes=True)
  
  id: int
  name: str
  status: StatusEnum

class ProductResponseSchema(BaseModel):
  
  model_config = ConfigDict(from_attributes=True)
  
  id: int
  name: str
  category: CategoryResponse
  cost_price: Decimal
  sale_value: Decimal
  status: StatusEnum
  available_quantity: int