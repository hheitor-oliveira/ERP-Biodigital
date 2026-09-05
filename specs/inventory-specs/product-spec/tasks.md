---

description: "Actionable implementation tasks for Product Management"
---

# Tasks: Product Management

**Input**: Design documents from `specs/inventory-specs/product-spec/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/product-api.md`, and `quickstart.md`

**Organization**: Tasks are grouped by user story so each increment can be implemented and validated independently. Tests are included because the plan, research, and quickstart explicitly require contract, API, and PostgreSQL integration coverage.

## Path Conventions

- Layered backend source paths are rooted at `domain/`, `models/`, `repository/`, `services/`, `schemas/`, and `api/`.
- Database changes belong in `alembic/versions/<new_product_management_revision>.py`.
- Feature tests belong in `tests/contract/`, `tests/integration/`, and the PostgreSQL-specific integration test named in the plan.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the implementation and validation baseline without adding dependencies or changing the existing authentication mechanism.

- [x] T001 Confirm the existing Product, Category, StatusEnum, authentication, database-session, and test-fixture conventions in `domain/`, `models/`, `services/`, `repository/`, `api/`, and `tests/conftest.py`
- [x] T002 [P] Define the product-management test markers and PostgreSQL test-database configuration in `pytest.ini`
- [ ] T003 [P] Document the product migration and validation commands from `specs/inventory-specs/product-spec/quickstart.md` in `docs/code/inventory/product-management.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared invariants and persistence guarantees required by every product user story.

**CRITICAL**: No user-story implementation should begin until this phase is complete.

- [x] T004 [P] Add typed product-domain exceptions for validation, not-found, duplicate-name, invalid-category, invalid-transition, and deletion-rejected cases in `domain/exceptions/__init__.py`
- [x] T005 [P] Implement canonical product-name normalization and validation helpers in `domain/inventory/product.py` for trimming, collapsing whitespace, rejecting blank names, and uppercasing
- [x] T006 [P] Implement typed Decimal monetary validation and non-negative quantity/status invariants in `domain/inventory/product.py`
- [x] T007 Update the Product aggregate's typed restore, field-change, status-transition, and capability methods in `domain/inventory/product.py` without implementing stock movement or sale execution
- [x] T008 Update the SQLAlchemy product mapping and constraints in `models/inventory_models/product_model.py` for canonical-name uniqueness, required fields, non-negative prices and quantity, explicit defaults, foreign key integrity, and valid statuses
- [x] T009 Create the Alembic migration in `alembic/versions/<new_product_management_revision>.py` for the Product schema constraints and canonical-name persistence, including upgrade and downgrade paths
- [x] T010 Refactor shared category-to-domain conversion and active-category validation at the existing Category boundary in `services/inventory/category_service.py`, preserving existing Category behavior
- [x] T011 Define typed Product response, create, query-filter, update, and status request schemas in `schemas/product_schema.py` with Decimal precision and enum validation
- [x] T012 Centralize authenticated-user and admin dependency usage in `api/dependencies.py`; keep product-domain error-to-HTTP mapping explicit in `api/routes/inventory_routes/product_routes.py`

**Checkpoint**: Shared domain, schema, persistence, transaction, and API-boundary primitives are ready; user stories can now be implemented independently.

---

## Phase 3: User Story 1 - Create Product (Priority: P1) 🎯 MVP

**Goal**: Allow any authenticated user to create a product linked to an existing active category, with canonical data, ACTIVE status, and zero available quantity.

**Independent Test**: Authenticate a registered user, create a product using valid data and a whitespace/case-variant name, then verify the `201` response, canonical uppercase name, ACTIVE status, quantity zero, and persisted category/prices. Also verify invalid and duplicate creations do not persist records.

### Tests for User Story 1

- [x] T013 [P] [US1] Add contract tests for `POST /product` request/response, authentication, status `201`, canonical name, ACTIVE status, and quantity zero in `tests/contract/test_product_management.py`
- [x] T014 [P] [US1] Add integration tests for valid creation, missing category, inactive category, invalid required fields, negative prices, excessive Decimal scale, and duplicate canonical names in `tests/integration/test_product_create.py`

### Implementation for User Story 1

- [x] T015 [US1] Implement typed Product persistence construction and single-transaction create/rollback behavior in `repository/inventory/product_repository.py`
- [x] T016 [US1] Implement authenticated create validation for active category, canonical name, prices, initial quantity, and duplicate integrity errors in `services/inventory/product_service.py`
- [x] T017 [US1] Implement `POST /product` at `api/routes/inventory_routes/product_routes.py` with bearer authentication, `201` response, and stable `400`, `404`, `409`, and `401` error mapping
- [x] T018 [US1] Return the created Product representation with category, Decimal prices, status, and available quantity through `schemas/product_schema.py` and `api/routes/inventory_routes/product_routes.py`

**Checkpoint**: Authenticated product creation is independently functional and safe against invalid categories, invalid money, duplicate names, and partial persistence.

---

## Phase 4: User Story 2 - Query Products (Priority: P1)

**Goal**: Allow authenticated users to list and retrieve products with case-insensitive name lookup and combined category/status filters.

**Independent Test**: Create products across categories and all three statuses, then verify list, detail, case-insensitive name, category, status, combined filters, empty result `[]`, and unknown-ID `404` behavior.

### Tests for User Story 2

- [x] T019 [P] [US2] Add contract tests for `GET /product` and `GET /product/{product_id}` representations, filters, empty arrays, authentication, and not-found responses in `tests/contract/test_product_management.py`
- [x] T020 [P] [US2] Add integration tests for list/detail queries, case-insensitive canonical-name lookup, category/status filters, combined filters, empty catalog, and unknown identifiers in `tests/integration/test_product_query.py`

### Implementation for User Story 2

- [x] T021 [US2] Implement typed repository queries for list, identifier, canonical name, category, status, and combined filters with category loading in `repository/inventory/product_repository.py`
- [x] T022 [US2] Implement Product-to-response/domain mapping without N+1 category lookups in `services/inventory/product_service.py`
- [x] T023 [US2] Implement authenticated `GET /product` and `GET /product/{product_id}` handlers with optional filters and stable empty/not-found behavior in `api/routes/inventory_routes/product_routes.py`
- [ ] T024 [US2] Align response attribute serialization for identifiers, nested category, Decimal prices, quantity, and all status values in `schemas/product_schema.py`

**Checkpoint**: Authenticated catalog visibility is independently functional, including all required filters and status distinctions.

---

## Phase 5: User Story 5 - Preserve Product and Consistency (Priority: P1)

**Goal**: Preserve product rows and identifiers throughout lifecycle operations, reject physical deletion, and guarantee atomic failure without partial updates.

**Independent Test**: Attempt deletion and deliberately fail validation or persistence during an update; verify rejection, unchanged row and identifier, and continued queryability.

### Tests for User Story 5

- [ ] T025 [P] [US5] Add contract tests for deletion absence/rejection and stable atomic-update error responses in `tests/contract/test_product_management.py`
- [ ] T026 [P] [US5] Add integration tests for deletion protection, identifier preservation, failed-update rollback, and nonexistent-update no-create behavior in `tests/integration/test_product_update.py`

### Implementation for User Story 5

- [ ] T027 [US5] Reject product deletion explicitly and preserve rows/identifiers in `repository/inventory/product_repository.py` and `services/inventory/product_service.py`
- [ ] T028 [US5] Implement full prospective-state validation and one-commit rollback semantics shared by product mutations in `services/inventory/product_service.py` and `repository/inventory/product_repository.py`
- [ ] T029 [US5] Ensure generic or legacy product deletion paths are absent or mapped to the stable deletion-rejected response in `api/routes/inventory_routes/product_routes.py`

**Checkpoint**: Product lifecycle preservation and atomicity guarantees are independently verified.

---

## Phase 6: User Story 3 - Edit Product Data (Priority: P2)

**Goal**: Allow only admin users to update name, category, cost price, and sale value atomically while preserving omitted fields and rejecting invalid prospective states.

**Independent Test**: As an admin, update each field alone and in combination, then query the product. As a non-admin or with invalid/duplicate/inactive-category data, verify the documented error and no changed field.

### Tests for User Story 3

- [ ] T030 [P] [US3] Add contract tests for `PATCH /product/{product_id}` partial payloads, admin authorization, updated representation, and error status categories in `tests/contract/test_product_management.py`
- [ ] T031 [P] [US3] Add integration tests for single/multi-field updates, omitted fields, non-admin denial, invalid prices, excessive precision, duplicate names, invalid categories, and atomic rollback in `tests/integration/test_product_update.py`

### Implementation for User Story 3

- [x] T032 [US3] Implement typed repository lookup and atomic partial-update persistence for Product records in `repository/inventory/product_repository.py`
- [ ] T033 [US3] Implement admin-only product-data update service logic with complete prospective-state validation and active-category checks in `services/inventory/product_service.py`
- [ ] T034 [US3] Implement `PATCH /product/{product_id}` with optional update fields, at-least-one-field validation, bearer/admin authorization, and stable errors in `api/routes/inventory_routes/product_routes.py`
- [ ] T035 [US3] Enforce canonicalization and Decimal serialization for updated Product values in `schemas/product_schema.py` and `domain/inventory/product.py`

**Checkpoint**: Admin product-data maintenance is independently functional and cannot partially persist invalid changes.

---

## Phase 7: User Story 4 - Change Product Status (Priority: P2)

**Goal**: Allow only admins to move products among ACTIVE, INACTIVE, and DISCONTINUED according to domain rules while preserving the product record.

**Independent Test**: As an admin, transition an ACTIVE product to INACTIVE and DISCONTINUED, reactivate with an active category, and verify persisted status, unchanged identifier, and status-specific capabilities. Verify invalid transitions, inactive-category reactivation, missing products, and non-admin requests fail.

### Tests for User Story 4

- [ ] T036 [P] [US4] Add contract tests for `PATCH /product/{product_id}/status`, all status values, authorization, preserved representation, and error categories in `tests/contract/test_product_management.py`
- [ ] T037 [P] [US4] Add integration tests for allowed transitions, reactivation category rules, invalid statuses/transitions, missing products, record preservation, and explicit stock-entry/sale capability predicates for ACTIVE, INACTIVE, and DISCONTINUED in `tests/integration/test_product_status.py`

### Implementation for User Story 4

- [ ] T038 [US4] Implement typed repository status lookup/update with one-transaction commit and rollback in `repository/inventory/product_repository.py`
- [ ] T039 [US4] Implement admin-only status transition validation, active-category reactivation checks, and stock/sale capability predicates in `services/inventory/product_service.py` and `domain/inventory/product.py`
- [ ] T040 [US4] Implement `PATCH /product/{product_id}/status` with enum validation, authentication/admin enforcement, stable errors, and preserved Product response in `api/routes/inventory_routes/product_routes.py`

**Checkpoint**: Admin lifecycle status management is independently functional, preserves records, and does not implement out-of-scope stock or sale workflows.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Verify all layers, PostgreSQL-specific invariants, documentation, and regression behavior.

- [ ] T041 [P] Add PostgreSQL-backed constraint and transaction tests for foreign keys, canonical uniqueness, Decimal precision, non-negative values, status constraints, defaults, duplicate races, rollback, and preservation of the distinction between product-level `available_quantity` and stock-specific quantities in `tests/integration/test_product_constraints_postgres.py`
- [ ] T042 [P] Review all new and modified Product functions, methods, route handlers, repositories, and schemas for complete parameter and return type annotations in `domain/inventory/product.py`, `models/inventory_models/product_model.py`, `repository/inventory/product_repository.py`, `services/inventory/product_service.py`, `schemas/product_schema.py`, and `api/routes/inventory_routes/product_routes.py`
- [ ] T043 Run migration and selected contract/integration validation from `specs/inventory-specs/product-spec/quickstart.md`, including `.venv/bin/python -m pytest tests/ -m "contract or integration"`
- [ ] T044 Run PostgreSQL-specific validation from `specs/inventory-specs/product-spec/quickstart.md` with `.venv/bin/python -m pytest tests/ -m postgres`
- [ ] T045 Run the complete regression suite with `.venv/bin/python -m pytest` and confirm existing Category/authentication behavior remains intact
- [ ] T046 Update the feature's implementation and acceptance evidence record in `specs/inventory-specs/product-spec/quickstart.md` with observed response statuses and database read-back results

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No implementation dependencies; T001 must precede convention-sensitive tasks, while T002-T003 can run in parallel.
- **Foundational (Phase 2)**: Depends on Phase 1; T004-T012 establish shared domain, schema, persistence, migration, and authorization foundations and block all stories.
- **P1 stories (Phases 3-5)**: Depend on Phase 2. US1 enables creation fixtures used by query and preservation tests; US2 and US5 are otherwise independently implementable after the foundation.
- **P2 stories (Phases 6-7)**: Depend on Phase 2 and the preservation/atomicity guarantees in US5; they may be developed in parallel after T028 is complete.
- **Polish (Phase 8)**: Depends on all desired stories and the migration being complete.

### User Story Dependencies

- **US1 (P1)**: Depends on Phase 2; MVP starting point. No dependency on another story.
- **US2 (P1)**: Depends on Phase 2 and product records/fixtures from US1 for realistic query coverage.
- **US5 (P1)**: Depends on Phase 2; its atomic mutation behavior is a prerequisite for safe US3 and US4 updates.
- **US3 (P2)**: Depends on Phase 2 and US5 atomicity/deletion guarantees; does not depend on US4.
- **US4 (P2)**: Depends on Phase 2 and US5 preservation/transaction guarantees; does not depend on US3.

### Parallel Opportunities

- T002-T003 can run in parallel during setup.
- T004-T006, T008-T009, and T011-T012 can run in parallel when they touch different files; T007 follows the domain helpers and T010 follows existing Category inspection.
- Within each story, contract and integration test tasks are parallelizable; repository, service, schema, and route tasks are parallel only when their files and dependencies do not overlap.
- After Phase 2, separate developers can work on US1, US2, and US5 in parallel, then US3 and US4 in parallel after shared atomicity behavior is agreed and validated.
- T041-T042 can run in parallel with documentation work; T043-T045 must run sequentially as validation gates.

## Parallel Example: User Story 1

```text
Task T013: Contract tests in tests/contract/test_product_management.py
Task T014: Create integration tests in tests/integration/test_product_create.py
Task T015: Repository create/rollback in repository/inventory/product_repository.py
Task T016: Create service in services/inventory/product_service.py
```

## Parallel Example: User Story 2

```text
Task T019: Query contract tests in tests/contract/test_product_management.py
Task T020: Query integration tests in tests/integration/test_product_query.py
Task T021: Query repository methods in repository/inventory/product_repository.py
Task T024: Response serialization in schemas/product_schema.py
```

## Parallel Example: User Story 3 and User Story 4

```text
Developer A: T030-T035 for admin product-data updates
Developer B: T036-T040 for admin status transitions
Shared prerequisite: T028 atomic prospective-state validation and rollback
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup.
2. Complete Phase 2 foundational domain, schema, migration, and API-boundary work.
3. Complete Phase 3 US1 creation tasks.
4. Run T013-T018 validation and stop at the checkpoint.
5. Demonstrate authenticated creation before expanding the catalog surface.

### Incremental Delivery

1. Add US2 query capability and validate list/detail/filter behavior.
2. Add US5 preservation and atomicity guarantees.
3. Add US3 admin data editing and validate rollback/authorization.
4. Add US4 admin status lifecycle and validate capability semantics.
5. Run PostgreSQL and full regression checks before final acceptance.

### Scope Guardrails

- Do not add new libraries or change the authentication mechanism.
- Do not implement stock entry, exit, transfer, allocation, purchase, sale execution, or sale-item behavior.
- Apply all schema changes through Alembic and validate PostgreSQL-specific invariants against PostgreSQL, not SQLite alone.
- Follow the project constitution's ABDC rule: each implementation block remains subject to explicit review and approval before code changes are applied.

## Notes

- `[P]` means the task can run in parallel without depending on incomplete work in another task.
- Story labels map tasks to US1-US5 in `spec.md`.
- Every story has an independent test criterion and a checkpoint.
- No git commands are required for this task artifact.
