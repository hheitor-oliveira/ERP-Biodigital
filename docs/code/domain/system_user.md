# Class: SystemUser

### **Responsibility's**

- Representar os usuários que realizam as ações dentro do sistema, e controlar permissionismo.

---
### **Relationships**

##### Sale
- Tipo de Relacionamento: Composição
- -> Representa o usuário responsável pela venda.

##### Movement
- Tipo de Relacionamento: Composição
- -> Representa o usuário responsável pela movimentação.

---
### **Attribute's**

  - id: int
  - name: str
  - login: str
  - password_hash: str
  - role: Roles (enum) -> admin, technique, attendant

---
### **Rules**

- Em desenvolvimento.

---
### Public Interface

- Em desenvolvimento
