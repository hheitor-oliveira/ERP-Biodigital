# Modelagem Relacional — ERP

## 1. CATEGORY

Representa as categorias utilizadas para classificar os produtos.

### Atributos

- **category_id** — Identificador da categoria.
- category_name — Nome da categoria.
- category_status — Estado da categoria.

### Chave Primária

- **category_id**

### Regras

- `category_name` deve ser único.
- `category_status` possui os estados:
  - ACTIVE
  - INACTIVE

### Relacionamentos

Uma categoria pode possuir vários produtos.

```text
CATEGORY 1 ─── N PRODUCT
```

---

## 2. APP_USER

Representa os usuários que utilizam o sistema.

### Atributos

- **user_id** — Identificador do usuário.
- user_name — Nome do usuário.
- user_login — Login utilizado pelo usuário.
- password_hash — Hash da senha do usuário.

### Chave Primária

- **user_id**

### Regras

- `user_login` deve ser único.
- A senha não é armazenada diretamente, apenas seu hash.

### Relacionamentos

Um usuário pode realizar várias movimentações.

Um usuário pode registrar várias vendas.

```text
APP_USER 1 ─── N MOVEMENT

APP_USER 1 ─── N SALE
```

---

## 3. PRODUCT

Representa os produtos controlados pelo sistema.

### Atributos

- **product_id** — Identificador do produto.
- category_id — Categoria à qual o produto pertence.
- available_quantity — Quantidade disponível do produto.
- product_name — Nome do produto.
- cost_price — Valor de custo.
- sale_value — Valor de venda.
- product_status — Estado do produto.

### Chave Primária

- **product_id**

### Chave Estrangeira

- `category_id` → CATEGORY.`category_id`

### Regras

- `available_quantity` não pode ser negativa.
- `cost_price` não pode ser negativo.
- `sale_value` não pode ser negativo.
- `product_status` possui os estados:
  - ACTIVE
  - INACTIVE
  - DISCONTINUED

### Relacionamentos

- Um produto pertence a uma categoria.
- Um produto pode possuir vários registros de estoque.
- Um produto pode participar de várias movimentações.
- Um produto pode participar de várias vendas.

```text
CATEGORY 1 ─── N PRODUCT

PRODUCT 1 ─── N STOCK_ITEM

PRODUCT 1 ─── N MOVEMENT_ITEM

PRODUCT 1 ─── N SALE_ITEM
```

---

## 4. STOCK

Representa um estoque ou contexto de armazenamento.

O estoque não necessariamente representa apenas um local físico.

Exemplos:

- Estoque da loja
- Estoque de um carro
- Estoque de equipamentos
- Estoque de notebooks
- Almoxarifado

### Atributos

- **stock_id** — Identificador do estoque.
- stock_name — Nome do estoque.
- status — Estado do estoque.
- description — Descrição do estoque.

### Chave Primária

- **stock_id**

### Regras

`status` possui os estados:

- ACTIVE
- INACTIVE

### Relacionamentos

- Um estoque pode possuir vários produtos através de STOCK_ITEM.
- Um estoque pode participar de várias movimentações como origem.
- Um estoque pode participar de várias movimentações como destino.

```text
STOCK 1 ─── N STOCK_ITEM

STOCK 1 ─── N MOVEMENT (origem)

STOCK 1 ─── N MOVEMENT (destino)
```

---

## 5. STOCK_ITEM

Representa a quantidade de determinado produto dentro de determinado estoque.

Essa entidade resolve a relação entre PRODUCT e STOCK.

### Atributos

- **stock_item_id** — Identificador do registro.
- product_id — Produto alocado no estoque.
- stock_id — Estoque onde o produto está alocado.
- quantity — Quantidade do produto naquele estoque.

### Chave Primária

- **stock_item_id**

### Chaves Estrangeiras

- `product_id` → PRODUCT.`product_id`
- `stock_id` → STOCK.`stock_id`

### Regra de unicidade

A combinação:

