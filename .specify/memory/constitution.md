# ERP-Biodigital Constitution

## Core Principles

### [1 - Simplicity - KISS]

[Keep It Simple, Stupid.]

Prefer the simplest solution that correctly solves the problem.

* Avoid premature complexity.
* Avoid unnecessary abstractions.
* Prefer code that is easy to understand over "clever" code.

### [2 - YAGNI]

[You Aren't Gonna Need It.]

Never implement functionality outside the scope of the current task. The goal is to implement what is necessary now, not hypothetical future solutions.

If ideas arise during implementation, they may be documented in `docs/ideas.md`.

### [3 - Orthogonality]

[Independent Components.]

Components should depend only on the abstractions or layers necessary for their responsibilities. Dependencies between components must be explicit and justifiable.

### [4 - ABDC]

[Ask Before, Don't Change.]

All code changes must go through my review.

For every implementation, follow this workflow:

**Propose → Review → Approval → Implement.**

No implementation should proceed without explicit approval.

For code implementation tasks, show me the code you intend to implement. If the task involves running tests, show me only the tests you intend to run; you don't need to show me the code.

### [5 - High Cohesion / Low Coupling]

[High Cohesion, Low Coupling.]

Components should:

* Concentrate related responsibilities.
* Minimize dependencies on external implementation details.

### [6 - Fail Fast]

[Fail Early, Fail Clearly.]

Invalid states and inputs must be detected and reported as early as reasonably possible.

### [7 - Type Safety]

[Explicit and Consistent Typing.]

All functions and methods must explicitly declare:

- Parameter types.
- Return types.

Type hints must accurately represent the expected values and must not be omitted without technical justification.

### [8 - Exception Handling]

[Fail Clearly, Handle at the Appropriate Layer.]

Exceptions must be handled at the layer responsible for their interpretation or resolution.

- Do not use broad exception handling without a justified reason.
- Do not silently suppress exceptions.
- Domain and business-rule violations must be represented explicitly through appropriate exceptions.
- Lower-level exceptions must not be unnecessarily exposed to higher layers.
- Exceptions that need to be translated into another representation must be handled at the appropriate boundary.

## Stack Rules

1. The project's database management system is PostgreSQL and must be used exclusively.
2. The programming language is Python and must be used exclusively.
3. Alembic is used for database schema versioning and must be used for all schema changes.
4. FastAPI is used for API implementation and must be used for the project's API layer.
5. SQLAlchemy is used for all database interactions.
6. New libraries may be suggested when there is a justified technical need, but must not be added without approval. Suggestions should be documented in `docs/ideas.md`.
7. Git commands must not be executed by the agent.

## Governance

This Constitution defines the fundamental engineering principles and technical constraints of the project. All specifications, plans, implementations, and reviews must comply with it.

Changes to this Constitution require explicit approval and must update its version and amendment date.

**Version**: 1.0.0 | **Ratified**: 2026-08-30 | **Last Amended**: 2026-08-30
