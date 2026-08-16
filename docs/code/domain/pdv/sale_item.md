# Class: SaleItem

### **Responsibility's**

  - Representar um item individualmente em uma venda.
  - Calcular subtotal a partir da quantidade de items.

---
### **Relationships**

##### Sale
  - Tipo de Relacionamento: Associação
  - -> Representar os itens das vendas.

##### Product
  - Tipo de Relacionamento: Composição
  - -> Referência do produto vendido.

---
### **Attribute's**

  - (#) id: int
  - (#) product: Product
  - (#) quantity: int
  - (#) unitary_value: Decimal

---
### **Rules**

- Domain Rule Sale_Item 01: Um item em uma venda deve ter a quantidade maior que 0.

- Domain Rule Sale_Item 02: O subtotal do item tem que ser estritamente calculado em base da quantidade do produto.

---
### Public Interface

- modify_quantity()