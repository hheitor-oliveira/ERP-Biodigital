# Tasks: Gerenciamento de Categorias

**Input**: Design documents from `/specs/inventory/category/management-category/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Automated tests are in scope for this feature and are traced to the user stories below.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the shared test scaffolding and category foundations used by all stories

- [X] T001 [P] Create automated test structure for the category feature in `tests/contract/`, `tests/integration/`, and `tests/unit/`
- [X] T002 [P] Add shared pytest configuration and category fixtures in `tests/conftest.py` and `pytest.ini`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core category behaviors that every user story depends on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Implement category lifecycle helpers and normalized-name handling in `domain/inventory/category.py`
- [X] T004 [P] Add category persistence constraints and status defaults in `models/inventory_models/category_model.py`
- [X] T005 Implement repository primitives for create, find-by-id, find-by-normalized-name, update-name, and update-status in `repository/inventory/category_repository.py`
- [X] T006 [P] Expand category request/response schemas for create, list, rename, and status change in `schemas/category_schema.py`
- [X] T007 Add shared category validation and business-rule helpers in `services/inventory/category_service.py`

**Checkpoint**: Shared category foundations are ready; user story implementation can now begin

---

## Phase 3: User Story 1 - Cadastrar categoria de produto (Priority: P1) 🎯 MVP

**Goal**: Allow users to create new product categories with a valid, unique name and active status.

**Independent Test**: A valid category can be created, returned as active, and duplicate names are rejected.

### Tests for User Story 1

- [X] T008 [P] [US1] Create automated contract tests for category creation covering valid create, blank/whitespace rejection, duplicate-name rejection, and name-length validation in `tests/contract/test_category_management.py`
- [X] T009 [P] [US1] Create automated integration tests for the category-create endpoint and active-status response in `tests/integration/test_category_create.py`

### Implementation for User Story 1

- [X] T010 [US1] Implement category creation workflow and duplicate-name rejection in `services/inventory/category_service.py`
- [ ] T011 [US1] Wire the create-category endpoint and return payload in `api/routes/inventory_routes/category_routes.py`

**Checkpoint**: Category creation should work independently and reject invalid duplicates

---

## Phase 4: User Story 2 - Consultar categorias cadastradas (Priority: P2)

**Goal**: Allow users to list all categories and see their current status.

**Independent Test**: Existing categories are returned in a list, including active and inactive records, and empty results are handled clearly.

### Tests for User Story 2

- [ ] T012 [P] [US2] Create automated integration tests for category listing covering active, inactive, and empty-list cases in `tests/integration/test_category_list.py`

### Implementation for User Story 2

- [ ] T013 [US2] Implement category listing behavior that returns active and inactive categories in `services/inventory/category_service.py`
- [ ] T014 [US2] Wire the list endpoint response mapping in `api/routes/inventory_routes/category_routes.py` and `schemas/category_schema.py`

**Checkpoint**: Category listing should work independently of create/update flows

---

## Phase 5: User Story 3 - Editar e inativar categoria (Priority: P3)

**Goal**: Allow users to rename categories and switch them between active and inactive without breaking historical product links.

**Independent Test**: An existing category can be renamed or inactivated, even when products are associated, and the association remains intact.

### Tests for User Story 3

- [ ] T015 [P] [US3] Create automated integration tests for renaming categories and rejecting duplicate names in `tests/integration/test_category_update.py`
- [ ] T016 [P] [US3] Create automated integration tests for inactivating categories with linked products while preserving associations in `tests/integration/test_category_status.py`

### Implementation for User Story 3

- [ ] T017 [US3] Implement rename and active/inactive transition rules without blocking linked products in `services/inventory/category_service.py`
- [ ] T018 [US3] Wire update and status-change endpoints in `api/routes/inventory_routes/category_routes.py`

**Checkpoint**: Category maintenance actions should work without removing historical references

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and consistency checks across the whole feature

- [ ] T019 [P] Validate create, list, rename, and inactivate scenarios end to end using `specs/inventory/category/management-category/quickstart.md`
- [ ] T020 [P] Review and align feature documentation in `specs/inventory/category/management-category/spec.md`, `data-model.md`, and `contracts/category-api.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational phase completion
  - User stories can then proceed in priority order or in parallel where files do not overlap
- **Polish (Final Phase)**: Depends on the selected user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational phase; no dependency on other stories
- **User Story 2 (P2)**: Can start after Foundational phase; should remain independently testable
- **User Story 3 (P3)**: Can start after Foundational phase; should remain independently testable and preserve linked products

### Within Each User Story

- Shared foundations before story-specific implementation
- Test tasks for the story before implementation tasks for the same story
- Service behavior before route wiring
- Core behavior before final validation
- Story complete before moving to the next priority

### Parallel Opportunities

- T001 and T002 can run in parallel because they touch different files
- T004, T006, and T005 can run in parallel once the shared design is understood
- T008 and T009 can run in parallel for US1 test coverage
- T015 and T016 can run in parallel for US3 test coverage
- After Phase 2, US1, US2, and US3 can be worked on independently by different people if file ownership is coordinated
- T019 and T020 can run in parallel during the final validation/documentation pass

---

## Parallel Example: User Story 1

```bash
# If staffing allows, split the first story after foundations are done:
Task: "Create automated contract tests for category creation covering valid create, blank/whitespace rejection, duplicate-name rejection, and name-length validation in `tests/contract/test_category_management.py`"
Task: "Create automated integration tests for the category-create endpoint and active-status response in `tests/integration/test_category_create.py`"
Task: "Implement category creation workflow and duplicate-name rejection in `services/inventory/category_service.py`"
Task: "Wire the create-category endpoint and return payload in `api/routes/inventory_routes/category_routes.py`"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate the create flow using the quickstart guide and the US1 automated tests
5. Stop and demo if the basic category creation flow is correct

### Incremental Delivery

1. Deliver shared foundations
2. Add User Story 1 to create categories and verify it with automated tests
3. Add User Story 2 to list categories and verify it with automated tests
4. Add User Story 3 to rename and inactivate categories while preserving history and verify it with automated tests
5. Finish with validation and documentation alignment

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once foundations are done:
   - Developer A: User Story 1 tests and implementation
   - Developer B: User Story 2 tests and implementation
   - Developer C: User Story 3 tests and implementation
3. Final validation and documentation are handled after all stories are complete

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to a specific user story for traceability
- Each user story is independently valuable and testable
- Preserve historical product links when inactivating categories
- Avoid physical deletion as the standard lifecycle path
- Automated tests are in scope and should trace back to user stories and acceptance criteria
