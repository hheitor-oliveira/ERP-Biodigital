# Status do Projeto

## Task 1 — README

Propósito do projeto:

- O ERP-Biodigital é descrito como um projeto de estudo de ERP em Python, focado em arquitetura de software, programação orientada a objetos e boas práticas de desenvolvimento.

- O objetivo declarado é simular o desenvolvimento de um sistema ERP real, desde a modelagem do domínio até a persistência dos dados e exposição por API.

Arquitetura:

- O README descreve uma arquitetura em camadas.

- Menciona conceitos de Domain Driven Design, padrão Repository, camada de Service, separação de responsabilidades e encapsulamento orientado a objetos.

- Também documenta módulos separados em `api/`, `database/`, `domain/`, `models/`, `repository/`, `services/`, `alembic/`, `docs/` e um ponto de entrada principal.

Stack tecnológica:

- Python 3.12

- FastAPI

- SQLAlchemy ORM

- Alembic

- PostgreSQL

- Pydantic

- Uvicorn

- python-dotenv

- passlib + argon2-cffi

- python-jose

Funcionalidades descritas:

- Módulo de Estoque: cadastro e listagem de categorias, cadastro/listagem/edição de produtos e modelagem de domínio para estoques e movimentações de estoque.

- Módulo de Vendas: modelagem de domínio para vendas, itens de venda e pagamentos.

- Módulo de Usuários: modelagem de domínio para usuários e uma estrutura inicial de rotas de autenticação.

- O README também documenta a persistência com PostgreSQL e as migrations do banco de dados.

Estado documentado do projeto:

- O projeto é descrito como "Em desenvolvimento".

- O README informa que a persistência do estoque está funcional com PostgreSQL.

- Informa que vendas e usuários ainda estão na fase de modelagem de domínio.

- Informa que a API REST está em uma estrutura inicial utilizando FastAPI.

## Task 2 — Documentação

Documentação existente:

- `docs/business/vision/objective.md` e `docs/business/vision/insight.md` descrevem o problema de negócio: processos internos fragmentados e mal gerenciados, com o objetivo de centralizar os fluxos do ERP.

- `docs/business/requisites/business_rules.md` define regras de negócio para vendas, estoque e usuários, embora a seção de usuários esteja incompleta.

- `docs/business/requisites/funcional_requeriments.md` lista requisitos funcionais para estoque, vendas e usuários.

- `docs/business/requisites/non_funcional_requeriments.md` existe, mas contém apenas placeholders.

- `docs/business/requisites/cases_of_uses.md` contém pelo menos um caso de uso em desenvolvimento, mas está incompleto e parece apresentar inconsistências de nomenclatura.

- `docs/code/IMPLEMENTACAO_ESTOQUE.md` é um guia detalhado de implementação do módulo de estoque, contendo observações de arquitetura, regras de dependência e acompanhamento das fases.

- `docs/code/domain/...` contém documentação das entidades de estoque, vendas/pagamentos e usuários do sistema, além de seus relacionamentos e regras.

- `docs/code/persistance/Modelo Relacional - ERP Biodigital V2.0.md` documenta o modelo relacional para `category`, `app_user`, `product`, `stock`, `stock_item`, `movement`, `movement_item`, `sale`, `sale_item` e `sale_payment`.

- `docs/ideas.md` está vazio.

Decisões arquiteturais documentadas:

- O guia de implementação do estoque define uma arquitetura estritamente em camadas:

  `API → Service → Domain → Repository → Model → Database`

- O guia estabelece que as entidades de domínio devem ser Python puro, os repositories devem lidar com persistência, os services devem conter regras de negócio e os schemas devem validar entrada/saída da API.

- O guia recomenda explicitamente padronizar os repositories utilizando SQLAlchemy ORM em vez de misturar padrões com SQL puro.

Decisões técnicas documentadas:

- O guia de implementação descreve o uso de métodos de classe `restore()` para reconstruir entidades de domínio a partir de dados de persistência.

- O documento do modelo relacional define regras de unicidade, chaves estrangeiras e constraints para impedir quantidades/valores negativos em diversas tabelas.

- A documentação de domínio define enums e padrões de encapsulamento para categorias, produtos, estoque, movimentações, vendas, pagamentos e usuários do sistema.

