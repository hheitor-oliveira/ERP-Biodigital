## Levantamento Necessário para Completar o Escopo do Projeto

Esta seção registra as informações que ainda precisam ser definidas para que a documentação do ERP-Biodigital seja completa, consistente e baseada em requisitos confirmados.

### Informações já identificadas

Atualmente, o projeto já possui informações sobre:

- Objetivo geral do ERP.
- Problemas atuais da empresa.
- Arquitetura em camadas.
- Tecnologias obrigatórias.
- Módulos inicialmente previstos.
- Requisitos funcionais básicos de estoque, vendas e usuários.
- Algumas regras de negócio.
- Modelo inicial de entidades e banco de dados.
- Estado atual da implementação do módulo de estoque.
- Padrões de domínio, serviços, repositórios, schemas e API.

As definições abaixo ainda são necessárias para fechar o escopo sem presumir requisitos.

### 1. Visão geral do produto

- O ERP será utilizado somente pela Biodigital ou será projetado como um produto genérico?
- Qual é o objetivo principal da primeira versão?
- O projeto continua sendo acadêmico/de estudos ou será utilizado em produção?
- Quais módulos serão realmente desenvolvidos?
- Quais módulos pertencem ao MVP, ao futuro ou estão fora do escopo?

Módulos atualmente mencionados:

- Estoque.
- Vendas.
- Usuários e autenticação.
- Financeiro.
- Marketing.
- Chamados.
- Monitoramento de interfaces.
- CRM.
- Chat interno.
- Gestão de parceiros e clientes.

### 2. Usuários e permissões

Para cada perfil, definir nome, responsabilidades, módulos acessíveis, operações permitidas e operações proibidas.

Confirmar também:

- Se os cargos `ADMIN`, `TECHNIQUE` e `ATTENDANT` estão corretos.
- Se existirão outros cargos.
- Se as permissões serão fixas por cargo ou configuráveis.
- Se um usuário poderá possuir mais de um cargo.
- Quem poderá criar, editar, desativar e reativar usuários.
- Quais ações deverão ser auditadas.

### 3. Estoque

#### 3.1 Produtos

Definir:

- Campos obrigatórios.
- Código interno, SKU e código de barras.
- Marca e unidade de medida.
- Categoria obrigatória ou opcional.
- Preço de custo e preço de venda.
- Estoque mínimo e máximo.
- Número de série, lote e validade.
- Se o produto pode representar serviço ou somente item físico.
- Se produtos inativos podem ser vendidos.
- Se produtos podem ser excluídos ou somente desativados.
- Se o nome deve ser único.
- Regra de normalização do nome.

#### 3.2 Categorias

Definir:

- Se haverá apenas nome e status.
- Se categorias poderão ser hierárquicas.
- Se o nome deverá ser único.
- Se uma categoria poderá ser desativada com produtos associados.
- Se produtos poderão trocar de categoria.
- Se a exclusão física será proibida definitivamente.

#### 3.3 Estoques

Definir:

- O que representa um estoque: loja, filial, depósito, sala ou outro local.
- Se haverá mais de um estoque.
- Se um produto poderá existir em vários estoques.
- Quem poderá criar e editar estoques.
- Se estoques poderão ser desativados.
- Se será possível transferir produtos entre estoques.
- Se haverá um estoque central.
- Como será calculado o estoque total.

#### 3.4 Movimentações

Confirmar os tipos oficiais:

- Entrada.
- Saída.
- Transferência.
- Ajuste.
- Devolução.
- Perda.
- Inventário.

Para cada tipo, definir:

- Quem poderá executar.
- Campos obrigatórios.
- Necessidade de motivo.
- Necessidade de aprovação.
- Alteração automática da quantidade disponível.
- Possibilidade de cancelamento ou estorno.
- Possibilidade de edição após confirmação.
- Regras de auditoria.

#### 3.5 Inventário e auditoria

Definir:

- Como será realizado o inventário físico.
- Como divergências serão tratadas.
- Se haverá ajuste automático ou aprovação manual.
- Filtros disponíveis na auditoria.
- Possibilidade de exportar relatórios.
- Tempo de preservação dos registros.

### 4. Vendas

