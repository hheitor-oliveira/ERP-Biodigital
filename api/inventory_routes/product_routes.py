from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_session
from services.inventory.product_service import ProductService

product_router = APIRouter(
    prefix='/product', 
    tags=['product']
    )

@product_router.get('/list')
async def get_products(session: Session = Depends(get_session)):

    products = ProductService.get_all_products(session)

    return {"message": "Get all products", "products": products}