Funcionalidades documentadas:

- Estoque: gerenciamento de produtos/categorias, contextos de estoque, itens de estoque e movimentações.

- Vendas: composição de vendas, itens de venda, pagamentos de venda, controle de descontos e métodos de pagamento.

- Usuários: usuários internos, funções e controle de permissões.

- Os requisitos de negócio mencionam auditoria, consulta de estoque, listas de compras, geração de PDF de notas fiscais, extratos de caixa e garantias, mas muitas dessas funcionalidades ainda não estão implementadas no código.

Informações relevantes do projeto:

- A documentação é composta por uma combinação de visão de negócio, requisitos, modelagem relacional, documentação de domínio e backlog de implementação.

- Vários documentos estão parciais ou contêm apenas placeholders, portanto o conjunto de documentação ainda não está completo.

- O guia de implementação do estoque contém indicadores explícitos de status, mostrando fases concluídas e fases ainda pendentes.

## Task 3 — API

Endpoints:

- `api/app.py` cria a aplicação FastAPI e inclui três routers: inventory, auth e category.

- `api/routes/inventory_routes/product_routes.py`

  - `POST /product/cadastrar`

  - `GET /product/listar`

- `api/routes/inventory_routes/category_routes.py`

  - `GET /category/list`

  - `POST /category/create`

- `api/routes/auth_routes.py`

  - `POST /auth/create_user`

Responsabilidades:

- A camada de API é responsável por expor endpoints HTTP e delegar o processamento para os services.

- As rotas recebem schemas Pydantic e utilizam uma dependência de sessão SQLAlchemy.

Dependências:

- `fastapi.APIRouter`, `fastapi.Depends` e `fastapi.FastAPI`

- `sqlalchemy.orm.Session`

- `api.dependencies.get_session` para sessões do banco de dados

- `schemas.user_schema`, `schemas.product_schema`, `schemas.category_schema`

- `services.users.user_service.UserService`

- `services.inventory.product_service.ProductService`

- `services.inventory.category_service.CategoryService`

- `api.dependencies.pwd_context` para hashing de senhas durante a criação de usuários

Estado atual da implementação:

- Implementada em nível básico.

- A API consegue registrar e incluir routers, mas aparenta ser uma superfície inicial, e não uma API REST completa.

- Os endpoints de criação chamam métodos dos services, mas não retornam payloads explícitos de sucesso.

- Não há um fluxo de autenticação/login visível, middleware de autorização ou camada de tratamento de erros nos arquivos da API analisados.

- A API atualmente cobre apenas criação de usuários, criação/listagem de produtos e criação/listagem de categorias.

## Task 4 — Schemas

Schemas presentes:

- `schemas/product_schema.py`

  - `CreateProductSchema`

  - `CategoryResponse`

  - `ProductResponseSchema`

- `schemas/category_schema.py`

  - `CategoryCreateSchema`

  - `CategoryResponseSchema`

- `schemas/user_schema.py`

  - `CreateUserSchema`

Responsabilidades de validação:

- Os schemas definem os formatos de requisição e resposta da API.

- Utilizam modelos Pydantic para validação de tipos e serialização.

- Os schemas de resposta utilizam `ConfigDict(from_attributes=True)` para permitir a serialização de objetos ORM a partir de seus atributos.

- Os schemas analisados não definem constraints adicionais de campos, como tamanho mínimo/máximo, limites numéricos ou validadores personalizados.

Contratos da API:

- A criação de produtos espera `product_name`, `category_id`, `cost_price` e `sale_value`.

- As respostas de produtos expõem `id`, `name`, `category` aninhada, `cost_price`, `sale_value`, `status` e `available_quantity`.

- A criação de categorias espera apenas `name`.

- As respostas de categorias expõem `category_id`, `category_name` e `category_status`.

- A criação de usuários espera `name`, `email` e `password`.

Responsabilidades:

- Os schemas funcionam como contrato entre a camada HTTP e a camada de services.

- Eles representam apenas os campos utilizados pelas rotas atuais da API.

Estado atual da implementação:

- Parcialmente implementado.

- Existem schemas de criação/listagem para categorias e produtos.

- Existe schema de entrada para criação de usuários.

- Não foram encontrados schemas para login de usuários, atualizações ou operações de vendas/estoque além dos endpoints básicos atuais.

