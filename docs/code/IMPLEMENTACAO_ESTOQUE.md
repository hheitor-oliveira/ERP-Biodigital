# Guia de Implementação — Módulo de Estoque

> Arquivo de referência para acompanhar o que foi implementado e o que falta.
> Atualizado em: 23/08/2026

---

## Visão Geral do Módulo

O módulo de estoque controla produtos, categorias, estoques (locais/contexts), itens de estoque e movimentações de entrada, saída e transferência.

---

## Encapsulamento por Camadas

> Regras de dependência e responsabilidade de cada camada do projeto.
> Entenda isso antes de implementar qualquer coisa.

### Diagrama de Dependências

```
┌─────────────────────────────────────────────────────────┐
│                     INTERFACE (Frontend)                │
│              Não existe ainda neste projeto             │
└──────────────────────────┬──────────────────────────────┘
                           │ consome
                           ▼
┌─────────────────────────────────────────────────────────┐
│                     API (Routes)                        │
│            api/routes/*.py  +  schemas/*.py             │
│              FastAPI Routers + Pydantic                 │
└──────────────────────────┬──────────────────────────────┘
                           │ delega
                           ▼
┌─────────────────────────────────────────────────────────┐
│                     SERVICE (Serviços)                  │
│                services/inventory/*.py                  │
│               Lógica de negócio / regras                │
└──────────────────────────┬──────────────────────────────┘
                           │ usa
                           ▼
┌─────────────────────────────────────────────────────────┐
│                     DOMAIN (Domínio)                    │
│                 domain/inventory/*.py                   │
│           Entidades puras Python, sem framework         │
└──────────────────────────┬──────────────────────────────┘
                           │ usa
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   REPOSITORY (Repositório)              │
│              repository/inventory/*.py                  │
│           Acesso a dados (SQLAlchemy / SQL)             │
└──────────────────────────┬──────────────────────────────┘
                           │ usa
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  MODELS (Modelos ORM)                   │
│              models/inventory_models/*.py               │
│           Mapeamento tabela-classe SQLAlchemy           │
└──────────────────────────┬──────────────────────────────┘
                           │ usa
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  DATABASE (Banco de Dados)              │
│               database/connection.py                    │
│            Engine, Session, conexão                     │
└─────────────────────────────────────────────────────────┘
```

### Regra de Ouro

**Uma camada só pode depender de camadas ABAIXO dela, nunca de camadas ACIMA.**

```
API      → pode chamar Service, Schema
Service  → pode chamar Repository, Domain
Domain   → não pode chamar ninguém (é puro Python)
Repository → pode chamar Model, Database
Model    → pode chamar Database
```

### Responsabilidades de Cada Camada

#### 1. DATABASE (`database/`)
| O que faz | O que NÃO faz |
|---|---|
| Cria engine e sessão | Não contém lógica de negócio |
| Gerencia conexão com o banco | Não cria entidades de domínio |
| Fornece `open_session()` | Não executa queries |

#### 2. MODELS (`models/`)
| O que faz | O que NÃO faz |
|---|---|
| Mapeia tabela → classe SQLAlchemy | Não contém regras de negócio |
| Define colunas, FKs, constraints | Não cria objetos de domínio |
| Usa `Mapped[]` e `mapped_column` | Não valida dados |

#### 3. REPOSITORY (`repository/`)
| O que faz | O que NÃO faz |
|---|---|
| Executa INSERT, SELECT, UPDATE, DELETE | Não contém regras de negócio |
| Converte Model ↔ Domain Entity | Não chama Service |
| Usa Session do SQLAlchemy | Não expõe endpoints |
| Apenas acessa dados | Não valida regras (ex: RNGE01) |

**Exemplo de fluxo no Repository:**
```
save(category)    → recebe entidade Domain → cria Model → persiste no banco
reconstruct()     → busca Models do banco → converte para entidades Domain → retorna
```

#### 4. DOMAIN (`domain/`)
| O que faz | O que NÃO faz |
|---|---|
| Define entidades com atributos privados | Não importa nada de fora (nem repository, nem model) |
| Implementa comportamento (métodos de negócio) | Não acessa banco de dados |
| Usa `@property` para leitura | Não usa frameworks (SQLAlchemy, FastAPI) |
| `@classmethod restore()` para reconstituir | Não valida schemas Pydantic |

**Padrão de encapsulamento no Domínio:**
```python
class Product:
    def __init__(self, name: str, ...):
        self._name = name      # ← atributo PRIVADO (com _)

    @property
    def name(self) -> str:     # ← leitura via property
        return self._name

    def change_name(self, new_name: str):  # ← escrita via método
        self._name = new_name
```

