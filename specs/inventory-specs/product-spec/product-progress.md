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
- Completed T015 by implementing typed Product persistence construction in `repository/inventory/product_repository.py`.
- Product persistence now explicitly stores the canonical name, category identifier, prices, available quantity, and status.
- Product creation now returns the persisted `ProductModel` after commit and refresh.
- SQLAlchemy persistence failures now roll back the session and re-raise the original exception, preserving single-transaction behavior.
- Completed T016 by implementing authenticated product-creation service validation through the active-category boundary and Product domain invariants.
- Product creation now explicitly initializes `available_quantity` to zero and `status` to `StatusEnum.ACTIVE`, returns the persisted `ProductModel`, and translates product-create integrity failures into `DuplicateProductNameError`.

## Where It Stopped

T016 is complete. Execution stopped after implementing Product creation service validation and duplicate-integrity translation.

No unrelated task was started. T017 was not started.

Validation:

- `.venv/bin/python -m py_compile services/inventory/product_service.py` passed.
- `.venv/bin/python -m pytest tests/integration/test_product_create.py -q` collected and executed 12 tests: 1 passed and 11 failed because `/product` is not yet implemented and returned `404` for the endpoint scenarios.
- The failed endpoint execution is an existing dependency on T017/T018, not a service syntax failure.
- The run reported the existing Pydantic deprecation warning in `schemas/user_schema.py`.
- Repository-level transaction smoke validation from T015 remains passed.

## Next Task

T017 — Implementar `POST /product` em `api/routes/inventory_routes/product_routes.py` com autenticação bearer, resposta `201` e mapeamento estável de erros `400`, `404`, `409` e `401`.

## Required Files

- `.specify/memory/constitution.md`
- `specs/inventory-specs/product-spec/product-progress.md`
- `specs/inventory-specs/product-spec/tasks.md`
- `specs/inventory-specs/product-spec/contracts/product-api.md`
- `api/dependencies.py`
- `api/routes/inventory_routes/product_routes.py`
- `domain/exceptions/__init__.py`
- `services/inventory/product_service.py`
- `schemas/product_schema.py`
- `models/user_model/user_model.py`
- `tests/conftest.py`
- `tests/contract/test_product_management.py`
- `tests/integration/test_product_create.py`