- O conjunto de schemas é pequeno e representa apenas a superfície inicial da API atualmente existente.

## Task 5 — Services

Services presentes:

- `services/inventory/category_service.py`

- `services/inventory/product_service.py`

- `services/users/user_service.py`

Lógica de aplicação:

- `CategoryService.create_category()` instancia um objeto de domínio `Category` e delega a persistência para `CategoryRepository.create_category()`.

- `CategoryService.list_all_categories()` delega para `CategoryRepository.find_all_categories()`.

- `ProductService.create_product()` carrega a categoria através de `CategoryRepository.find_category_by_id()`, reconstrói um objeto de domínio `Category`, cria um `Product` e delega a persistência para `ProductRepository.create_user()`.

- `ProductService.list_products()` lê modelos de produtos do repository, reconstrói entidades de domínio `Category` e `Product` e retorna uma lista de produtos.

- `UserService.create_user()` realiza o hashing da senha utilizando Argon2 através de `pwd_context` e persiste uma entidade de domínio `AppUser` através de `UserRepository.create_user()`.

Dependências:

- Entidades de domínio: `Category`, `Product`, `AppUser`

- Repositories: `CategoryRepository`, `ProductRepository`, `UserRepository`

- `sqlalchemy.orm.Session`

- `decimal.Decimal` para valores monetários dos produtos

- `api.dependencies.pwd_context` para hashing de senhas

Responsabilidades:

- Os services atuam como camada de lógica de aplicação entre as rotas da API e a persistência.

- Eles transformam dados simples das requisições em entidades de domínio e coordenam chamadas aos repositories.

- O hashing de senhas é realizado exclusivamente nessa camada, dentre os pontos observados no código atual.

Estado atual da implementação:

- Parcialmente implementado.

- Existem services de estoque para operações de categoria e produto, além de um método básico de criação de usuários.

- Não existe uma camada de services para vendas ou movimentações de estoque no código analisado.

- A aplicação de regras de negócio aparenta ser mínima na implementação atual, com a maioria dos métodos delegando diretamente aos repositories.

- A camada de services atualmente suporta apenas fluxos básicos de criação e listagem.

## Task 6 — Domain

Escopo do domínio:

- A camada de domínio inclui entidades de estoque, entidades de vendas, entidades de usuários e enums.

- O código de domínio de estoque é a parte mais desenvolvida da camada.

Entidades e enums:

- Estoque: `Category`, `Product`, `Stock`, `StockItem`, `Movement`, `MovementItem`

- Vendas: `Sale`, `SaleItem`, `SalePayment`, `PaymentMethod`

- Usuários: `AppUser`

- Enums: `StatusEnum`, `MovementType`, `UserRoles`, `Method`

Relacionamentos documentados ou implementados:

- `Category` está associada a `Product`.

- `Product` está associado a `MovementItem`, `StockItem` e `SaleItem`, e possui composição com `Category` na documentação.

- `Stock` possui composição com `StockItem` e está associado a `Movement`.

- `Movement` está associado a `AppUser` e possui composição com `MovementItem`.

- `Sale` está associado a `AppUser` e possui composição com `SaleItem` e `SalePayment`.

- `PaymentMethod` é utilizado por `SalePayment`.

Regras e comportamentos de negócio observados no código/documentação:

- `Product` permite alterar nome, valor de venda, preço de custo, status, categoria e quantidade em estoque.

- `Stock` permite alterar nome, descrição, status e adicionar/remover `StockItem`.

- `Movement` e as entidades relacionadas às vendas são, em sua maioria, estruturas de dados na implementação analisada.

- A documentação descreve regras como quantidades não negativas, verificações de disponibilidade de estoque e restrições relacionadas a vendas/pagamentos.

- O código não implementa todas as regras descritas na documentação.

Estado atual da implementação:

- Maturidade mista.

- As entidades de estoque estão implementadas com construtores, propriedades e alguns métodos de mutação.

- As entidades de vendas existem, mas são majoritariamente containers de atributos com comportamento limitado.

- `AppUser` está implementada como uma entidade básica contendo id, nome, email e senha.

- Alguns métodos/propriedades de domínio estão incompletos ou incorretos no código analisado, portanto a camada de domínio ainda não está totalmente estável.

