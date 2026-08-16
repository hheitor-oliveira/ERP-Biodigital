# Class: PaymentMethod


### **Responsibility's**

  - Representar os métodos de pagamento em um pagamento.

---
### **Relationships**

##### Sale_Payment
  - Tipo de Relacionamento: Associação
  - -> Representa o método de pagamento utilizado em um pagamento.

---
### **Attribute's**

  - (#) id: int
  - (#) method: Method (enum) -> PIX, DEBIT, CREDIT
  - (#) active: bool

---
### **Rules**

  - Domain Rules PaymentMethod 01: Um método de pagamento só pode ser usado em um pagamento se ele estiver ativo.

---
### Public Interface

  - Em desenvolvimento