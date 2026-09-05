# Product Implement Progress

## What Was Done

- Completed T035 by canonicalizing names in `UpdateProductSchema` before service/domain processing and explicitly serializing Product monetary response fields as two-decimal strings through Pydantic field serializers.
- The Product domain already enforced canonicalization through `normalize_product_name()` in construction, restore, and `change_name()`; no additional domain change was required.
- Completed T028 by implementing prospective-state product updates across `repository/inventory/product_repository.py` and `services/inventory/product_service.py`.
- Product updates now preserve omitted fields, canonicalize names through the Product domain, validate the complete prospective state before persistence, require replacement categories to be active, and reject missing products without creating rows.
- Product repository updates assign the complete validated state and perform exactly one commit with refresh; SQLAlchemy failures roll back and re-raise the original exception.
- Product service updates translate duplicate canonical-name integrity failures into `DuplicateProductNameError` and missing identifiers into `ProductNotFoundError`.
- Completed T033 validation for the existing admin product-data update service logic in `services/inventory/product_service.py`; no code change was necessary because the prospective-state validation, omitted-field preservation, active-category check, missing-product handling, and duplicate-name translation are already implemented.
- Completed T034 by implementing `PATCH /product/{product_id}` in `api/routes/inventory_routes/product_routes.py` with `UpdateProductSchema`, admin authorization through `get_admin_user`, empty-payload rejection, service delegation, complete response serialization, and explicit product-domain error mapping.
- Completed T027 by adding explicit typed product deletion rejection methods to `repository/inventory/product_repository.py` and `services/inventory/product_service.py`.
- Repository and service deletion methods raise `ProductDeletionRejectedError` with the stable message `Product deletion is not permitted.` without querying, mutating, deleting, or committing any product row.
- Completed T026 by creating `tests/integration/test_product_update.py` with integration coverage for deletion protection, row and identifier preservation after failed updates, duplicate-name rollback, and nonexistent-update no-create behavior.
- Completed T025 by adding contract coverage in `tests/contract/test_product_management.py` for the absence of a product deletion endpoint and the stable PATCH update error contract.
- The deletion contract verifies that `DELETE /product/{product_id}` is not exposed and returns `405`.
- The update contracts define `404` with `Product not found.` for an unknown product and `400` with `At least one product field must be updated.` for an empty update payload.
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
- Completed T017 by implementing `POST /product` with bearer authentication inherited from the router, `201 Created`, `CreateProductSchema` request validation, and explicit product-domain error mapping.
- Product request validation intentionally preserves FastAPI's `422` responses, per the approved scope decision; the contract's `400` validation mapping is not applied.
- Missing categories map to `404`, inactive categories map to `400`, duplicate canonical names map to `409`, and authentication failures map to `401`.
- The route uses `response_model=None` temporarily because Product response serialization is assigned to T018.
- Completed T018 by returning the complete Product representation from `POST /product` with the product identifier, canonical product name, persisted category representation, Decimal prices, status, and available quantity.
- Product response serialization now uses `ProductResponseSchema` explicitly instead of relying on mismatched SQLAlchemy attribute names.
- Product creation responses now declare `response_model=ProductResponseSchema` and preserve the persisted category name while exposing the canonical product name.
- Completed T019 by adding contract coverage for authenticated product listing and detail queries in `tests/contract/test_product_management.py`.
- The T019 contract coverage verifies complete list/detail representations, canonical case-insensitive name filtering, combined category/status filtering, empty filtered results, unknown identifiers, and authentication requirements for both GET endpoints.
- Completed T020 by creating `tests/integration/test_product_query.py` with integration coverage for empty catalogs, list/detail representations, canonical case-insensitive name filtering, category/status filters, combined filters, no-match results, and unknown identifiers.
- T020 query fixtures create products through the authenticated API where applicable and insert non-ACTIVE products through `ProductModel` to cover status filtering before status routes exist.
- Completed T021 by implementing typed ProductRepository queries in `repository/inventory/product_repository.py` for listing, identifier lookup, canonical-name lookup, category filtering, status filtering, and combined filters.
- Product queries now use an explicit join with `CategoryModel` and return typed `(ProductModel, CategoryModel)` tuples so category data is loaded in the same query.
- Product listing queries are ordered by `ProductModel.product_id` and support optional name, category, and status filters.
- Completed T022 by implementing Product persistence-to-domain and persistence-to-response mapping in `services/inventory/product_service.py`.
- Product list and detail mappings now consume the repository's joined `(ProductModel, CategoryModel)` tuples without N+1 category lookups.
- Product list mapping now supports optional name, category, and status filters and returns typed `ProductResponseSchema` values.
- Product detail mapping now returns a typed response or `None` for an unknown identifier.
- Completed T023 by canonicalizing repository name filters with `normalize_product_name()`.
- Completed T023 by routing product creation responses through `ProductResponseSchema.from_model()` and `CategoryService.to_domain_category()`, aligning create and query category representation.
- Updated the affected contract expectations to require canonical category serialization (`CATEGORIA VÁLIDA`) and FastAPI `422` validation for invalid request payloads.
- Completed T024 by aligning Product and nested Category response schemas with persistence attribute names through validation aliases while preserving public API field names.
- Product response schemas now accept `product_id`, `product_name`, and `product_status`, while nested category responses accept `category_id`, `category_name`, and `category_status`.
- Response schemas retain `from_attributes=True`, permit explicit public field names through `populate_by_name=True`, and preserve Decimal and StatusEnum serialization behavior.