O módulo de vendas ainda está majoritariamente em modelagem. É necessário especificar:

#### 4.1 Venda

- Quem poderá iniciar uma venda.
- Se será necessário cadastrar um cliente.
- Se haverá venda para consumidor não identificado.
- Campos obrigatórios da venda.
- Possibilidade de salvar como rascunho.
- Momento em que a venda é iniciada.
- Momento em que a venda é confirmada.
- Regras de cancelamento, devolução e estorno.
- Se uma venda concluída poderá ser editada.

#### 4.2 Itens da venda

- Quantidade mínima.
- Permissão para quantidades fracionadas.
- Possibilidade de alterar o preço manualmente.
- Venda de produtos inativos.
- Uso do preço atual ou do preço registrado no momento da venda.
- Desconto por item ou somente na venda inteira.
- Quem poderá conceder descontos.
- Limite máximo de desconto.

#### 4.3 Pagamentos

Confirmar:

- Formas de pagamento aceitas.
- Se uma venda poderá possuir múltiplos pagamentos.
- Se haverá pagamento parcial.
- Regras de troco.
- Cancelamento de pagamentos.
- Tratamento específico para cartão, PIX e dinheiro.
- Integração com gateway externo.
- Conciliação financeira.

#### 4.4 Nota fiscal e recibos

Definir:

- Se a nota fiscal será apenas um PDF interno ou terá integração fiscal oficial.
- Tipo de documento emitido.
- Integração com SEFAZ, prefeitura ou outro serviço.
- Dados fiscais necessários.
- Quem poderá emitir, cancelar e reemitir documentos.
- Formato e periodicidade do extrato de caixa.

### 5. Clientes, parceiros e CRM

Confirmar se estes recursos fazem parte da primeira versão:

- Cadastro de clientes, empresas e fornecedores.
- Cadastro de parceiros.
- Contatos e endereços.
- Histórico de compras.
- Histórico de atendimento.
- Status do cliente.
- Responsável pelo cliente.
- Funil de vendas.
- Tarefas e acompanhamentos.
- Integração com vendas e estoque.

### 6. Financeiro

Definir se haverá:

- Contas a pagar.
- Contas a receber.
- Fluxo de caixa.
- Contas bancárias.
- Categorias financeiras.
- Centro de custos.
- Conciliação bancária.
- Fechamento de caixa.
- Comissões.
- Parcelamento.
- Controle de inadimplência.
- Relatórios financeiros.
- Integração com vendas.

### 7. Chamados, monitoramento e chat interno

Confirmar se esses módulos fazem parte do escopo e definir seus fluxos.

Para chamados:

- Quem abre chamados.
- Tipos, prioridades e status.
- Responsáveis.
- SLA.
- Comentários, anexos e histórico.
- Notificações.

Para monitoramento de interfaces:

- Interfaces monitoradas.
- Critério de falha.
- Frequência de verificação.
- Histórico de indisponibilidade.
- Alertas.
- Integrações externas.

Para chat interno:

- Conversas individuais.
- Grupos e canais.
- Anexos.
- Histórico.
- Notificações.
- Retenção de mensagens.

### 8. Autenticação e segurança

Confirmar:

- Login por usuário e senha.
- Recuperação de senha.
- Expiração de senha.
- Bloqueio após tentativas inválidas.
- Sessão ou JWT.
- Validade do token e uso de refresh token.
- Autenticação em dois fatores.
- Controle de acesso por endpoint.
- Auditoria de login e ações.
- Tratamento de dados sensíveis.
- Requisitos da LGPD.
- Exclusão ou anonimização de dados pessoais.

### 9. Requisitos não funcionais

O arquivo atual de requisitos não funcionais ainda está incompleto. Definir:

- Tempo máximo de resposta esperado.
- Quantidade estimada de usuários simultâneos.
- Volume estimado de produtos, vendas e movimentações.
- Disponibilidade desejada.
- Estratégia de backup e restauração.
- Retenção de dados.
- Logs e monitoramento.
- Requisitos de segurança.
- Compatibilidade de navegadores.
- Responsividade e acessibilidade.
- Ambientes de desenvolvimento, homologação e produção.
- Estratégia de deploy.
- Necessidade de Docker e CI/CD.

