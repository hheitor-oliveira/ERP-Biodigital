# ERP - Biodigital Technology

> Um ERP desenvolvido em Python com foco em arquitetura de software, orientacao a objetos e boas praticas de desenvolvimento.

## Sobre o projeto

O ERP-Biodigital e um projeto de estudos que tem como objetivo simular o desenvolvimento de um ERP real, desde a modelagem de dominio ate a persistencia de dados e a exposicao por API.

Mais do que um sistema funcional, o projeto busca aplicar conceitos utilizados em softwares profissionais, como:

- Arquitetura em camadas
- Domain Driven Design (DDD) (conceitos)
- Programacao Orientada a Objetos
- Encapsulamento
- Separacao de responsabilidades
- Repository Pattern
- Service Layer
- Persistencia com PostgreSQL via SQLAlchemy ORM
- Migracoes de banco com Alembic
- API REST com FastAPI

Todo o desenvolvimento esta sendo realizado de forma incremental, implementando uma funcionalidade por vez.

---

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy (ORM)
- Alembic (migracoes)
- PostgreSQL
- Pydantic (validacao)
- Uvicorn (servidor ASI)
- python-dotenv
- passlib + argon2-cffi (hash de senhas com Argon2id)
- python-jose (JWT)

---

## Estrutura do Projeto

```text
ERP-Biodigital/
├── api/
│   ├── api.py                  # Instancia principal do FastAPI
│   └── routes/
│       ├── auth_routes.py      # Rotas de autenticacao
│       └── inventory_routes.py # Rotas de inventario
├── database/
│   └── connection.py           # Configuracao de conexao com o banco
├── domain/
│   ├── enums/
│   │   ├── movement_type.py    # Tipos de movimentacao (INPUT, OUTPUT, TRANSFER)
│   │   ├── payment_methods.py  # Formas de pagamento (PIX, CREDIT_CARD, etc.)
│   │   ├── status.py           # Status de entidades (ACTIVE, INACTIVE, DISCONTINUED)
│   │   └── user_roles.py       # Cargos de usuario (ADMIN, TECHNIQUE, ATTENDANT)
│   ├── exceptions/
│   ├── inventory/
│   │   ├── category.py         # Entidade Category
│   │   ├── movement.py         # Entidade Movement
│   │   ├── movement_item.py    # Entidade MovementItem
│   │   ├── product.py          # Entidade Product
│   │   ├── stock.py            # Entidade Stock
│   │   └── stock_item.py       # Entidade StockItem
│   ├── sales/
│   │   ├── payment_method.py   # Entidade PaymentMethod
│   │   ├── sale.py             # Entidade Sale
│   │   ├── sale_item.py        # Entidade SaleItem
│   │   └── sale_payment.py     # Entidade SalePayment
│   └── users/
│       └── app_user.py         # Entidade AppUser
├── models/
│   ├── base.py                 # Base declarativa do SQLAlchemy
│   ├── inventory_models/
│   │   ├── category_model.py
│   │   ├── movement_model.py
│   │   ├── movement_item_model.py
│   │   ├── product_model.py
│   │   ├── stock_model.py
│   │   └── stock_item_model.py
│   └── user_model/
│       └── app_user.py
├── repository/
│   ├── inventory/
│   │   ├── category_repository.py
│   │   ├── movement_repository.py   # (em implementacao)
│   │   ├── product_repository.py
│   │   └── stock_repository.py      # (em implementacao)
│   ├── sales/
│   │   └── sale_repository.py       # (em implementacao)
│   └── users/
│       └── app_user_repository.py   # (em implementacao)
├── services/
│   └── inventory/
│       ├── category_service.py
│       └── product_service.py
├── alembic/                     # Migracoes do banco de dados
├── docs/                        # Documentacao do projeto
├── alembic.ini
├── main.py
└── requirements.txt
```

Cada camada possui uma responsabilidade especifica, mantendo o sistema organizado e de facil manutencao.

---

## Modulos do Sistema

### Inventario (em implementacao)

Modulo responsavel pela gestao de produtos, categorias, estoques e movimentacoes de estoque.

Tabelas de banco: `category`, `product`, `stock`, `stock_item`, `movement`, `movement_item`

Funcionalidades implementadas:
- Cadastro e listagem de categorias
- Cadastro, listagem e edicao de produtos
- Definicao de modelo de dominio para estoques e movimentacoes

### Vendas (em implementacao)

Modulo responsavel pela gestao de vendas, itens de venda e pagamentos.

Tabelas de banco: (a serem criadas)

Funcionalidades implementadas:
- Definicao de modelo de dominio para vendas, itens de venda e pagamentos

### Usuarios (em implementacao)

Modulo responsavel pela gestao de usuarios do sistema e autenticacao.

Tabelas de banco: `app_user`

Funcionalidades implementadas:
- Definicao de modelo de dominio para usuarios
- Rotas de autenticacao (estrutura inicial)

---

## Banco de Dados

O projeto utiliza PostgreSQL como banco de dados relacional, com ORM via SQLAlchemy e migracoes gerenciadas pelo Alembic.

Tabelas existentes:
- `app_user` - Usuarios do sistema
- `category` - Categorias de produtos
- `product` - Produtos do inventario
- `stock` - Estoques
- `stock_item` - Itens dentro de cada estoque
- `movement` - Movimentacoes de estoque
- `movement_item` - Itens de cada movimentacao

---

## Como Executar

1. Clonar o repositorio
2. Criar o ambiente virtual: `python -m venv .venv`
3. Ativar o ambiente virtual: `source .venv/bin/activate`
4. Instalar as dependencias: `pip install -r requirements.txt`
5. Configurar as variaveis de ambiente no arquivo `.env`
6. Executar as migracoes: `alembic upgrade head`
7. Iniciar o servidor: `uvicorn main:app --reload`

---

## Objetivo

O principal objetivo deste projeto e aprofundar conhecimentos em desenvolvimento de software atraves da construcao de um ERP completo, simulando cenarios encontrados no mercado.

Durante o desenvolvimento sao estudados temas como:

- Modelagem de dominio
- Banco de dados relacional
- Casos de uso
- Arquitetura de Software
- Clean Code
- Repository Pattern
- Service Layer
- Boas praticas de programacao

---

## Status

Em desenvolvimento.

O modulo de inventario possui persistencia funcional com PostgreSQL. Os modulos de vendas e usuarios estao em fase de modelagem de dominio. A API REST esta em estrutura inicial com FastAPI.

---

## Licenca

Este projeto esta licenciado sob a licenca MIT.
referência