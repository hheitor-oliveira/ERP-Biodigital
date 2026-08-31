# Research: Gerenciamento de Categorias

## Decision 1: Existing project architecture is the source of truth
- Decision: The feature follows the current layered backend already present in the repository: API/routes, schemas, services, domain, repository, models, and database session management.
- Rationale: `README.md`, `docs/project-status.md`, and the implementation guide in `docs/code/IMPLEMENTACAO_ESTOQUE.md` all describe this architecture consistently, and the current code already uses it.
- Alternatives considered:
  - Collapsing layers for a smaller implementation was rejected because it would diverge from the documented architecture and existing code structure.
  - Introducing a new architectural style was rejected because the feature is intended to extend the current backend, not redesign it.

## Decision 2: Category names are unique by business meaning
- Decision: Category names must be treated as unique by business meaning, with normalization for case and surrounding whitespace.
- Rationale: The feature spec requires duplicate prevention, and the clarified requirements state that values differing only by case or spacing should be treated as duplicates.
- Alternatives considered:
  - Case-sensitive uniqueness was rejected because it would allow confusing duplicates such as `Periféricos` and `PERIFÉRICOS`.
  - Allowing similar names with suffixes was rejected because it weakens category consistency and discoverability.

## Decision 3: Category lifecycle is active/inactive only
- Decision: Category lifecycle is limited to active and inactive states; categories are not physically deleted as the default management behavior.
- Rationale: The spec explicitly requires preserving history, and the clarification confirms that inactivation is allowed even when products are linked.
- Alternatives considered:
  - Physical deletion was rejected because it would break historical traceability and conflict with the existing inventory model.
  - A richer state machine was rejected because there is no evidence in the current scope that more states are needed.

## Decision 4: Linked products remain associated after inactivation
- Decision: Inactivating a category does not remove or sever its association with existing products.
- Rationale: The clarified acceptance behavior requires historical/reference use to remain available after inactivation.
- Alternatives considered:
  - Blocking inactivation while products exist was rejected by clarification.
  - Reassigning all products before inactivation was rejected because it adds unnecessary operational burden and is not required by the feature scope.

## Decision 5: Validation rules should be conservative and user-facing
- Decision: Category name validation should reject empty values, whitespace-only values, and values outside the allowed length range defined in the spec.
- Rationale: This matches the feature requirements and the fail-fast principle in the project constitution.
- Alternatives considered:
  - Accepting arbitrary strings and sanitizing later was rejected because it delays errors and complicates duplicate detection.
  - Allowing very short or very long names was rejected because it weakens usability and consistency.

## Decision 6: The backend API is the public contract boundary for this feature
- Decision: The feature should expose its behavior through the backend HTTP API already used by the project.
- Rationale: The repository already includes FastAPI routes and schemas for category management, and the spec asks for backend behavior rather than a UI feature.
- Alternatives considered:
  - Treating the feature as repository-only was rejected because it would not satisfy backend management workflows.
  - Treating it as a database-only feature was rejected because the current project exposes behavior through API routes.

## Decision 7: Test strategy should validate behavior from the outside in
- Decision: Validation should focus on end-to-end category behavior: create, list, update, inactivate, duplicate rejection, and preserved history.
- Rationale: The feature is business-facing and its acceptance criteria are naturally expressed as observable outcomes.
- Alternatives considered:
  - Testing only domain objects was rejected because it would miss API and persistence behavior.
  - Testing only routes was rejected because it would miss business-rule enforcement in services/domain.

## Decision 8: Existing stack remains unchanged
- Decision: The implementation should stay within the current stack already declared by the project: Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic, Pydantic, and the current auth/session utilities.
- Rationale: The constitution explicitly constrains the stack and the repository already uses these dependencies.
- Alternatives considered:
  - Adding a new framework or data layer was rejected because it would violate project constraints and increase complexity.

## Decision 9: Automated test framework is not yet evidenced in the repository
- Decision: The planning artifacts should treat automated tests as a desired validation outcome, but not assume a currently standardized test runner beyond the project’s existing environment.
- Rationale: `requirements.txt` and the inspected code do not show a project-level test framework in use.
- Alternatives considered:
  - Assuming a specific test runner was rejected because the repository does not currently evidence one.

## Open confirmations resolved by research
- Category management is a backend feature for the inventory domain.
- Category name uniqueness should be case/whitespace normalized.
- Categories can be inactivated even with linked products.
- History must be preserved instead of physically deleting categories.
