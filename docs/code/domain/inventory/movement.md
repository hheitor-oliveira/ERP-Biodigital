# Class: Movement

### **Responsibility**

  - Representar as movimentações realizadas no sistema.

---
### **Relationships**

##### Sale
 - Tipo de Relacionamento: Associação
 - -> Representa um dos métodos de movimentação, saídas através de vendas.

### MovementItem
 - Tipo de Relacionamento: Composição
 - -> Representa os itens que componhem a movimentação, permitindo vários itens em uma movimentação.

### Stock
 - Tipo de Relacionamento: Associação
 - -> Representa as movimentações de transferência, no qual precisam registrar de qual estoque e para qual foram transferidos os itens.

---
### **Attribute's**

  - (#) id: int | default = 0
  - (#) items: list[MovementItem]
  - (#) user: SystemUser
  - (#) movement_type: MovementType (enum) -> ENTRY, EXIT, TRASNFERENCE
  - (#) movement_date: datetime
  - (#) from_stock_id: int | optional
  - (#) to_stock_id: int | optional

---
### **Rules**

- Domain Rule Movement 01: Para uma movimentação ser cadastrada, deve haver no mínimo 1 item.

- Domain Rule Movement 02: Caso não seja uma trasnferência, o "from_stock" e o "to_stock" devem ser definidos para NULL.

---
### Public Interface

- Em desenvolvimento.