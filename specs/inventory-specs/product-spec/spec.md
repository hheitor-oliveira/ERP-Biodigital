# Feature Specification: Product Management

**Feature Branch**: `management-product`

**Created**: 2026-08-30

**Status**: Draft

**Module**: Inventory

**Domain**: Product

**Directory**: `specs/inventory-specs/product-spec/management-product/`

**Input**: User description: "Create the feature for the Inventory module. Context: Module: Inventory; Domain: Product; Directory: `specs/inventory-specs/product-specs/`. Analyze `README.md`, `docs/project-status.md`, `docs/`, and the existing code to understand the current context. The feature must specify complete product management in the backend, including its behaviors, business rules, validations, and acceptance criteria. Consider all existing backend layers, but do not define technical implementation at this stage. This will be defined later in `/speckit-plan`. Do not implement code or modify the project. Create only `spec.md` in the specified directory."

## Context and Objective

The product is one of the central elements of the Inventory module. It must be registered, queried, and maintained consistently so that categories, future sales, and stock operations can use a single reliable source of product information.

This feature defines the expected behavior for product management in the backend, including registration, querying, editing, activation, inactivation, and discontinuation. The specification describes what the system must guarantee without defining endpoints, libraries, code structures, or other implementation decisions.

## User Scenarios & Testing

### User Story 1 - Create Product (Priority: P1)

As an inventory responsible user, I want to create a product with its category and commercial values so that it can be identified and used by other processes in the system.

**Permission**: Any registered/authenticated user (API layer)

**Why this priority**: Product creation is the foundation of the product catalog and is required for subsequent inventory or sales operations.

**Independent Test**: Provide all valid product data, confirm that the product is created, and verify its initial status and availability in subsequent queries.

**Acceptance Scenarios**:

1. **Given** that a valid and active category exists, **When** the user provides valid name, cost price, and sale price, **Then** the product must be created with `available_quantity` equal to zero and status `ACTIVE`.

2. **Given** that the specified category does not exist, **When** product creation is requested, **Then** the operation must be rejected and no product must be created.

3. **Given** that the specified category is inactive, **When** product creation is requested, **Then** the operation must be rejected because new products can only be associated with active categories.

4. **Given** that one or more required fields are missing or invalid, **When** product creation is requested, **Then** the operation must be rejected and the data requiring correction must be identified.

---

### User Story 2 - Query Products (Priority: P1)

As an inventory user, I want to list and query products using their current data so that I can locate items and verify their category, commercial situation, and available quantity.

The system must support querying by name without case sensitivity and filtering by category and status.

**Permission**: Any registered/authenticated user (API layer)

**Why this priority**: Querying provides visibility into the catalog and allows dependent processes to use current product data.

**Independent Test**: Create products with different statuses and categories and verify that queries return the corresponding identifying, commercial, category, quantity, and status information.

**Acceptance Scenarios**:

1. **Given** that products are registered, **When** the product list is requested, **Then** all registered products must be returned with name, category, prices, `available_quantity`, and status.

2. **Given** that active, inactive, and discontinued products exist, **When** the product list is requested, **Then** each product must be presented with its current status, without confusing inactive products with discontinued products.

3. **Given** that no products match the request, **When** the product list is requested, **Then** the system must return HTTP `200 OK` with an empty array (`[]`).

4. **Given** that a product identifier does not correspond to a registered product, **When** an individual query is requested, **Then** the system must indicate that the product was not found.

5. **Given** that products exist with different name casing, **When** a product is queried by name, **Then** the query must not distinguish between uppercase and lowercase characters.

6. **Given** that products exist in different categories or statuses, **When** a category or status filter is applied, **Then** only products matching the requested filter must be returned.

---

### User Story 3 - Edit Product Data (Priority: P2)

As a user responsible for inventory maintenance, I want to change a product's name, category, and prices so that the catalog remains correct without creating a new product record.

**Permission**: Admin users only (API layer)

**Why this priority**: Editing keeps product data reliable over time and avoids creating duplicate records to correct information.