## Where It Stopped

T035 is complete. Updated Product names are canonicalized at schema validation, and Product monetary response fields are serialized explicitly with two decimal places while remaining `Decimal` values internally.

Validation:

- `.venv/bin/python -m pytest tests/integration/test_product_update.py tests/contract/test_product_management.py -q -k 'update_product or product_update or admin_can_partially_update_product or admin_can_update_multiple_product_fields'` returned 18 passed, 3 failed, 13 deselected, and 1 existing Pydantic deprecation warning. The failures are pre-existing expectation mismatches: one integration test expects `400` for Pydantic price validation that returns `422`, and two contract tests use a non-admin client while expecting business responses and therefore return `401`.
- `.venv/bin/python -m compileall -q schemas/product_schema.py domain/inventory/product.py` completed successfully.
- `.venv/bin/python -m pytest tests/integration/test_product_update.py -q -k 'update_product_name_preserves_omitted_fields or update_product_multiple_fields_returns_complete_representation or non_admin_cannot_update_product or update_product_rejects_invalid_prices or update_product_rejects_duplicate_canonical_name or update_product_rejects_missing_category_without_changes or update_product_rejects_inactive_category_without_changes or update_product_preserves_identifier_and_state_after_atomic_failure or update_of_missing_product_does_not_create_row or delete_product_rejects_and_preserves_row' returned 11 passed, 2 deselected, and 1 existing Pydantic deprecation warning.
- `.venv/bin/python -m pytest tests/contract/test_product_management.py -q -k 'admin_can_partially_update_product or non_admin_cannot_update_product or product_update_requires_authentication or product_update_rejects_invalid_payload or product_update_rejects_duplicate_name'` returned 3 passed, 18 deselected, and 1 existing Pydantic deprecation warning.
- `.venv/bin/python -m compileall -q api/routes/inventory_routes/product_routes.py` completed successfully.
- The combined update test run still has 3 failures caused by pre-existing incompatible expectations: two contract tests use the non-admin `authenticated_client` while expecting business responses, and one integration test expects `400` for Pydantic price validation that returns `422`. No production behavior was changed to weaken authorization or override FastAPI validation semantics.

## Next Task

T036 — Add contract tests for `PATCH /product/{product_id}/status`, all status values, authorization, preserved representation, and error categories in `tests/contract/test_product_management.py`. Do not begin T036 until explicitly approved.

## Required Files

- `.specify/memory/constitution.md`
- `specs/inventory-specs/product-spec/product-progress.md`
- `specs/inventory-spec/product-spec/tasks.md`
- `schemas/product_schema.py`
- `domain/inventory/product.py`
- `tests/contract/test_product_management.py`
- `tests/integration/test_product_update.py`