#### 5. SERVICE (`services/`)
| O que faz | O que NÃO faz |
|---|---|
| Coordena a lógica de negócio | Não acessa banco direto |
| Valida regras (RNGE01, RNGE02, etc.) | Não cria endpoints |
| Chama Repository para persistir | Não define schemas |
| Cria objetos de Domínio | Não importa Models |

**Exemplo de fluxo no Service:**
```
create_product(name, category_id, cost_price, sale_value)
    → busca Category via CategoryRepository
    → cria entidade Product (Domain)
    → chama ProductRepository.save(product)
    → retorna product
```

#### 6. SCHEMAS (`schemas/`)
| O que faz | O que NÃO faz |
|---|---|
| Valida dados de entrada (request) | Não contém lógica de negócio |
| Define formato de saída (response) | Não acessa banco |
| Usa Pydantic BaseModel | Não cria entidades de domínio |

#### 7. API / ROUTES (`api/routes/`)
| O que faz | O que NÃO faz |
|---|---|
| Define endpoints HTTP | Não contém lógica de negócio |
| Recebe request via Pydantic Schema | Não acessa banco |
| Delega para Service | Não cria entidades de domínio |
| Retorna response | Não valida regras de negócio |

### Fluxo Completo de uma Requisição

```
HTTP Request
    │
    ▼
┌─────────────────────────┐
│ 1. ROUTE (API)          │  Recebe: CreateProductSchema
│    inventory_routes.py  │  Valida formato com Pydantic
└───────────┬─────────────┘
            │ chama
            ▼
┌─────────────────────────┐
│ 2. SERVICE              │  Recebe: dados do schema
│    product_service.py   │  Valida regras de negócio
│                         │  Cria entidade Product (Domain)
└───────────┬─────────────┘
            │ delega
            ▼
┌─────────────────────────┐
│ 3. REPOSITORY           │  Recebe: entidade Product
│    product_repository.py│  Converte para ProductModel
│                         │  Persiste no banco via Session
└───────────┬─────────────┘
            │ usa
            ▼
┌─────────────────────────┐
│ 4. MODEL                │  Mapeia tabela product
│    product_model.py     │  SQLAlchemy ORM
└───────────┬─────────────┘
            │ persiste
            ▼
┌─────────────────────────┐
│ 5. DATABASE             │  Executa SQL no PostgreSQL
│    connection.py        │
└─────────────────────────┘
```

### Erros Comuns de Encapsulamento

| Erro | Por que é errado | Onde acontece |
|---|---|---|
| Repository chama Service | Cria dependência circular | `repository/*.py` |
| Domain importa Repository | Domain não pode acessar dados | `domain/*.py` |
| Route acessa Repository direto | Pula a camada de negócio | `api/routes/*.py` |
| Service cria Model SQLAlchemy | Service não deve saber de ORM | `services/*.py` |
| Domain usa Pydantic | Domain é puro Python | `domain/*.py` |
| Repository valida regras de negócio | Isso é responsabilidade do Service | `repository/*.py` |

### Regra Prática

**Antes de fazer um `import`, pergunte:**

> "Esta camada deveria saber que a outra camada existe?"

- Se a resposta for **não** → não importe.
- Se a resposta for **sim** → verifique se a dependência está na direção correta (para baixo).

---

## Fase 0 — Correções de Bugs Existentes

### 0.1 `domain/inventory/stock_item.py` — Bug: recursão infinita

**Linha 25**: `return self.stock` chama a própria property, causando recursão infinita.

```python
# ANTES (bug)
@property
def stock(self) -> Stock:
    return self.stock

# DEPOIS
@property
def stock(self) -> Stock:
    return self._stock
```

### 0.2 `domain/inventory/movement_item.py` — Atributos públicos

Usa atributos públicos (`self.id`, `self.product`, `self.quantity`) em vez de privados com `@property`, quebrando o padrão do projeto.

```python
# ANTES
self.id = id
self.product = product
self.quantity = quantity

# DEPOIS
self._id = id
self._product = product
self._quantity = quantity

# + properties para id, product, quantity
```

### 0.3 `main.py` — Stub vazio

O `main.py` não expõe o objeto `app`. O README diz para rodar `uvicorn main:app`, mas `app` não existe aqui.

```python
# CORREÇÃO: importar e expor o app
from api.api import app
```

**Status:** [X] Realizado

---

## Fase 1 — Completar Entidades de Domínio

### 1.1 `domain/inventory/stock.py`

Adicionar `@classmethod restore()` e métodos de comportamento.

**Métodos necessários:**
- `restore(id, name, description, status)` → reconstitui do banco
- `change_name(new_name)` → altera nome
- `change_description(new_description)` → altera descrição
- `change_status(new_status)` → altera status

**Status:** [X] Realizado

### 1.2 `domain/inventory/stock_item.py`

Adicionar `@classmethod restore()`.

