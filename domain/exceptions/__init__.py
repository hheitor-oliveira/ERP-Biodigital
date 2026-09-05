
class ProductDomainError(Exception):
    """Base exception for product-domain violations."""


class ProductValidationError(ProductDomainError):
    """Raised when product data is invalid."""


class ProductNotFoundError(ProductDomainError):
    """Raised when a product cannot be found."""


class DuplicateProductNameError(ProductDomainError):
    """Raised when a product name already exists."""


class InvalidProductCategoryError(ProductDomainError):
    """Raised when a product category is invalid or inactive."""


class InvalidProductStatusTransitionError(ProductDomainError):
    """Raised when a product status transition is not allowed."""


class ProductDeletionRejectedError(ProductDomainError):
    """Raised when product deletion is requested."""
