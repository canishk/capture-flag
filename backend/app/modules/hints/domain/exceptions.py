from app.shared.exceptions.base import ConflictError, NotFoundError, ValidationAppError


class HintNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="HINT_NOT_FOUND", message="Hint not found")


class DuplicateHintOrderError(ConflictError):
    def __init__(self) -> None:
        super().__init__(
            code="DUPLICATE_HINT_ORDER",
            message="Display order already exists for this challenge",
        )


class InvalidHintConfigurationError(ValidationAppError):
    def __init__(self, message: str) -> None:
        super().__init__(code="INVALID_HINT_CONFIGURATION", message=message)
