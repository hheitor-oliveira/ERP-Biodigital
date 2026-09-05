# Product Management Quickstart Validation

## Prerequisites

- Python 3.12 and the repository virtual environment.
- Dependencies installed from `requirements.txt`.
- PostgreSQL running and `DATABASE_URL` configured in `.env`.
- An existing active category and authenticated users, including one admin user.

## Prepare the database

From the repository root:

    source .venv/bin/activate
    alembic upgrade head

The implementation phase must add the Product migration before running this command against a fresh database. Schema details are in `data-model.md`.

## Run automated validation

Fast contract and API checks:

    .venv/bin/python -m pytest tests/ -m "contract or integration"

PostgreSQL-backed checks (the implementation phase must provide/configure the project marker or test database target):

    .venv/bin/python -m pytest tests/ -m postgres

Full regression suite:

    .venv/bin/python -m pytest

Expected result: all selected tests pass, with no unapproved SQLite-only substitute for PostgreSQL constraint coverage.

## Manual API scenarios

1. Log in through the existing authentication route and retain the bearer token.
2. Create an active category, then POST a product using a name with leading/trailing and repeated internal whitespace. Verify the response stores the canonical uppercase name, status `ACTIVE`, and quantity `0`.
3. Repeat creation using different casing/whitespace. Verify `409` and confirm only one product exists.
4. Query the list with case variants of `name`, with `category_id`, and with each status filter. Verify matching is case-insensitive and status/category filters return only matching products. Verify an empty result is `[]`.
5. Query an unknown product identifier. Verify `404` and that no new record exists.
6. Authenticate as a non-admin and attempt PATCH data/status. Verify `401`/authorization denial and no change.
7. Authenticate as admin and update one field, then multiple fields. Verify omitted fields remain unchanged.
8. Attempt an update with an invalid price, duplicate name, missing category, or inactive category. Verify the documented error and that every original field remains unchanged.
9. Change an ACTIVE product to `INACTIVE` and `DISCONTINUED`, then reactivate it with an active category. Verify the identifier and row are preserved and the three statuses remain distinguishable.
10. Attempt a deletion through any available generic path. Verify rejection and that the product remains queryable.

## Acceptance evidence

Record response status/payload and database read-back for creation, duplicate protection, filtering, authorization, atomic rollback, status preservation, and deletion protection. Use the API contract in `contracts/product-api.md` and invariants in `data-model.md` as the expected behavior.

## Observed acceptance evidence

The following evidence was observed during implementation validation against the project test stack and PostgreSQL-specific checks:

- Migration: `alembic upgrade head` completed successfully against PostgreSQL.
- Creation: valid authenticated product creation returned `201 Created`; the response and database read-back confirmed the canonical uppercase name, `ACTIVE` status, `available_quantity` equal to `0`, category association, and persisted Decimal prices.
- Duplicate protection: creating a second product with a case/whitespace variant of an existing canonical name returned `409 Conflict`; the database read-back confirmed that only the original product row remained.
- Queries: authenticated list and detail operations returned `200 OK`; canonical case-insensitive name filtering, category/status filters, combined filters, and empty-result behavior returned the expected representations; an unknown product identifier returned `404 Not Found` without creating a row.
- Authorization: unauthenticated requests returned `401 Unauthorized`; authenticated non-admin requests to admin-only product mutations returned `401 Unauthorized`.
- Product data updates: valid admin updates returned `200 OK` with the complete representation and preserved omitted fields. Missing product/category cases returned `404`, inactive-category replacement returned `400`, duplicate canonical names returned `409`, and an empty update payload returned `400` with the stable error message.
- Schema validation: missing fields, negative prices, excessive Decimal scale, invalid status values, and other Pydantic request-schema violations returned `422 Unprocessable Content` before route-handler execution.
- Atomicity: failed update attempts preserved the original product identifier and persisted fields on database read-back; repository transaction checks confirmed one commit on success and rollback with exception re-raising on SQLAlchemy failure.
- Status lifecycle: valid status transitions returned `200 OK`; invalid transitions and reactivation with an inactive category returned `400`; unknown products returned `404`; the product identifier and row remained preserved.
- Deletion protection: no product deletion endpoint was exposed; `DELETE /product/{product_id}` returned `405 Method Not Allowed`, and the product remained queryable.
- Automated validation: the affected test set returned `66 passed`; the complete regression suite returned `107 passed`. Both runs reported one existing Pydantic deprecation warning in `schemas/user_schema.py`.

The observed `422` responses apply to validation performed by FastAPI/Pydantic before route execution. Domain and business-rule errors continue to use the status categories documented in the API contract.
