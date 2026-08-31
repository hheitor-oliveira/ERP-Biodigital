# Contract: Category Management API

## Purpose
Defines the backend contract for managing product categories in the inventory domain.

## Resources

### Category
Represents a product grouping with a business name and lifecycle status.

## Operations

### Create Category
- Method and route: `POST /category/create`
- Purpose: Register a new category.
- Input:
  - JSON body: `{ "name": "category name" }`
- Rules:
  - name is required
  - name must be unique by business meaning
  - name must respect the approved length range
- Expected outcome:
  - category is created with active status
  - returned name uses the canonical normalized form

### List Categories
- Method and route: `GET /category/list`
- Purpose: Retrieve all categories.
- Output:
  - category id
  - category name
  - category status
- Rules:
  - active and inactive categories are included
- Empty result: returns an empty list when no categories exist

### Update Category Name
- Method and route: `PUT /category/{category_id}/rename`
- Purpose: Change the business name of an existing category.
- Input:
  - category identifier
  - JSON body: `{ "name": "new category name" }`
- Rules:
  - new name must be valid
  - new name must not duplicate another category by business meaning
  - returned name uses the canonical normalized form

### Change Category Status
- Method and route: `PATCH /category/{category_id}/status`
- Purpose: Activate or inactivate an existing category.
- Input:
  - category identifier
  - JSON body: `{ "status": "ACTIVE" | "INACTIVE" }`
- Rules:
  - categories can transition between active and inactive
  - inactivation is allowed even when products remain associated
  - existing product links are preserved

## Error Conditions
- Empty or whitespace-only category names are rejected
- Duplicate category names are rejected
- Names outside the accepted length range are rejected
- Requests that target a missing category are rejected

## Response Expectations
- Successful requests should return category data in the form `{ "id": integer, "name": string, "status": "ACTIVE" | "INACTIVE" }`
- Successful requests should return category data that reflects the current state of the category
- Validation failures should clearly identify the rule that was violated