- A documentação de domínio e o código real não estão completamente alinhados em todos os pontos.

## Task 7 — Models

Modelos de persistência presentes:

- `models/base.py` define a base declarativa do SQLAlchemy.

- Modelos de estoque:

  - `CategoryModel`

  - `ProductModel`

  - `StockModel`

  - `StockItemModel`

  - `MovementModel`

  - `MovementItemModel`

- Modelo de usuário:

  - `UserModel`

Mapeamentos e relacionamentos:

- `CategoryModel` mapeia para `category` com `category_id`, `category_name` e `category_status`.

- `ProductModel` mapeia para `product` e possui uma chave estrangeira para `category.category_id`.

- `StockModel` mapeia para `stock` com `stock_name` único.

- `StockItemModel` mapeia para `stock_item` com chaves estrangeiras para `product.product_id` e `stock.stock_id`.

- `MovementModel` mapeia para `movement` com chaves estrangeiras para `app_user.user_id`, `stock.stock_id` (origem e destino) e um enum de tipo de movimentação.

- `MovementItemModel` mapeia para `movement_item` com chaves estrangeiras para `movement.movement_id` e `product.product_id`.

- `UserModel` mapeia para `app_user` com `user_email` único e um campo booleano `admin`.

Validações / constraints nos models:

- `ProductModel` possui constraints para impedir valores negativos em `cost_price`, `sale_value` e `available_quantity`.

- `MovementItemModel` possui uma constraint para impedir quantidade negativa.

- `StockItemModel` possui uma constraint para impedir quantidade negativa.

- `UserModel` armazena a senha como campo obrigatório e possui `admin` com valor padrão `false`.

Responsabilidades:

- Os models lidam com o mapeamento ORM das tabelas e com as constraints do banco de dados.

- Eles não contêm lógica de negócio.

Estado atual da implementação:

- Os models de persistência de estoque e usuários estão implementados em nível básico.

- O código analisado não inclui models de persistência para vendas, apesar de a documentação descrevê-los.

- A camada de models está concentrada nas definições das tabelas e constraints, em vez de relacionamentos ORM ou mapeamentos mais completos.

- `StockItemModel` aparenta possuir `__table_args__` escrito fora da indentação da classe no código analisado, portanto esse model deve ser verificado caso seja utilizado em runtime.

## Task 8 — Repository

Repositories presentes:

- `repository/inventory/category_repository.py`

- `repository/inventory/product_repository.py`

- `repository/users/user_repository.py`

- `repository/inventory/movement_repository.py` (vazio)

- `repository/inventory/stock_repository.py` (vazio)

- `repository/sales/sale_repository.py` (vazio)

Operações de persistência:

- `CategoryRepository.create_category()` insere um `CategoryModel` e realiza commit da sessão.

- `CategoryRepository.find_all_categories()` seleciona todos os registros de `CategoryModel`.

- `CategoryRepository.find_category_by_id()` seleciona um único `CategoryModel` através da chave primária.

- `ProductRepository.create_user()` cria e persiste um `ProductModel` a partir de um `Product` de domínio.

- `ProductRepository.list_products()` seleciona todos os registros de `ProductModel`.

- `UserRepository.create_user()` cria e persiste um `UserModel` a partir de um `AppUser` de domínio.

Responsabilidades:

- A camada de repositories encapsula as operações diretas de persistência utilizando SQLAlchemy.

- Ela traduz entidades de domínio para models ORM durante escritas e retorna models ORM durante leituras.

Integração com o banco de dados:

- Os repositories utilizam `sqlalchemy.orm.Session`.

- As consultas são construídas utilizando `select()` do SQLAlchemy.

- A persistência é confirmada diretamente através de `session.commit()`.

- A sessão é fornecida por `database.connection.SessionLocal` através da dependência da API.

Estado atual da implementação:

- Parcialmente implementado.

- A persistência de categorias, produtos e usuários está implementada em nível básico.

- Os repositories de movimentação, estoque e vendas existem como arquivos, mas estão vazios.

- Não há tratamento de rollback/erros visível em torno dos commits.

- A cobertura dos repositories está limitada aos fluxos de categoria/produto do estoque e criação de usuários atualmente expostos pela API.