from sqlalchemy.orm import Session
from domain.inventory.category import Category
from models.inventory_models.category_model import CategoryModel
from typing import Sequence
from sqlalchemy import select

class CategoryRepository:
  
  @classmethod
  def create_category(cls,
                      category: Category,
                      session: Session):
    
    category_model = CategoryModel(
      category_name = category.name
    )
    
    session.add(category_model)
    session.commit()
  
  @classmethod
  def find_all_categories(cls,
                          session: Session) -> Sequence[CategoryModel]:
    
    query = select(CategoryModel)
    result = session.execute(query)
    categories = result.scalars().all()
    
    return categories
  
  @classmethod
  def find_category_by_id(cls,
                          id: int,
                          session: Session) -> CategoryModel | None:
    
    query = select(CategoryModel).where(
      CategoryModel.category_id == id
    )
    
    result = session.execute(query)
    
    category = result.scalar_one_or_none()
    
    return category