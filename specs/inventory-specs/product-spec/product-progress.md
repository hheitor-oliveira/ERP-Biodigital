# Product Implement Progress

## What Was Done

- Completed T003 by creating `docs/code/inventory/product-management.md`.
- Completed T004 by adding the typed product-domain exception hierarchy in `domain/exceptions/__init__.py`.
- Completed T005 by adding canonical product-name normalization and blank-name validation in `domain/inventory/product.py`.
- Applied the same canonicalization rule during Product construction and `change_name`.
- Completed T006 by adding runtime validation for Product monetary values, quantity, and status in `domain/inventory/product.py`.
- Monetary values now require finite `Decimal` instances, must be non-negative, must fit `NUMERIC(10,2)`, and must not contain more than two decimal places.
- Product quantity now requires a non-negative integer; boolean values are rejected because Python treats `bool` as a subclass of `int`.
- `add_stock` now rejects negative quantities and validates the resulting quantity.
- Product status now requires a valid `StatusEnum` value.
- Applied the T006 validations during Product construction, restore, monetary changes, stock addition, and status changes.
- Completed T007 by adding typed Product restore, field-change, status-transition, and capability methods in `domain/inventory/product.py`.
- Product status transitions now allow ACTIVE to INACTIVE or DISCONTINUED, allow reactivation only from INACTIVE or DISCONTINUED, accept idempotent transitions, and reject unsupported transitions with typed domain errors.
- Product reactivation now rejects inactive categories with `InvalidProductCategoryError`.
- Added `can_add_stock` and `can_sell` capability predicates without implementing stock movement or sale execution.
- Documented the Product migration command from the product quickstart:
  - `source .venv/bin/activate`
  - `alembic upgrade head`
- Documented the contract/integration, PostgreSQL marker, and full regression validation commands.
- Included the manual API validation scenarios and acceptance-evidence requirements from the quickstart.
- Completed T008 by updating `models/inventory_models/product_model.py` with required fields, explicit Python/server defaults, canonical-name uniqueness persistence, non-negative value constraints, `NUMERIC(10,2)` monetary columns, the category foreign key, and non-null valid status mapping.
- Completed T009 by creating `alembic/versions/c1d2e3f4a5b6_product_management.py`.
- The T009 migration canonicalizes existing PostgreSQL product names by trimming, collapsing whitespace, and uppercasing before adding the database unique constraint `product_product_name_key`.
- The migration includes a downgrade path that removes the canonical product-name uniqueness constraint.

## Where It Stopped

T009 is complete. The Product mapping and Alembic migration now express the persistence invariants required by the Product specification, including canonical product-name persistence and database uniqueness.

No unrelated task was started. Execution stopped before T010.

Validation:

- The new migration passed Python syntax validation with `.venv/bin/python -m py_compile`.
- Alembic revision-chain validation passed; `c1d2e3f4a5b6` is the current head and revises `bba7ec3010b3`.
- `.venv/bin/alembic upgrade head` completed successfully using `PostgresqlImpl`.
- PostgreSQL upgrade read-back validation passed for revision `c1d2e3f4a5b6`, constraint `product_product_name_key`, and zero non-canonical product names.
- PostgreSQL downgrade read-back validation passed after removing `product_product_name_key`; the migration was then reapplied and the upgrade read-back passed again.

## Next Task

T010 — Refatorar a conversão compartilhada de Category para domínio e a validação de categoria ativa em `services/inventory/category_service.py`, preservando o comportamento existente de Category.

## Required Files

- `.specify/memory/constitution.md`
- `specs/inventory-specs/product-spec/product-progress.md`
- `specs/inventory-specs/product-spec/tasks.md`
- `models/inventory_models/product_model.py`
- `models/inventory_models/category_model.py`
- `domain/enums/status.py`
- `alembic/env.py`
- `alembic/versions/`
- `specs/inventory-specs/product-spec/data-model.md`
- `specs/inventory-specs/product-spec/plan.md`
- `specs/inventory-specs/product-spec/research.md`
- `services/inventory/category_service.py`
- `domain/inventory/category.py`