**Métodos necessários:**
- `restore(id, stock, quantity, products)` → reconstitui do banco
- `change_quantity(new_quantity)` → altera quantidade

**Status:** [X] Realizado

### 1.3 `domain/inventory/movement.py`

Adicionar `@classmethod restore()`.

**Métodos necessários:**
- `restore(id, user, movement_type, movement_date, items)` → reconstitui do banco

**Status:** [X] Realizado

### 1.4 `domain/inventory/movement_item.py`

Adicionar `@classmethod restore()` (após correção da Fase 0.2).

**Métodos necessários:**
- `restore(id, product, quantity)` → reconstitui do banco

**Status:** [X] Realizado

---

## Fase 2 — Padronizar Repositórios

### Decisão: Raw SQL (psycopg) vs SQLAlchemy ORM

Os repositórios de `category_repository.py` e `product_repository.py` usam `DatabaseConnection.get_connection()`, que **não existe** em `database/connection.py`. O `connection.py` fornece engine e session do SQLAlchemy, não conexão raw psycopg.

**Duas opções:**

| Opção | Prós | Contras |
|---|---|---|
| **A) Padronizar em SQLAlchemy ORM** | Consistente com `user_repository.py` e `connection.py`; usa sessões gerenciadas | Reescrever `category_repository` e `product_repository` |
| **B) Criar `DatabaseConnection`** para raw psycopg | Mantém código existente | Dois padrões diferentes; mais complexo de manter |

**Recomendação: Opção A** — padronizar tudo em SQLAlchemy ORM.

**Status:** [X] Realizado

---

## Fase 3 — Implementar Repositórios

> Todos devem seguir o padrão SQLAlchemy ORM com `Session` do `open_session`.

### 3.1 `repository/inventory/stock_repository.py`

| Método | Descrição |
|---|---|
| `save(stock: Stock)` | Insere um novo estoque no banco |
| `reconstruct() → list[Stock]` | Lista todos os estoques ativos |
| `find_by_id(stock_id: int) → Stock` | Busca estoque por ID |

**Status:** [ ] Pendente

### 3.2 `repository/inventory/stock_item_repository.py`

| Método | Descrição |
|---|---|
| `save(stock_item: StockItem)` | Insere item de estoque |
| `update(stock_item: StockItem)` | Atualiza quantidade |
| `find_by_stock_and_product(stock_id, product_id) → StockItem` | Busca item específico |

**Status:** [ ] Pendente

### 3.3 `repository/inventory/movement_repository.py`

| Método | Descrição |
|---|---|
| `save(movement: Movement)` | Insere movimentação + items |
| `reconstruct() → list[Movement]` | Lista todas as movimentações |
| `find_by_id(movement_id: int) → Movement` | Busca movimentação por ID |

**Status:** [ ] Pendente

### 3.4 Refatorar `repository/inventory/category_repository.py`

Migrar de raw SQL para SQLAlchemy ORM.

**Status:** [ ] Pendente

### 3.5 Refatorar `repository/inventory/product_repository.py`

Migrar de raw SQL para SQLAlchemy ORM.

**Status:** [ ] Pendente

---

## Fase 4 — Implementar Serviços

### 4.1 `services/inventory/stock_service.py`

| Método | Descrição |
|---|---|
| `create_stock(name, description) → Stock` | Cria estoque |
| `list_stocks() → list[Stock]` | Lista estoques |
| `add_product_to_stock(stock, product, quantity)` | Adiciona produto ao estoque (cria StockItem) |
| `remove_product_from_stock(stock, product, quantity)` | Remove quantidade do estoque |
| `get_stock_products(stock) → list[StockItem]` | Lista produtos do estoque |

**Regras de negócio:**
- RNGE01: Quantidade requisitada deve estar disponível
- RNGE02: Quantidade nunca pode ser negativa

**Status:** [ ] Pendente

### 4.2 `services/inventory/movement_service.py`

| Método | Descrição |
|---|---|
| `create_movement(user, type, from_stock, to_stock, items) → Movement` | Cria movimentação |
| `list_movements() → list[Movement]` | Lista movimentações |
| `filter_by_date(start, end) → list[Movement]` | Filtra por data |
| `filter_by_type(movement_type) → list[Movement]` | Filtra por tipo |

**Regras de negócio:**
- RNGE01: Movimentação barrada se quantidade indisponível
- RNGE03: Saídas manuais devem registrar motivo

**Status:** [ ] Pendente

### 4.3 Atualizar `services/inventory/product_service.py`

Adicionar método:
- `get_product_by_id(product_id) → Product`

**Status:** [ ] Pendente

### 4.4 Atualizar `services/inventory/category_service.py`

Adicionar método:
- `get_category_by_id(category_id) → Category`

**Status:** [ ] Pendente

---

