# Product Management Planning Research

## Decision 1: Extend the existing layered backend

- Decision: Keep the existing domain, service, repository, SQLAlchemy model, Pydantic schema, FastAPI route, and Alembic layers. Product implementation should follow the working Category patterns while correcting the incomplete Product paths.
- Rationale: The repository already uses this separation in `domain/inventory/category.py`, `services/inventory/category_service.py`, `repository/inventory/category_repository.py`, `models/inventory_models/category_model.py`, and `api/routes/inventory_routes/category_routes.py`. This satisfies the project structure and avoids a new abstraction.
- Alternatives considered: A direct route-to-ORM implementation was rejected because it would violate the existing layering and weaken domain/business-rule isolation.

## Decision 2: Use the existing authentication boundary and explicit admin guard

- Decision: Product list, detail, and create operations use the existing bearer-token dependency. Product edits, status changes, and any deletion attempt use the authenticated user and require `UserModel.admin`.
- Rationale: `api/dependencies.py` provides `verify_access_token`, and `api/routes/auth_routes.py` already checks the `admin` flag for protected administrative behavior. Authorization belongs at the API boundary; product business rules remain in the service/domain layer.
- Alternatives considered: Adding a new role or permission library was rejected because `UserModel.admin` already exists and the constitution prohibits unapproved dependencies.

## Decision 3: Canonical product names are normalized before storage and lookup

- Decision: Trim leading/trailing whitespace, collapse repeated internal whitespace, reject the blank result, and store the canonical value in uppercase. Use the same canonical value for uniqueness and name lookup. Enforce uniqueness in PostgreSQL with a dedicated canonical-name column and a unique constraint, or an equivalent migration-level unique expression if implementation proves the extra column unnecessary.
- Rationale: Application-only duplicate checks race under concurrent requests. A database constraint is the final invariant. Reusing the Category normalization convention makes behavior predictable in this codebase.
- Alternatives considered: Case-insensitive comparison only at the service layer was rejected. A functional unique index on `upper(trim(product_name))` avoids a second column but does not capture internal-whitespace normalization as transparently; the implementation task should prefer the dedicated column unless the existing schema constraints make it impractical.

## Decision 4: Preserve the current monetary contract explicitly

- Decision: Keep monetary values as Python `Decimal` and PostgreSQL/SQLAlchemy `NUMERIC(10,2)`, reject negative values and values with more than two fractional digits rather than silently rounding. Validate total precision consistently in Pydantic, the service, the model/migration, and integration tests.
- Rationale: The existing `ProductModel` uses `Numeric(10, 2)`, and Decimal avoids floating-point errors. Retaining the established precision is the smallest compatible design.
- Alternatives considered: Floating-point values were rejected for monetary data. Increasing precision was not justified by the feature and would require an explicit product decision.

## Decision 5: Use explicit status values and transition validation

- Decision: Continue using `StatusEnum.ACTIVE`, `INACTIVE`, and `DISCONTINUED` in Python and PostgreSQL. Status changes are service operations with validation, not unrestricted field assignment. Creation starts ACTIVE; reactivation requires an active category. Product rows are never deleted or recreated.
- Rationale: The enum already exists in `domain/enums/status.py`, and the specification requires the three values to remain distinct. Explicit transitions protect stock-entry semantics while leaving sale execution to the future Sale feature.
- Alternatives considered: A free-form status string was rejected because it permits invalid states. A new lifecycle framework was rejected as unnecessary for the three-state scope.

## Decision 6: Enforce invariants in both service and database

- Decision: Validate category existence/activity, prices, names, statuses, and quantity in the service/domain boundary; enforce category foreign key, unique canonical name, non-negative prices and quantity, non-null required fields, and valid status at PostgreSQL level through an Alembic migration.
- Rationale: Service validation gives clear domain/API errors, while database constraints protect against races and non-API writes. The constitution requires PostgreSQL and Alembic for schema changes.
- Alternatives considered: Service-only validation was rejected because it cannot guarantee concurrency safety or protect direct database access.

## Decision 7: Make writes atomic

- Decision: Product create, edit, and status operations validate the complete prospective state and commit once. Expected integrity failures are translated at the repository/service boundary and rolled back; API routes map stable domain errors to HTTP responses. Failed updates preserve every prior field.
- Rationale: The specification explicitly forbids partial persistence, and a single transaction is the simplest way to guarantee it.
- Alternatives considered: Committing each field separately was rejected because it creates partial-update states. Broad exception swallowing was rejected by the constitution.

## Decision 8: Validate against PostgreSQL in addition to existing fast tests

- Decision: Add unit/contract tests for normalization and domain rules, API integration tests for authentication, authorization, responses, filters, and not-found behavior, and PostgreSQL-backed integration coverage for constraints, Decimal precision, foreign keys, rollback, and duplicate-name races.
- Rationale: Existing `tests/conftest.py` uses SQLite in memory for fast tests, but SQLite cannot be the sole validation for PostgreSQL-specific constraints. The project constitution explicitly requires PostgreSQL as the database.
- Alternatives considered: SQLite-only testing was rejected because it can mask PostgreSQL constraint, enum, collation, and transaction differences.

## Resolved planning assumptions

- The existing integer product/category identifiers remain the identifier type.
- Product creation and querying require an authenticated user; administrative mutations require `admin=True`.
- `available_quantity` is initialized to zero and is not modified by this feature's API. Stock quantity operations remain out of scope.
- The API contract will use resource-oriented product routes while preserving the existing route module; exact paths are documented in `contracts/product-api.md` for implementation review.
- No new dependency is required.