**Independent Test**: Change each permitted field individually and in combination, then verify the updated values in a subsequent query and confirm that unchanged data remains unchanged.

**Acceptance Scenarios**:

1. **Given** that the product exists and the new data is valid, **When** the edit is requested, **Then** only the specified fields must be updated.

2. **Given** that the new category exists and is active, **When** the product category is changed, **Then** the product must reference the new category.

3. **Given** that the new category does not exist or is inactive, **When** the category change is requested, **Then** the operation must be rejected and the previous category preserved.

4. **Given** that a new price is negative, invalid, or exceeds the permitted monetary precision, **When** the edit is requested, **Then** the operation must be rejected without changing the product.

5. **Given** that the new name is empty or does not meet the defined limits, **When** the edit is requested, **Then** the operation must be rejected without changing the product.

6. **Given** that the new name is already used by another product, **When** the edit is requested, **Then** the operation must be rejected and the previous name preserved.

---

### User Story 4 - Change Product Status (Priority: P2)

As a user responsible for inventory, I want to activate, inactivate, or discontinue a product so that I can control its use without deleting its history.

**Special Rules**: Product statuses define which operations can be performed with the product. These rules must be protected.

* `ACTIVE` → Product can receive stock entries and can be sold.
* `INACTIVE` → Product cannot receive stock entries and cannot be sold.
* `DISCONTINUED` → Product cannot receive stock entries but can be sold.

**Note**: Keep the sale-related behavior intentionally incomplete at this stage because it depends on the `Sale` module.

**Permission**: Admin users only (API layer)

**Why this priority**: Product status must represent its lifecycle and prevent incompatible operations while preserving historical references.

**Independent Test**: Change each possible status and verify the persisted state and the operations allowed for that status.

**Acceptance Scenarios**:

1. **Given** that the product exists and is active, **When** its status is changed to inactive, **Then** it must remain queryable and its status must become `INACTIVE`, and it must not receive stock entries or be sold.

2. **Given** that the product exists and is active, **When** its status is changed to discontinued, **Then** it must remain queryable and its status must become `DISCONTINUED`, and it must not receive stock entries but may be sold.

3. **Given** that the product is inactive or discontinued, **When** it is reactivated, **Then** its status must become `ACTIVE`, subject to the category rules defined by the domain.

4. **Given** that the product does not exist, **When** a status change is requested, **Then** the operation must be rejected and no record must be changed.

---

### User Story 5 - Preserve Product and Consistency (Priority: P1)

As an inventory manager, I want product records to be preserved so that references used by other parts of the system remain valid throughout the product lifecycle.

**Why this priority**: Physically deleting a product could invalidate historical references and compromise ERP data integrity.

**Independent Test**: Attempt to remove products in different situations and verify that their records remain preserved.

**Acceptance Scenarios**:

1. **Given** that a product exists, **When** physical deletion is requested, **Then** the product must not be removed.

2. **Given** that a product has historical references, **When** its data or status is maintained, **Then** the references must continue pointing to the same product.

3. **Given** that an update fails because of a validation or business rule, **When** the error is returned, **Then** no partial product data must be persisted.

## Business Rules

* **RN-PROD-001**: Every product must have a name, category, cost price, sale price, and status.

* **RN-PROD-002**: `available_quantity` can never be negative.

* **RN-PROD-003**: A new product must start with `available_quantity` equal to zero.

* **RN-PROD-004**: `available_quantity` represents the quantity available for allocation to a `Stock`. It does not represent the quantity held in a specific stock.

* **RN-PROD-005**: Stock entry, exit, transfer, and allocation operations are not defined by this feature and belong to future stock-related features.

* **RN-PROD-006**: An `ACTIVE` product can receive stock entries and can be sold.

* **RN-PROD-007**: An `INACTIVE` product cannot receive stock entries and cannot be sold.

* **RN-PROD-008**: A `DISCONTINUED` product cannot receive stock entries but can be sold.

