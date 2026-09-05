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
- Completed T010 by centralizing active-category validation and CategoryModel-to-Category conversion in `services/inventory/category_service.py`.
- Product creation now requires an existing active category through the shared CategoryService boundary.
- Product listing now reuses the shared CategoryService domain conversion while preserving the existing missing-category error behavior.
- Completed T011 by defining typed Product response, creation, query-filter, update, and status request schemas in `schemas/product_schema.py`.
- Product schemas now validate finite, non-negative Decimal monetary values within `99999999.99` and with at most two decimal places.
- Product schemas now validate non-blank names with the existing 100-character model limit, use `StatusEnum`, support optional query filters, and represent partial updates.
- Explicit null values are rejected for update fields, and `UpdateProductSchema.has_updates()` identifies empty update payloads for application-layer rejection.
- Completed T012 by centralizing authenticated-user and admin dependencies in `api/dependencies.py`.
- Product routes now require the reusable authenticated-user dependency at the router boundary.
- Product-domain exception-to-HTTP mapping is explicit in `api/routes/inventory_routes/product_routes.py` for validation, category, not-found, duplicate-name, transition, and deletion errors.
- Completed T013 by creating `tests/contract/test_product_management.py` with contract coverage for authenticated product creation, canonical representation, authentication requirements, empty listing, invalid creation data, category errors, and duplicate canonical names.
- Completed T014 by creating `tests/integration/test_product_create.py` with integration coverage for valid creation, canonical persistence, missing and inactive categories, missing required fields, negative prices, excessive Decimal scale, and duplicate canonical names.

## Where It Stopped

T014 is complete. Product integration tests now cover the planned creation endpoint and persistence/error behavior for the full T014 scenario set.

No unrelated task was started. Execution stopped before T015.

Validation:

- The new migration passed Python syntax validation with `.venv/bin/python -m py_compile`.
- Alembic revision-chain validation passed; `c1d2e3f4a5b6` is the current head and revises `bba7ec3010b3`.
- `.venv/bin/alembic upgrade head` completed successfully using `PostgresqlImpl`.
- PostgreSQL upgrade read-back validation passed for revision `c1d2e3f4a5b6`, constraint `product_product_name_key`, and zero non-canonical product names.
- PostgreSQL downgrade read-back validation passed after removing `product_product_name_key`; the migration was then reapplied and the upgrade read-back passed again.
- Category contract tests passed: 8 passed.
- Direct validation of active, inactive, and missing category handling passed.
- Python syntax validation passed for `services/inventory/category_service.py` and `services/inventory/product_service.py`.
- Selected Category integration suite produced 11 passes and 7 existing authentication-gate failures (`401 Unauthorized`); those failures occurred before the modified service logic was reached.
- Python syntax validation passed for `schemas/product_schema.py`.
- Direct schema validation passed for valid creation data, blank names, negative/excess-scale/overflow monetary values, enum parsing, optional query filters, empty updates, partial updates, and explicit null update rejection.
- Contract test collection passed: 6 tests collected from `tests/contract/test_product_management.py`.
- Contract test execution currently reports 6 expected failures with `404 Not Found` because the planned `/product` endpoints are not implemented yet; no production code was changed during T013.
- The contract test run also reported one existing Pydantic deprecation warning in `schemas/user_schema.py`.
- Python syntax validation passed for `tests/integration/test_product_create.py` with `.venv/bin/python -m py_compile`.
- Integration test collection passed with 12 tests collected from `tests/integration/test_product_create.py`.
- T014 integration execution reported 11 failures and 1 pass because the planned `POST /product` endpoint is not implemented yet and returns `404 Not Found`; the one passing test verified no product was persisted after a missing-category request.
- The T014 integration run also reported the existing Pydantic deprecation warning in `schemas/user_schema.py`.

## Next Task

T015 — Implementar a construção tipada e a persistência transacional de Product com comportamento de commit/rollback em `repository/inventory/product_repository.py`.

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
- `services/inventory/product_service.py`
- `domain/inventory/product.py`
- `schemas/product_schema.py`
- `specs/inventory-specs/product-spec/spec.md`
- `specs/inventory-specs/product-spec/contracts/product-api.md`
- `api/dependencies.py`
- `api/routes/inventory_routes/product_routes.py`
- `api/routes/auth_routes.py`
- `domain/exceptions/__init__.py`
- `tests/conftest.py`
- `tests/contract/test_product_management.py`
- `tests/integration/test_product_create.py`
- `repository/inventory/product_repository.py`