## Fase 5 — Implementar Schemas Pydantic

### 5.1 `schemas/inventory/category_schema.py`

```python
class CreateCategorySchema(BaseModel):
    name: str

class CategoryResponseSchema(BaseModel):
    id: int
    name: str
```

**Status:** [ ] Pendente

### 5.2 `schemas/inventory/product_schema.py`

```python
class CreateProductSchema(BaseModel):
    name: str
    category_id: int
    cost_price: Decimal
    sale_value: Decimal

class UpdateProductSchema(BaseModel):
    name: str | None = None
    category_id: int | None = None
    cost_price: Decimal | None = None
    sale_value: Decimal | None = None
    status: str | None = None

class ProductResponseSchema(BaseModel):
    id: int
    name: str
    category: CategoryResponseSchema
    cost_price: Decimal
    sale_value: Decimal
    available_quantity: int
    status: str
```

**Status:** [ ] Pendente

### 5.3 `schemas/inventory/stock_schema.py`

```python
class CreateStockSchema(BaseModel):
    name: str
    description: str

class StockResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    status: str
```

**Status:** [ ] Pendente

### 5.4 `schemas/inventory/movement_schema.py`

```python
class MovementItemSchema(BaseModel):
    product_id: int
    quantity: int

class CreateMovementSchema(BaseModel):
    user_id: int
    movement_type: str
    from_stock_id: int | None = None
    to_stock_id: int | None = None
    items: list[MovementItemSchema]

class MovementResponseSchema(BaseModel):
    id: int
    user: UserResponseSchema
    movement_type: str
    movement_date: datetime
    items: list[MovementItemResponseSchema]
```

**Status:** [ ] Pendente

---

## Fase 6 — Implementar Rotas da API

### 6.1 `api/routes/inventory_routes.py` — Rotas de Produto

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/inventario/produtos` | Cadastrar produto |
| `GET` | `/inventario/produtos` | Listar produtos |
| `GET` | `/inventario/produtos/{id}` | Buscar produto por ID |
| `PUT` | `/inventario/produtos/{id}` | Editar produto |

**Status:** [ ] Pendente

### 6.2 `api/routes/category_routes.py` — Rotas de Categoria

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/inventario/categorias` | Cadastrar categoria |
| `GET` | `/inventario/categorias` | Listar categorias |

**Status:** [ ] Pendente

### 6.3 `api/routes/stock_routes.py` — Rotas de Estoque

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/inventario/estoques` | Cadastrar estoque |
| `GET` | `/inventario/estoques` | Listar estoques |
| `GET` | `/inventario/estoques/{id}` | Buscar estoque por ID |
| `POST` | `/inventario/estoques/{id}/produtos` | Adicionar produto ao estoque |
| `DELETE` | `/inventario/estoques/{id}/produtos` | Remover produto do estoque |
| `GET` | `/inventario/estoques/{id}/produtos` | Listar produtos do estoque |

**Status:** [ ] Pendente

### 6.4 `api/routes/movement_routes.py` — Rotas de Movimentação

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/inventario/movimentacoes` | Registrar movimentação |
| `GET` | `/inventario/movimentacoes` | Listar movimentações |
| `GET` | `/inventario/movimentacoes/{id}` | Buscar movimentação por ID |
| `GET` | `/inventario/movimentacoes/filtrar` | Filtrar por data/tipo |

**Status:** [ ] Pendente

---

## Fase 7 — Migrar e Testar

### 7.1 Gerar migration Alembic

```bash
alembic revision --autogenerate -m "refactor_stock_module"
alembic upgrade head
```

**Status:** [ ] Pendente

### 7.2 Testar endpoints

Verificar se todos os endpoints funcionam corretamente via Swagger (`/docs`).

**Status:** [ ] Pendente

---

## Resumo de Implementação

| Fase | Descrição | Itens | Status |
|---|---|---|---|
| 0 | Corrigir bugs | 3 | [ ] |
| 1 | Completar entidades de domínio | 4 | [ ] |
| 2 | Padronizar repositórios | 1 decisão | [ ] |
| 3 | Implementar repositórios | 5 | [ ] |
| 4 | Implementar serviços | 4 | [ ] |
| 5 | Implementar schemas | 4 | [ ] |
| 6 | Implementar rotas API | 4 | [ ] |
| 7 | Migrar e testar | 2 | [ ] |
| **Total** | | **27 itens** | |

---

## Ordem Recomendada de Implementação

```
Fase 0 (bugs) → Fase 1 (domínio) → Fase 2 (decisão ORM) → Fase 3 (repositórios)
→ Fase 4 (serviços) → Fase 5 (schemas) → Fase 6 (rotas) → Fase 7 (migração/testes)
```

**Dica:** Após cada fase, teste individualmente antes de avançar para a próxima.
