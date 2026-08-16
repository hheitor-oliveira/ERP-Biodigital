# Class: Stock

### **Responsibility**

  - Representar os grupos de estoque no sistema.

---
### **Relationships**

##### StockItem
- Tipo de Relacionamento: Composição
- -> Representa os produtos que estão contidos naquele estoque.

##### Movement
- Tipo de Relacionamento: Associação
- -> Representa a transferência de quantidade entre os grupos de estoque.

---
### **Attribute's**

- (#) id: int
- (#) products: list[StockItem]
- (#) name: str
- (#) status: (enum) -> Active, Inactive
- (#) description: str

---
### **Rules**

- Domain Rule Stock 01: Um estoque só pode ser inativado, caso, não hajam mais produtos em estoque.

---
### Public Interface

- Em desenvolvimento.
