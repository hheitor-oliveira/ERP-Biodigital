from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.product_schema import CreateProductSchema, ProductResponseSchema
from services.inventory.product_service import ProductService
from api.dependencies import get_session

inventory_router = APIRouter(prefix='/product',tags=['product'])

@inventory_router.post('/cadastrar')
async def cadastrar_produto(product: CreateProductSchema,
                   session: Session = Depends(get_session)):
  
  ProductService.create_product(product.product_name,
                                product.category_id,
                                product.cost_price,
                                product.sale_value,
                                session)
  
  
@inventory_router.get('/listar',
                      response_model=(list[ProductResponseSchema]))
async def listar_produtos(session: Session = Depends(get_session)):
  
  products_list = ProductService.list_products(session)
  
  return products_list