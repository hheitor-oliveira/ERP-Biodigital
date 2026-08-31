# Feature Specification: Módulo de Produtos

**Feature Branch**: `inventory-specs/product-spec`

**Created**: 2026-08-30

**Status**: Draft

**Input**: User description: "crie no diretório specs/inventory-specs/product-spec um template de especificação do módulo produto. Utilize a documentação do docs/ para ter uma base inicial."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cadastrar produto (Priority: P1)

Como responsável pelo estoque, quero cadastrar um produto associado a uma categoria, informando seu nome, preço de custo e preço de venda, para que ele possa ser controlado e utilizado nas operações do negócio.

**Why this priority**: O cadastro é a capacidade fundamental para que o produto exista no catálogo e participe do controle de estoque e das vendas.

**Independent Test**: Pode ser testado criando um produto com dados válidos, consultando-o e verificando que seus dados foram preservados, com quantidade inicial igual a zero e status ativo.

**Acceptance Scenarios**:

1. **Given** uma categoria existente e dados válidos, **When** o usuário cadastra o produto, **Then** o produto é criado com quantidade disponível igual a zero e status ativo.
2. **Given** uma categoria inexistente ou dados inválidos, **When** o usuário tenta cadastrar o produto, **Then** o cadastro é recusado e uma mensagem identifica o dado que precisa ser corrigido.

---

### User Story 2 - Consultar produtos (Priority: P2)

Como responsável pelo estoque ou pela venda, quero consultar os produtos cadastrados e seus dados atuais, para saber quais itens estão disponíveis, seus preços, categorias e status.

**Why this priority**: A consulta torna o catálogo utilizável e fornece visibilidade para as operações de estoque e venda.

**Independent Test**: Pode ser testado cadastrando produtos em categorias distintas e consultando a listagem para confirmar que cada produto apresenta seus dados e quantidade disponível.

**Acceptance Scenarios**:

1. **Given** produtos cadastrados, **When** o usuário consulta a listagem, **Then** cada produto é apresentado com nome, categoria, preços, quantidade disponível e status.
2. **Given** que não existem produtos cadastrados, **When** o usuário consulta a listagem, **Then** o sistema informa que não há produtos disponíveis para consulta.

---

### User Story 3 - Atualizar produto e status (Priority: P3)

Como responsável pelo estoque, quero alterar os dados e o status de um produto sem removê-lo do histórico, para manter o catálogo correto e preservar a rastreabilidade das operações.

**Why this priority**: Produtos podem mudar de preço, categoria ou disponibilidade comercial, e o sistema deve conservar sua referência histórica.

**Independent Test**: Pode ser testado alterando individualmente os dados de um produto e seu status, consultando-o novamente e verificando os efeitos definidos para cada status.

**Acceptance Scenarios**:

1. **Given** um produto existente, **When** o usuário altera nome, categoria ou preços com valores válidos, **Then** a consulta posterior apresenta os novos dados.
2. **Given** um produto existente, **When** o usuário o torna inativo, **Then** o produto permanece registrado, não pode ser vendido nem receber entradas ou saídas.
3. **Given** um produto descontinuado, **When** o usuário consulta sua situação para venda e compras, **Then** o produto pode ser vendido, mas não é incluído na lista de compras.

### Edge Cases

- O cadastro deve ser recusado quando o nome estiver vazio, quando a categoria não existir ou quando algum preço for negativo.
- A quantidade disponível deve iniciar em zero e nunca pode se tornar negativa.
- Uma saída deve ser recusada quando a quantidade solicitada for maior que a quantidade disponível.
- Alterações em um produto inexistente devem ser recusadas sem criar um novo registro.
- Um produto não deve ser excluído fisicamente; sua disponibilidade deve ser controlada por status.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE permitir o cadastro de um produto com nome, categoria, preço de custo e preço de venda.
- **FR-002**: O sistema DEVE associar cada produto a uma categoria existente.
- **FR-003**: O sistema DEVE iniciar a quantidade disponível do produto em zero e o status em ativo, quando esses valores não forem informados no cadastro.
- **FR-004**: O sistema DEVE permitir a consulta dos produtos cadastrados, exibindo nome, categoria, preços, quantidade disponível e status.
- **FR-005**: O sistema DEVE permitir a consulta de um produto pelo seu identificador.
- **FR-006**: O sistema DEVE permitir a alteração do nome, categoria, preço de custo, preço de venda e status de um produto existente.
- **FR-007**: O sistema DEVE rejeitar nomes vazios, categorias inexistentes e preços ou quantidades negativos.
- **FR-008**: O sistema DEVE impedir saídas de estoque que excedam a quantidade disponível do produto.
- **FR-009**: O sistema DEVE impedir vendas, entradas e saídas para produtos inativos.
- **FR-010**: O sistema DEVE permitir a venda de produtos descontinuados, mas não deve incluí-los na lista de compras.
- **FR-011**: O sistema DEVE preservar o registro do produto e controlar sua disponibilidade por status, sem exclusão física.

### Key Entities *(include if feature involves data)*

- **Produto**: Item controlado pelo sistema, com identificador, nome, categoria, preços, quantidade disponível e status (ativo, inativo ou descontinuado).
- **Categoria**: Classificação à qual o produto pertence; uma categoria pode estar associada a vários produtos.
- **Item de estoque**: Registro da quantidade de um produto em um estoque específico.
- **Movimentação**: Registro de entrada, saída ou transferência que pode conter um ou mais produtos.
- **Item de venda**: Registro que representa a participação de um produto em uma venda.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Em uma avaliação com dados válidos, pelo menos 95% dos cadastros de produtos são concluídos na primeira tentativa.
- **SC-002**: Usuários conseguem cadastrar um produto completo em até 2 minutos, sem treinamento adicional.
- **SC-003**: Pelo menos 99% das consultas de produtos exibem dados consistentes de categoria, preços, quantidade e status.
- **SC-004**: Nenhuma operação aceita quantidade disponível negativa ou saída superior ao saldo disponível.
- **SC-005**: 100% dos produtos inativos permanecem impedidos de participar de vendas e movimentações de estoque.

## Assumptions

- O módulo será utilizado por usuários autorizados do estoque e das vendas, conforme as permissões existentes no sistema.
- O cadastro não recebe quantidade inicial; entradas e saídas posteriores são registradas pelas operações de estoque.
- Os preços são valores monetários não negativos e podem ser alterados por usuários autorizados.
- Os status válidos são ativo, inativo e descontinuado.
- O produto não é removido fisicamente para preservar referências em estoques, movimentações e vendas.
- O escopo desta especificação cobre o ciclo de vida e as regras do produto; telas, relatórios de compras e operações detalhadas de movimentação são dependências de outros módulos.
