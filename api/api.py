from fastapi import FastAPI

app = FastAPI()

from api.routes.inventory_routes import inventory_router
from api.routes.auth_routes import auth_router

app.include_router(inventory_router)
app.include_router(auth_router)