```text
product_id + stock_id
```

deve ser única.

Isso significa que determinado produto possui apenas um STOCK_ITEM dentro de determinado estoque.

### Regra de quantidade

`quantity` não pode ser negativa.

### Relacionamentos

```text
PRODUCT 1 ─── N STOCK_ITEM N ─── 1 STOCK
```

---

## 6. MOVEMENT

Representa um evento de movimentação de estoque.

A movimentação representa a operação realizada, enquanto seus produtos e quantidades são representados por MOVEMENT_ITEM.

### Atributos

- **movement_id** — Identificador da movimentação.
- user_id — Usuário responsável pela movimentação.
- from_stock_id — Estoque de origem.
- to_stock_id — Estoque de destino.
- movement_type — Tipo da movimentação.

### Chave Primária

- **movement_id**

### Chaves Estrangeiras

- `user_id` → APP_USER.`user_id`
- `from_stock_id` → STOCK.`stock_id`
- `to_stock_id` → STOCK.`stock_id`

### Tipos de movimentação

- INPUT
- OUTPUT
- TRANSFER

### Relacionamentos

```text
APP_USER 1 ─── N MOVEMENT

STOCK 1 ─── N MOVEMENT (origem)

STOCK 1 ─── N MOVEMENT (destino)

MOVEMENT 1 ─── N MOVEMENT_ITEM
```

---

## 7. MOVEMENT_ITEM

Representa um produto e sua quantidade dentro de uma movimentação.

### Atributos

- **movement_item_id** — Identificador do item da movimentação.
- movement_id — Movimentação à qual o item pertence.
- product_id — Produto movimentado.
- quantity — Quantidade movimentada.

### Chave Primária

- **movement_item_id**

### Chaves Estrangeiras

- `movement_id` → MOVEMENT.`movement_id`
- `product_id` → PRODUCT.`product_id`

### Regra

A quantidade movimentada deve ser maior que zero.

### Relacionamentos

```text
MOVEMENT 1 ─── N MOVEMENT_ITEM

PRODUCT 1 ─── N MOVEMENT_ITEM
```

---

## 8. SALE

Representa uma venda.

### Atributos

- **sale_id** — Identificador da venda.
- user_id — Usuário responsável pela venda.
- total_value — Valor total da venda.
- discount_type — Tipo de desconto.
- discount_value — Valor do desconto.

### Chave Primária

- **sale_id**

### Chave Estrangeira

- `user_id` → APP_USER.`user_id`

### Regras

- `total_value` não pode ser negativo.
- `discount_value` não pode ser negativo.
- `discount_type` possui os estados:
  - NONE
  - FIXED
  - PERCENTAGE

### Relacionamentos

```text
APP_USER 1 ─── N SALE

SALE 1 ─── N SALE_ITEM

SALE 1 ─── N SALE_PAYMENT
```

---

## 9. SALE_ITEM

Representa um produto vendido dentro de uma venda.

### Atributos

- **sale_item_id** — Identificador do item.
- sale_id — Venda à qual o item pertence.
- product_id — Produto vendido.
- quantity — Quantidade vendida.
- unitary_value — Valor unitário praticado na venda.
- subtotal — Subtotal do item.

### Chave Primária

- **sale_item_id**

### Chaves Estrangeiras

- `sale_id` → SALE.`sale_id`
- `product_id` → PRODUCT.`product_id`

### Regras

- `quantity` deve ser maior que zero.
- `unitary_value` não pode ser negativo.
- `subtotal` não pode ser negativo.

### Observação

`unitary_value` pertence ao item da venda porque representa o valor efetivamente praticado naquele momento.

O `sale_value` atual de PRODUCT pode sofrer alterações posteriormente.

### Relacionamentos

```text
SALE 1 ─── N SALE_ITEM

PRODUCT 1 ─── N SALE_ITEM
```

---

## 10. SALE_PAYMENT

Representa um pagamento associado a uma venda.

### Atributos

