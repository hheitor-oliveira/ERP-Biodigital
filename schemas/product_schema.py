from pydantic import BaseModel
from decimal import Decimal

class CreateProductSchema(BaseModel):
  
  product_name: str
  category_id: int
  cost_price: Decimal
  sale_value: Decimal

class ProductResponseSchema(BaseModel):
  id: int
  name: str
  category: str
  cost_price: Decimal
  sale_value: Decimal
  status: str
  available_quantity: int