* **RN-PROD-009**: Product status must be one of the domain-recognized values: `ACTIVE`, `INACTIVE`, or `DISCONTINUED`.

* **RN-PROD-010**: Every product must reference an existing category.

* **RN-PROD-011**: New products and reactivation may require an active category according to the category lifecycle rules defined by the domain.

* **RN-PROD-012**: Two products cannot have the same name.

* **RN-PROD-013**: Product name comparison for uniqueness and name queries must be case-insensitive.

* **RN-PROD-014**: Product names must be stored in uppercase for standardization.

* **RN-PROD-015**: Product records must not be physically deleted as a product lifecycle operation.

* **RN-PROD-016**: Invalid updates must not modify the current product data.

* **RN-PROD-017**: Updating a nonexistent product must not create a new product.

## Validation Rules

### Name

* The name is required.
* The name cannot be empty.
* The name cannot consist only of whitespace.
* The name must be unique among products.
* Name uniqueness must be case-insensitive.
* Leading and trailing whitespace must not cause two otherwise equivalent names to be treated as different.
* The name must be stored in uppercase.

### Category

* The category is required during creation.
* The specified category must exist.
* Category status must be considered for operations that require an active category.

### Cost Price

* Must be a valid monetary value.
* Must not be negative.

### Sale Price

* Must be a valid monetary value.
* Must not be negative.

### Available Quantity

* Must be a valid non-negative quantity.
* A new product must start with `available_quantity` equal to zero.
* `available_quantity` must not become negative.
* `available_quantity` must not be interpreted as the quantity of a specific `Stock`.

### Status

The status must belong to the domain-recognized set:

* `ACTIVE`
* `INACTIVE`
* `DISCONTINUED`

## Query Rules

* Product name queries must be case-insensitive.
* Product queries must support filtering by category.
* Product queries must support filtering by status.
* Individual product queries must support identification by product identifier.
* Product lists must distinguish clearly between `ACTIVE`, `INACTIVE`, and `DISCONTINUED` products.

## Edge Cases

* A product creation request using a name that already exists must be rejected.
* Names differing only by case must not create duplicate products.
* Names differing only by leading or trailing whitespace must not create duplicate products.
* A category that does not exist must be rejected.
* An invalid update must not partially persist valid fields.
* An update for a nonexistent product must not create a new product.
* A product with `available_quantity` equal to zero remains valid.
* A negative `available_quantity` must always be rejected.
* Changing product status must not delete the product.
* `INACTIVE` and `DISCONTINUED` products must remain identifiable in product queries.
* `available_quantity` must not be treated as a stock-specific quantity.
* Stock entry, exit, transfer, and allocation rules must not be introduced into this feature.
* Sale-specific behavior must remain intentionally incomplete until the `Sale` module is specified.

## Functional Requirements

* **FR-001**: The system MUST allow authorized users to create products.
* **FR-002**: The system MUST require a name, category, cost price, and sale price when creating a product.
* **FR-003**: The system MUST reject product creation when the specified category does not exist or when its status is not `ACTIVE`.
* **FR-004**: The system MUST reject the creation of a product when another product already has the same name.
* **FR-005**: Product name uniqueness MUST be case-insensitive.
* **FR-006**: The system MUST store product names in uppercase.
* **FR-007**: The system MUST initialize a new product with `available_quantity` equal to zero.
* **FR-008**: The system MUST allow authenticated users to query the product list.
* **FR-009**: The system MUST allow authenticated users to query an individual product by identifier.
* **FR-010**: The system MUST support case-insensitive product name queries.
* **FR-011**: The system MUST support filtering products by category.
* **FR-012**: The system MUST support filtering products by status.
* **FR-013**: The system MUST return the product's relevant current data in queries, including identifier, name, category, prices, `available_quantity`, and status.
* **FR-014**: The system MUST allow admin users to update product data.
* **FR-015**: The system MUST allow updating the product name, category, cost price, and sale price.
* **FR-016**: The system MUST reject updates that would create a duplicate product name.
* **FR-017**: The system MUST reject updates that reference a nonexistent or otherwise invalid category.
* **FR-018**: The system MUST reject negative monetary values.
* **FR-019**: The system MUST allow admin users to change product status among `ACTIVE`, `INACTIVE`, and `DISCONTINUED`.
* **FR-020**: The system MUST preserve the product record when its status changes.
* **FR-021**: The system MUST prevent physical deletion of products through product lifecycle management.
* **FR-022**: The system MUST reject operations targeting nonexistent product identifiers.
* **FR-023**: The system MUST prevent invalid operations from producing partial updates.
* **FR-024**: The system MUST enforce the status-specific stock-entry rules defined by the product domain.
* **FR-025**: The system MUST preserve the distinction between product-level `available_quantity` and stock-specific quantities.
* **FR-026**: This feature MUST NOT define stock entry, exit, transfer, or allocation operations.
* **FR-027**: This feature MUST NOT fully define sale behavior; sale-specific enforcement will be completed by the `Sale` feature.

