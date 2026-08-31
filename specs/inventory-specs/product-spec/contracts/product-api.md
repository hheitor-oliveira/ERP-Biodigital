# Product API Contract

All product endpoints require `Authorization: Bearer <access_token>` unless stated otherwise. JSON responses use the domain values `ACTIVE`, `INACTIVE`, and `DISCONTINUED`.

The route names below are the planned contract. The existing `api/routes/inventory_routes/product_routes.py` is the implementation location; compatibility aliases may be retained only if they do not create duplicate behavior.

## Product representation

```json
{
  "id": 1,
  "name": "EXAMPLE PRODUCT",
  "category": {
    "id": 2,
    "name": "CATEGORY NAME",
    "status": "ACTIVE"
  },
  "cost_price": "10.00",
  "sale_value": "15.00",
  "available_quantity": 0,
  "status": "ACTIVE"
}
```

Prices are serialized as Decimal-compatible JSON values according to the existing Pydantic configuration; the implementation must preserve two-decimal monetary precision.

## Create product

`POST /product`

Permission: authenticated user.

Request:

```json
{
  "name": "  Example   Product  ",
  "category_id": 2,
  "cost_price": "10.00",
  "sale_value": "15.00"
}
```

Success: `201 Created` with a Product representation. The response name is canonical uppercase, status is `ACTIVE`, and `available_quantity` is `0`.

Errors:

- `400` for invalid name, price, or inactive category.
- `404` when `category_id` does not exist.
- `409` when the canonical name already exists.
- `401` when no valid bearer token is supplied.

## List products

`GET /product?name=<text>&category_id=<id>&status=<status>`

Permission: authenticated user.

All query parameters are optional. `name` is case-insensitive and uses the same canonical comparison as writes. Category and status filters combine with one another. Success: `200 OK` with an array of Product representations. An empty catalog or no matching filters returns `200 OK` with `[]`.

## Get product

`GET /product/{product_id}`

Permission: authenticated user.

Success: `200 OK` with one Product representation. A missing identifier returns `404` and does not create a record.

## Update product data

`PATCH /product/{product_id}`

Permission: admin user only.

Request fields are optional, but at least one of `name`, `category_id`, `cost_price`, or `sale_value` must be supplied. Omitted fields remain unchanged; explicit invalid/null values are rejected. The complete proposed product state is validated before one atomic commit.

Success: `200 OK` with the updated Product representation.

Errors:

- `401` for absent/invalid authentication or authenticated non-admin user.
- `400` for invalid name, price, or update payload.
- `404` for missing product or category.
- `409` for a duplicate canonical name.

## Change product status

`PATCH /product/{product_id}/status`

Permission: admin user only.

Request:

```json
{"status": "INACTIVE"}
```

Success: `200 OK` with the preserved Product representation and new status. Reactivation validates that the product category is active.

Errors:

- `400` for an unrecognized or disallowed status transition.
- `401` for absent/invalid authentication or non-admin user.
- `404` for missing product.

## Delete behavior

No product deletion endpoint is exposed. If a generic deletion path reaches the product service/repository, it must reject the operation and preserve the row and identifier. This is a lifecycle invariant, not a soft-delete requirement.

## Error shape

Errors use the existing FastAPI convention:

```json
{"detail": "stable human-readable domain error"}
```

The exact messages should be centralized or consistently mapped during implementation; clients must rely on status codes and error categories rather than incidental database exception text.
