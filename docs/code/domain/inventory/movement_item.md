# Class: MovementItem

### **Responsibility's**

 - Representar os itens dentro de uma movimentação no sistema, permitindo assim uma movimentação com múltiplos itens.

---
### **Relationships**

##### Movement
  - Tipo de Relacionamento: Associação
  - -> Movimentação onde os items estão incluídos.

##### Product
  - Tipo de Relacionamento: Composição
  - -> Produto usado como referência para o item.

---
### **Attribute's**

  - id (int)
  - product (Product)
  - quantity (int)

---
### **Rules**

 - Domain Rule MovementItem 01: A quantidade do item deve ser maior que 0.

---
### Public Interface

 - PBINT 01: set_quantity -> Responsável por ditar a quantidade que será adicionada ou retirada do item na movimentação.