from app.shared.exceptions.base import NotFoundError, ValidationAppError


class ResourceNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="RESOURCE_NOT_FOUND", message="Resource not found")


class InvalidResourceConfigurationError(ValidationAppError):
    def __init__(self, message: str) -> None:
        super().__init__(code="INVALID_RESOURCE_CONFIGURATION", message=message)