## Key Entities

### Product

Represents a product registered in the Inventory catalog.

Its relevant attributes include:

* identifier;
* name;
* category;
* cost price;
* sale price;
* `available_quantity`;
* status.

### Category

Represents the category associated with a product.

* A product must reference an existing category. Product creation and reactivation require the category status to be `ACTIVE`.

### Stock

Represents a stock to which product quantities may be allocated in future inventory features.

The detailed management of `Stock` does not belong to this feature.

## Success Criteria

* **SC-001**: 100% of valid product creations must initialize `available_quantity` to zero.
* **SC-002**: 100% of attempts to create a duplicate product name must be rejected.
* **SC-003**: 100% of product name queries must be case-insensitive.
* **SC-004**: 100% of invalid category references must be rejected.
* **SC-005**: 100% of products must maintain `available_quantity` greater than or equal to zero.
* **SC-006**: 100% of invalid updates must preserve the product's previous valid data.
* **SC-007**: 100% of updates targeting nonexistent products must be rejected without creating new records.
* **SC-008**: 100% of product status changes must preserve the product record.
* **SC-009**: 100% of physical deletion attempts must fail to remove the product record.
* **SC-010**: 100% of product queries using category or status filters must return only matching products.

## Assumptions

* The `Category` domain already exists and can be referenced by `Product`.
* Authentication and authorization mechanisms already exist and will be reused.
* Any registered/authenticated user may create and query products at the API layer, while product data editing and status changes require admin privileges.
* `available_quantity` represents the quantity available for future allocation to a `Stock`.
* The quantity assigned to a specific stock will be defined by the future `Stock` feature.
* Stock entry, exit, transfer, and allocation operations are outside the scope of `management-product`.
* Sale operations are outside the scope of this feature, except for the product status rules that establish whether a product may be sold.
* Product names are unique within the product catalog.
* Product names are stored in uppercase.
* Product name lookup and uniqueness comparison are case-insensitive.
* Products are not physically deleted as part of normal lifecycle management.
* The recognized product statuses are `ACTIVE`, `INACTIVE`, and `DISCONTINUED`.
* Monetary values are non-negative.
* Technical implementation details for API, schemas, services, domain, repositories, models, and database structures are defined in the later planning and contract artifacts, not by this requirements document.

## Out of Scope

This feature does not define:

* Stock creation or management;
* stock-specific quantities;
* stock entry operations;
* stock exit operations;
* stock transfers;
* product allocation to stocks;
* purchase operations;
* purchase replenishment lists;
* sale execution;
* sale item behavior;
* sale-specific implementation;
* API endpoint design as a requirements concern (the concrete API contract is maintained separately in `contracts/product-api.md`);
* database schema design as a requirements concern (the implementation design is maintained separately in `plan.md` and `data-model.md`);
* framework or library selection as a requirements concern (the implementation stack is maintained separately in `plan.md`);
* internal architecture of backend layers as a requirements concern (the implementation structure is maintained separately in `plan.md`).
