from fastapi import FastAPI
import uvicorn

app = FastAPI()

from api.routes.inventory_routes.product_routes import inventory_router
from api.routes.auth_routes import auth_router
from api.routes.inventory_routes.category_routes import category_router

app.include_router(inventory_router)
app.include_router(auth_router)
app.include_router(category_router)

def run():
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)