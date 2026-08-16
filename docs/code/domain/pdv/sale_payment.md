# Class: SalePayment

### **Responsibility's**

  - Representar o(s) pagamento(s) dentro de uma venda.

---
### **Relationships**

##### Sale
  - Tipo de Relacionamento: Associação
  - -> Representa o pagamento realizado em uma venda.

##### Payment_Method
  - Tipo de Relacionamento: Composição
  - -> Representa os métodos de pagamento do sistema.

---
### **Attribute's**

  - (#) id: int
  - (#) payment_method: PaymentMethod
  - (#) payment_value: Decimal

---
### **Rules**

  - Domain Rule Payment_Method 01 - O valor do pagamento deve ser maior que 0.

---
### Public Interface

  - delete_payment()