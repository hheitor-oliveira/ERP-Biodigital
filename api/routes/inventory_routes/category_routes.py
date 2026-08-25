from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.category_schema import CategoryResponseSchema, CategoryCreateSchema
from services.inventory.category_service import CategoryService
from api.dependencies import get_session

category_router = APIRouter(prefix='/category',tags=['category'])

@category_router.get('/list',
                      response_model=list[CategoryResponseSchema])
async def produtos(session: Session = Depends(get_session)):
  
  categories = CategoryService.list_all_categories(session)
  
  return categories

@category_router.post('/create')
async def criar_categoria(category: CategoryCreateSchema,
                          session: Session = Depends(get_session)):
  
  CategoryService.create_category(category.name, session)
  