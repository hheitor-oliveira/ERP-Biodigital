from fastapi import APIRouter

inventory_router = APIRouter(prefix='/inventario',tags=['inventario'])

@inventory_router.get('/produtos')
async def produtos():
  return {'Mensagem': 'Você acessou a rota de produtos'}