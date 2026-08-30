# Data Model: Gerenciamento de Categorias

## Entity: Category

### Purpose
Represents a product grouping used to classify inventory items consistently.

### Fields
- id: unique identifier for the category
- name: human-readable category name
- status: lifecycle state of the category

### Validation Rules
- name is required
- name must contain between 5 and 32 characters
- name must not be blank or whitespace-only
- name must be unique by business meaning
- name comparison must ignore case and surrounding whitespace when checking duplicates
- status must be one of the supported lifecycle states

### State Transitions
- active → inactive
- inactive → active
- physical deletion is not part of the standard lifecycle

### Relationships
- One Category can be associated with many Products
- Products keep their category association even if the category becomes inactive

### Behavioral Notes
- Inactive categories remain available for historical consultation and catalog consistency
- Category duplication is rejected before the category becomes part of the active catalog
- The category name is the primary business identifier used for user-facing management

## Entity: Product

### Purpose
Represents an inventory item that belongs to a category.

### Relationship to Category
- Each Product references one Category
- Category changes must not invalidate existing products
- When a category is inactive, products tied to it remain associated for reference and history

## Entity: CategoryStatus

### Purpose
Represents the lifecycle state of a category.

### Supported Values
- active
- inactive

### Behavioral Rules
- active categories may be selected for normal inventory classification
- inactive categories remain visible in queries and reports, but are treated as not active for new active use
