from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.inventory_models.product_model import ProductModel
from repository.inventory.category_repository import CategoryRepository
from schemas.product_schema import (
  CreateProductSchema,
  ProductQueryFilterSchema,
  ProductResponseSchema,
)
from services.inventory.category_service import CategoryService
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


def product_model_to_response(
    product_model: ProductModel,
    session: Session,
) -> ProductResponseSchema:
  category_model = CategoryRepository.find_category_by_id(
    product_model.category_id,
    session,
  )

  if category_model is None:
    raise ProductNotFoundError('Product category not found.')

  return ProductResponseSchema.from_model(
    product_model=product_model,
    category=CategoryService.to_domain_category(category_model),
  )


@inventory_router.post(
  '',
  status_code=201,
  response_model=ProductResponseSchema,
)
async def create_product(
    product: CreateProductSchema,
    session: Session = Depends(get_session),
) -> ProductResponseSchema:
  try:
    product_model = ProductService.create_product(
      product.name,
      product.category_id,
      product.cost_price,
      product.sale_value,
      session,
    )
    return product_model_to_response(product_model, session)
  except (
    ProductValidationError,
    InvalidProductCategoryError,
    ProductNotFoundError,
    DuplicateProductNameError,
    InvalidProductStatusTransitionError,
    ProductDeletionRejectedError,
  ) as exc:
    raise product_domain_error_to_http(exc) from exc


@inventory_router.get(
  '',
  response_model=list[ProductResponseSchema],
)
async def list_products(
    filters: ProductQueryFilterSchema = Depends(),
    session: Session = Depends(get_session),
) -> list[ProductResponseSchema]:
  return ProductService.list_products(
    session,
    name=filters.name,
    category_id=filters.category_id,
    status=filters.status,
  )


@inventory_router.get(
  '/{product_id}',
  response_model=ProductResponseSchema,
)
async def get_product(
    product_id: int,
    session: Session = Depends(get_session),
) -> ProductResponseSchema:
  product = ProductService.find_product_by_id(product_id, session)

  if product is None:
    error = ProductNotFoundError('Product not found.')
    raise product_domain_error_to_http(error)

  return product