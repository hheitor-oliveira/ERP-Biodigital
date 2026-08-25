from repository.inventory.category_repository import CategoryRepository
from sqlalchemy.orm import Session
from domain.inventory.category import Category

class CategoryService():
  
  @classmethod
  def create_category(cls,
                      name: str,
                      session: Session):
    
    category = Category(
      name
    )
    
    CategoryRepository.create_category(category, session)
  
  @classmethod
  def list_all_categories(cls,
                          session: Session):
      
      categories = CategoryRepository.find_all_categories(session)
      
      return categories