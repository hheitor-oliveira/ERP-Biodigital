from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.inventory_models.product_model import ProductModel
from schemas.product_schema import CreateProductSchema, ProductResponseSchema
from services.inventory.product_service import ProductService
from api.dependencies import get_authenticated_user, get_session
from domain.exceptions import (
  DuplicateProductNameError,
  InvalidProductCategoryError,
  InvalidProductStatusTransitionError,
  ProductDeletionRejectedError,
  ProductNotFoundError,
  ProductValidationError,
)

inventory_router = APIRouter(
  prefix='/product',
  tags=['product'],
  dependencies=[Depends(get_authenticated_user)],
)


def product_domain_error_to_http(error: Exception) -> HTTPException:
  if isinstance(error, ProductValidationError):
    return HTTPException(status_code=400, detail=str(error))
  if isinstance(error, InvalidProductCategoryError):
    if str(error) == 'Category not found.':
      return HTTPException(status_code=404, detail=str(error))
    return HTTPException(status_code=400, detail=str(error))
  if isinstance(error, ProductNotFoundError):
    return HTTPException(status_code=404, detail=str(error))
  if isinstance(error, DuplicateProductNameError):
    return HTTPException(status_code=409, detail=str(error))
  if isinstance(error, InvalidProductStatusTransitionError):
    return HTTPException(status_code=400, detail=str(error))
  if isinstance(error, ProductDeletionRejectedError):
    return HTTPException(status_code=409, detail=str(error))
  raise error

@inventory_router.post('', status_code=201, response_model=None)
async def create_product(
    product: CreateProductSchema,
    session: Session = Depends(get_session),
) -> ProductModel:
  try:
    return ProductService.create_product(
      product.name,
      product.category_id,
      product.cost_price,
      product.sale_value,
      session,
    )
  except (
    ProductValidationError,
    InvalidProductCategoryError,
    ProductNotFoundError,
    DuplicateProductNameError,
    InvalidProductStatusTransitionError,
    ProductDeletionRejectedError,
  ) as exc:
    raise product_domain_error_to_http(exc) from exc


@inventory_router.get('/listar',
                      response_model=(list[ProductResponseSchema]))
async def listar_produtos(session: Session = Depends(get_session)):
  
  products_list = ProductService.list_products(session)
  
  return products_list