### 10. Interface do sistema

Definir:

- Se haverá frontend próprio.
- Tecnologia do frontend.
- Se a API será consumida por aplicação web, desktop ou mobile.
- Telas necessárias.
- Fluxos principais de cada tela.
- Necessidade de dashboard.
- Relatórios e exportações.
- Necessidade de impressão.
- Responsividade.
- Identidade visual da Biodigital.

### 11. Integrações externas

Listar todas as integrações desejadas, incluindo as futuras:

- Emissão fiscal.
- Gateways de pagamento.
- Bancos.
- E-mail.
- WhatsApp.
- Sistemas atuais.
- Bconnect.
- Serviços de autenticação.
- Armazenamento de arquivos.
- Provedores de monitoramento.

Para cada integração, definir objetivo, dados enviados, dados recebidos, frequência, responsável e obrigatoriedade.

### 12. Dados e banco de dados

Confirmar:

- Modelo relacional definitivo.
- Relacionamentos entre entidades.
- Campos obrigatórios.
- Regras de unicidade.
- Políticas de exclusão.
- Histórico de alterações.
- Auditoria.
- Estratégia de migrações.
- Dados iniciais obrigatórios.
- Necessidade de seed.
- Política de retenção.
- Processo de backup e restauração.

### 13. API

Definir:

- Prefixo da API, por exemplo `/api/v1`.
- Padrão de resposta e de erro.
- Paginação, ordenação e filtros.
- Versionamento.
- Autenticação dos endpoints.
- Códigos HTTP esperados.
- Limite de requisições.
- Formato de datas.
- Formato de valores monetários.
- Convenção de nomes.
- Compatibilidade entre versões.

### 14. Relatórios

Listar os relatórios desejados, por exemplo:

- Estoque atual.
- Movimentações.
- Produtos abaixo do estoque mínimo.
- Vendas por período.
- Vendas por usuário.
- Vendas por forma de pagamento.
- Fechamento de caixa.
- Produtos mais vendidos.
- Clientes.
- Financeiro.
- Auditoria.

Para cada relatório, definir filtros, campos exibidos, formato, permissões e período máximo de consulta.

### 15. Escopo e roadmap

Para cada funcionalidade, classificar como:

- MVP.
- Segunda versão.
- Futuro.
- Fora do escopo.

Também definir:

- O que significa considerar a primeira versão pronta.
- Critérios de aceite.
- Ordem de implementação.
- Funcionalidades bloqueadoras.
- O que não será desenvolvido.

### 16. Documentação desejada

Confirmar quais documentos deverão ser criados. A recomendação é incluir:

- Visão geral do sistema.
- Visão de negócio.
- Escopo e roadmap.
- Requisitos funcionais.
- Requisitos não funcionais.
- Casos de uso.
- Regras de negócio.
- Arquitetura.
- Modelo de domínio.
- Modelo de dados.
- Documentação da API.
- Guia de instalação.
- Guia de desenvolvimento.
- Guia de operação.
- Guia de permissões.
- Guia de testes.
- Guia de deploy.
- Glossário.
- Decisões arquiteturais.
- Limitações conhecidas.
- Changelog.

### Questionário para fechar o escopo

Responder aos itens abaixo para permitir a criação da documentação completa:

```text
1. Objetivo da primeira versão:
2. Usuários e cargos:
3. Módulos do MVP:
4. Módulos futuros:
5. Módulos fora do escopo:
6. Fluxo completo de estoque:
7. Fluxo completo de vendas:
8. Formas de pagamento:
9. Clientes, fornecedores e parceiros:
10. Financeiro:
11. Chamados, monitoramento e chat:
12. Autenticação e permissões:
13. Integrações externas:
14. Requisitos não funcionais:
15. Relatórios:
16. Frontend:
17. Ambiente de execução e deploy:
18. Critérios para considerar o MVP concluído:
19. Documentos desejados:
20. Decisões ou observações adicionais:
```

Os itens prioritários para iniciar a documentação são: objetivo da primeira versão, cargos, módulos do MVP, fluxo de estoque, fluxo de vendas, autenticação, requisitos não funcionais e critérios de conclusão do MVP.
