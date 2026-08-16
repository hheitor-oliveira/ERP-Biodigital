# Class: Category

### **Responsibility's**

- Representar as categorias do sistema e permitir a persistência.

---
### **Relationships**

##### Product
- Tipo de Relacionamento: Associação
- -> Categorias que os produtos podem ter.

---
### **Attribute's**

  - id (int)
  - name (str)
  - status (enum) -> Status: ACTIVE & INACTIVE

---
### **Rules**

- Domain Rule Category 01: 

---
### Public Interface

- PBINT01: change_name() -> Responsável por alterar o nome de uma categoria.