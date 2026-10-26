from fastapi import FastAPI

app = FastAPI()

from api.inventory_routes.product_routes import product_router
from api.auth_routes import auth_router

app.include_router(product_router)
app.include_router(auth_router)
