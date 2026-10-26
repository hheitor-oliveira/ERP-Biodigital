from sqlalchemy.orm import Session, joinedload
from models.inventory_models.product_model import ProductModel
from domain.inventory.product import Product
from domain.inventory.category import Category

class ProductRepository:
    '''Responsável por gerenciar a persistência de dados da Classe Product no sistema.'''
    
    @staticmethod
    def get_all_products(session: Session) -> list[Product]:

        products = []

        models = (
        session.query(ProductModel)
        .options(joinedload(ProductModel.category))
        .all()
        )

        for model in models:

            category = Category.restore(
            id=model.category.category_id,
            name=model.category.category_name,
            status=model.category.category_status
            )

            product = Product.restore(
            id=model.product_id,
            name=model.product_name,
            category=category,
            available_quantity=model.available_quantity,
            sale_value=model.sale_value,
            cost_price=model.cost_price,
            status=model.product_status
            )

        products.append(product)

        return products