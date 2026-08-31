# Quickstart: Category Management Validation

## Purpose
Validate the category management feature end to end using the backend API contract.

## Prerequisites
- Project dependencies installed
- PostgreSQL available and configured for the project
- Database migrations applied
- Backend server running

## Start the backend
1. Configure the project environment as usual for the repository.
2. Apply the database schema updates required by the project.
3. Start the backend service.

## Validation Scenarios

### 1) Create a valid category
- Send a request with a valid category name.
- Expected result:
  - the category is created successfully
  - the returned category is active
  - the category appears in later list operations

### 2) Reject duplicate names
- Create one category.
- Attempt to create another category using the same name, including variants that differ only by case or surrounding spaces.
- Expected result:
  - the second request is rejected
  - the error explains that the category already exists

### 3) List categories
- Request the category list after creating both active and inactive categories.
- Expected result:
  - all categories are returned
  - each entry includes its current status

### 4) Update a category name
- Choose an existing category and change its name to another valid non-duplicate name.
- Expected result:
  - the category name is updated
  - the updated name is returned in later queries

### 5) Inactivate a category with linked products
- Associate products with a category.
- Inactivate the category.
- Expected result:
  - the category becomes inactive
  - the product association remains intact
  - the category remains visible in historical or administrative queries

## Expected Success Conditions
- Valid categories can be created and retrieved
- Invalid names are rejected
- Duplicate names are rejected
- Category status changes preserve history and existing product links
- Listing returns both active and inactive categories

## References
- Contract: `contracts/category-api.md`
- Data model: `data-model.md`
