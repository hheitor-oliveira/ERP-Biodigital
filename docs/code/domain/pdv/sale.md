# Entity: Sale

### **Responsibility's**

  - Adicionar itens
  - Calcular total
  - Registrar pagamentos
  - Remover itens
  - Finalizar venda
  - Aplicar desconto

---
### **Relationships**

#####  User
  - Tipo de Relacionamento: Associação
  - -> Representa o usuário responsável pela venda.

##### Sale Item
  - Tipo de Relacionamento: Composição.
  - -> Representa os itens da venda.

##### Sale Payment
  - Tipo de Relacionamento: Composição.
  - -> Representa os pagamentos da venda.

---
### **Attribute's**

  - (#) id: int
  - (#) sale_items : list[SaleItem]
  - (#) payment_methods: list[SalePayment]
  - (#) user: SystemUser
  - (#) total_value: Decimal
  - (#) discount_type: str
  - (#) discount_value: Decimal

---
### **Rules**

  - Domain Rule Sale 01: Uma venda é iniciada quando um produto é adicionado a ela.

  - Domain Rule Sale 02: Uma venda só poderá ser finalizada se o valor total do(s) pagamento(s) foi igual ao valor total da venda.

  - Domain Rule Sale 03: O desconto em uma venda só podera ter um tipo: Porcentagem ou Valor Exato.

  - Domain Rule Sale 04: Um pagamento só pode ser adicionado se, a soma desse pagamento com os demais já existentes não for maior que o total da venda.

  - Domain Rule Sale 05: O desconto não pode gerar um total negativo.

  - Domain Rule Sale 06: O desconto percentual deve estar entre 0% e 100%.

  - Domain Rule Sale 07: O desconto em valor não pode ultrapassar o total da venda.

---
### Public Interface

  - add_item()
  - remove_item()
  - apply_discount()
  - cancel_sale()
  - finalize_sale()
