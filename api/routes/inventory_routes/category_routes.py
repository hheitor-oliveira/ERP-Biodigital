from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.category_schema import (
    CategoryResponseSchema,
    CategoryCreateSchema,
    CategoryRenameSchema,
    CategoryStatusUpdateSchema,
)
from services.inventory.category_service import CategoryService
from api.dependencies import get_session, verify_access_token

category_router = APIRouter(prefix='/category',tags=['category'], dependencies=[Depends(verify_access_token)])

@category_router.get('/list',
                      response_model=list[CategoryResponseSchema])
async def produtos(
    session: Session = Depends(get_session),
) -> list[CategoryResponseSchema]:
  
  categories = CategoryService.list_all_categories(session)
  
  category_responses: list[CategoryResponseSchema] = []
  for category in categories:
    if category.id is None:
      raise RuntimeError("Persisted category must have an id.")
    category_responses.append(
        CategoryResponseSchema(
            id=category.id,
            name=category.name,
            status=category.status,
        )
    )

  return category_responses

@category_router.post('/create',
                      response_model=CategoryResponseSchema)
async def criar_categoria(category: CategoryCreateSchema,
                          session: Session = Depends(get_session),
                          ) -> CategoryResponseSchema:
  try:
    created_category = CategoryService.create_category(category.name, session)
  except ValueError as error:
    raise HTTPException(
        status_code=400,
        detail=str(error),
    ) from error

  return CategoryResponseSchema(
      id=created_category.category_id,
      name=created_category.category_name,
      status=created_category.category_status,
  )

@category_router.put(
    '/{category_id}/rename',
    response_model=CategoryResponseSchema,
)
async def renomear_categoria(
    category_id: int,
    category: CategoryRenameSchema,
    session: Session = Depends(get_session),
) -> CategoryResponseSchema:
  try:
    updated_category = CategoryService.rename_category(
        category_id,
        category.name,
        session,
    )
  except ValueError as error:
    raise HTTPException(
        status_code=400,
        detail=str(error),
    ) from error

  return CategoryResponseSchema(
      id=updated_category.category_id,
      name=updated_category.category_name,
      status=updated_category.category_status,
  )

@category_router.patch(
    '/{category_id}/status',
    response_model=CategoryResponseSchema,
)
async def alterar_status_categoria(
    category_id: int,
    category: CategoryStatusUpdateSchema,
    session: Session = Depends(get_session),
) -> CategoryResponseSchema:
  try:
    updated_category = CategoryService.change_category_status(
        category_id,
        category.status,
        session,
    )
  except ValueError as error:
    if str(error) == "Category not found.":
      raise HTTPException(
          status_code=404,
          detail=str(error),
      ) from error

    raise HTTPException(
        status_code=400,
        detail=str(error),
    ) from error

  return CategoryResponseSchema(
      id=updated_category.category_id,
      name=updated_category.category_name,
      status=updated_category.category_status,
  )
