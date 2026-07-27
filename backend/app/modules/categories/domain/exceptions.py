from app.shared.exceptions.base import ConflictError, NotFoundError


class CategoryNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="CATEGORY_NOT_FOUND", message="Category not found")


class DuplicateCategoryNameError(ConflictError):
    def __init__(self) -> None:
        super().__init__(code="DUPLICATE_CATEGORY_NAME", message="Category name already exists")
