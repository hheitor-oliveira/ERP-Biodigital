# Implementation Plan: Product Management

**Branch**: `product-spec` | **Date**: 2026-08-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/inventory-specs/product-spec/spec.md`

## Summary

Complete backend product management for the Inventory module: authenticated creation and querying, admin-only product data and status maintenance, canonical case-insensitive names, category lifecycle validation, non-negative Decimal prices and quantity, atomic updates, and preservation of product records. The implementation extends the existing Python/FastAPI/SQLAlchemy layered structure and applies all schema changes through Alembic. Stock movement and sale execution remain outside scope.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: FastAPI 0.141.1, SQLAlchemy 2.0.52, Alembic (existing project tooling), Pydantic 2.13.4, psycopg 3.3.4

**Storage**: PostgreSQL exclusively for production and required constraint integration tests

**Testing**: pytest; existing fast tests use SQLite in-memory, with additional PostgreSQL-backed tests required for database-specific behavior

**Target Platform**: Linux server running FastAPI/Uvicorn

**Project Type**: Layered web-service API backend

**Performance Goals**: Not specified by the feature; use indexed product-name/category/status lookup and avoid N+1 category queries where practical

**Constraints**: Follow the Constitution; no new libraries; use Alembic for every schema change; preserve existing integer identifiers and authentication mechanisms; do not implement stock/sale workflows; all new functions/methods require complete type annotations

**Scale/Scope**: Incremental completion of the existing Product implementation in `domain/`, `services/`, `repository/`, `models/`, `schemas/`, `api/routes/`, and `alembic/`, with focused unit, contract, API, and PostgreSQL integration coverage

**Resolved design choices**:

- Product names use the existing Category-style canonicalization: trim, collapse internal whitespace, reject blank, uppercase; uniqueness is database-enforced on the canonical value.
- Monetary values remain `Decimal`/`NUMERIC(10,2)` and values exceeding scale are rejected rather than silently rounded.
- Status remains the existing `StatusEnum` with exactly ACTIVE, INACTIVE, and DISCONTINUED.
- Product IDs remain generated integers.
- Product creation/query requires bearer authentication; data/status mutation requires `UserModel.admin`.
- Product writes validate a complete prospective state and commit atomically.

No `NEEDS CLARIFICATION` items remain after Phase 0 research. Supporting rationale is in [research.md](research.md).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-evaluated after Phase 1 design below.*

- **Simplicity/KISS**: PASS — extends existing layers and enums; no new framework or abstraction.
- **YAGNI**: PASS — excludes stock, sale, allocation, transfer, and purchase workflows.
- **Orthogonality**: PASS — API authorization, service/domain rules, repository persistence, and database constraints have separate responsibilities.
- **ABDC/Governance**: PASS for this planning task — only design artifacts are created; implementation remains subject to explicit review and approval.
- **High cohesion/low coupling**: PASS — Product rules stay in Product/service code; Category is consulted through its existing repository/service boundary.
- **Fail fast**: PASS — request/domain validation occurs before persistence; invalid categories, names, prices, status, and identifiers are rejected clearly.
- **Type safety**: PASS — implementation tasks must type all parameters and return values, including route handlers and repository methods.
- **Exception handling**: PASS — expected domain errors are translated at the API boundary; expected database integrity conflicts become stable domain errors; no broad silent catches.
- **Stack rules**: PASS — Python, FastAPI, SQLAlchemy, PostgreSQL, and Alembic only; no new dependencies.
- **Database invariants**: PASS — foreign key, uniqueness, non-negative checks, defaults, and status constraint are planned for PostgreSQL/Alembic and verified with PostgreSQL tests.

No gate violations require complexity justification.

## Project Structure

### Documentation (this feature)

```text
specs/inventory-specs/product-spec/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── product-api.md
└── tasks.md                 # created later by /speckit-tasks
```

### Source Code (repository root)

```text
domain/
├── enums/status.py
└── inventory/product.py
models/inventory_models/
├── category_model.py
└── product_model.py
repository/inventory/
├── category_repository.py
└── product_repository.py
services/inventory/
├── category_service.py
└── product_service.py
schemas/
└── product_schema.py
api/routes/inventory_routes/
├── category_routes.py
└── product_routes.py
alembic/
├── env.py
└── versions/<new_product_management_revision>.py
tests/
├── contract/test_product_management.py
├── integration/test_product_create.py
├── integration/test_product_query.py
├── integration/test_product_update.py
├── integration/test_product_status.py
└── integration/test_product_constraints_postgres.py
```

**Structure Decision**: Use the repository's existing single-project layered API layout. Product domain behavior belongs in `domain/inventory/product.py` and `services/inventory/product_service.py`; persistence belongs in the Product repository/model and its Alembic revision; external HTTP behavior belongs in the Product route and schema modules. Tests follow the existing contract/integration split.

## Phase 0: Research Output

Completed in [research.md](research.md). It resolves architecture, authorization, canonical naming/uniqueness, money precision, status representation/transitions, database invariants, transaction boundaries, and PostgreSQL test requirements.

## Phase 1: Design Output

- [data-model.md](data-model.md): entities, fields, relationships, invariants, transitions, and transaction boundaries.
- [contracts/product-api.md](contracts/product-api.md): authenticated API operations, request/response shapes, permissions, status codes, and delete behavior.
- [quickstart.md](quickstart.md): migration, automated, manual, and acceptance validation scenarios.

## Implementation sequencing guidance

1. Add/adjust domain validation and status transition behavior with unit/contract coverage.
2. Align SQLAlchemy model and create an Alembic migration for canonical uniqueness and all database invariants.
3. Implement repository/service create, query/filter, update, status, and explicit no-delete behavior with atomic transaction handling.
4. Implement typed Pydantic schemas and FastAPI routes with authentication/admin enforcement and stable error mapping.
5. Add API and PostgreSQL integration tests, run the quickstart validation, and verify regression behavior.

## Post-design Constitution Check

- **Stack and migration rules**: PASS — design uses only existing stack and plans Alembic-only schema changes.
- **ABDC**: PASS — no implementation code is included; each implementation block must be proposed for review before application.
- **Type safety and exception boundaries**: PASS — contracts and sequencing require typed layers and domain-to-HTTP error translation.
- **Database correctness**: PASS — canonical uniqueness, foreign key, monetary/quantity checks, status constraints, defaults, and atomic rollback have explicit artifacts and PostgreSQL validation.
- **Scope**: PASS — stock and sale operations are explicitly excluded.

## Complexity Tracking

No violations. No new project, dependency, or architectural abstraction is introduced.
