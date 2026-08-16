# Class: Product

### **Responsibility's**

  - Representar os produtos do sistema.

---
### **Relationships**

##### SaleItem
  - Tipo de Relacionamento: Associação
  - -> Representa o produto dentro de um item da venda.

##### MovementItem
  - Tipo de Relacionamento: Associação
  - -> Representa o produto dentro de uma um item da movimentação.

##### StockItem
  - Tipo de Relacionamento: Associação
  - -> Representa o produto transferido para um estoque, ou entre eles.

##### Category
  - Tipo de Relacionamento: Composição
  - -> Representa uma categoria que componhe o produto.

---
### **Attribute's**

  - (#) id: int
  - (#) name: str
  - (#) category: Category
  - (#) stock_quantity: int
  - (#) sale_value: Decimal
  - (#) cost_price: Decimal
  - (#) status: (enum) -> Active, Inactive, Descontinued

---
### **Rules**

  - Domain Rule Product 01: A quantidade em estoque de um produto não pode ser negativa.

  - Domain Rule Product 02: O produto só poderá receber uma movimentação de saída, se a quantidade de saída não for maior que sua quantidade em estoque.

  - Domain Rule Product 03: Um produto que estiver descontinuado pode ser vendido, entretanto não deverá ser apontado no relatório de lista de compras.

  - Domain Rule Product 04: Um produto que estiver com o status de Inativo não pode ser vendido, nem receber entradas e saídas.

---
### Public Interface

  - remove_stock()
  - add_stock()
  - change_name()
  - change_sale_value()
  - change_cost_price()
  - change_status()
  - change_category()