- **sale_payment_id** — Identificador do pagamento.
- sale_id — Venda relacionada.
- payment_method — Método utilizado.
- payment_value — Valor pago.

### Chave Primária

- **sale_payment_id**

### Chave Estrangeira

- `sale_id` → SALE.`sale_id`

### Regras

- `payment_value` deve ser maior que zero.
- `payment_method` possui os estados:
  - CASH
  - PIX
  - CREDIT_CARD
  - DEBIT_CARD
  - OTHER

### Relacionamento

```text
SALE 1 ─── N SALE_PAYMENT
```

---

# Relacionamentos Gerais

```text
                         ┌──────────────┐
                         │   CATEGORY   │
                         └──────┬───────┘
                                │
                                │ 1:N
                                ▼
                         ┌──────────────┐
                         │   PRODUCT    │
                         └──────┬───────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              │ 1:N             │ 1:N             │ 1:N
              ▼                 ▼                 ▼
       ┌─────────────┐  ┌──────────────┐  ┌─────────────┐
       │ STOCK_ITEM  │  │MOVEMENT_ITEM │  │  SALE_ITEM  │
       └──────┬──────┘  └──────┬───────┘  └──────┬──────┘
              │                 │                 │
              │ N:1             │ N:1             │ N:1
              ▼                 ▼                 ▼
        ┌───────────┐     ┌──────────┐       ┌─────────┐
        │   STOCK   │     │ MOVEMENT │       │  SALE   │
        └───────────┘     └────┬─────┘       └────┬────┘
                               │                  │
                               │ N:1              │ 1:N
                               ▼                  ▼
                         ┌────────────┐    ┌──────────────┐
                         │  APP_USER  │    │SALE_PAYMENT  │
                         └────────────┘    └──────────────┘

STOCK também participa de MOVEMENT como:
- origem
- destino
```

# Visão Conceitual do Estoque

```text
PRODUCT
   │
   │ produto existente no sistema
   │
   ├── available_quantity
   │
   │ quantidade disponível para alocação
   │
   ▼
STOCK_ITEM
   │
   │ quantidade do produto
   │ dentro de determinado estoque
   │
   ▼
STOCK
   │
   └── contexto/local de armazenamento
```

Exemplo:

```text
PRODUCT
Mouse
available_quantity = 20

        │
        │ distribuição
        ▼

STOCK_ITEM

┌──────────────┬──────────┐
│ Stock        │ Quantity │
├──────────────┼──────────┤
│ Loja         │    10    │
│ Carro        │     5    │
│ Equipamentos │     5    │
└──────────────┴──────────┘
```

# Visão Conceitual de Movimentação

```text
MOVEMENT
   │
   ├── usuário responsável
   │
   ├── estoque de origem
   │
   ├── estoque de destino
   │
   ├── tipo da movimentação
   │
   └── MOVEMENT_ITEM
           │
           ├── produto
           └── quantidade
```

A movimentação representa **o evento**.

O `MovementItem` representa **o que foi movimentado**.

# Visão Conceitual de Venda

```text
SALE
   │
   ├── usuário responsável
   │
   ├── desconto
   │
   ├── SALE_ITEM
   │      │
   │      ├── produto
   │      ├── quantidade
   │      ├── valor unitário
   │      └── subtotal
   │
   └── SALE_PAYMENT
          │
          ├── método
          └── valor
```

# Resumo das Entidades

| Entidade | Responsabilidade |
|---|---|
| CATEGORY | Classificação dos produtos |
| PRODUCT | Cadastro e controle geral do produto |
| APP_USER | Usuários da aplicação |
| STOCK | Contexto/local de armazenamento |
| STOCK_ITEM | Quantidade de um produto em um estoque |
| MOVEMENT | Evento de movimentação |
| MOVEMENT_ITEM | Produtos envolvidos em uma movimentação |
| SALE | Registro principal da venda |
| SALE_ITEM | Produtos envolvidos em uma venda |
| SALE_PAYMENT | Pagamentos associados à venda |
