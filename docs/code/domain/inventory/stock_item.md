# Class: StockItem

### **Responsibility**

  - Representar os itens dentro de um grupo de estoque.

---
### **Relationships**

##### Stock
- Tipo de Relacionamento: Associação
- -> Representa os produtos que estão contidos naquele estoque.

##### Movement
- Tipo de Relacionamento: Associação
- -> Representa a transferência de quantidade entre os grupos de estoque.

---
### **Attribute's**

- (#) id: int
- (#) stock_id: int
- (#) product_id: int
- (#) quantity: int

---
### **Rules**

- Em desenvolvimento.

---
### Public Interface

- Em desenvolvimento.