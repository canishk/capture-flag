from app.shared.exceptions.base import ConflictError, NotFoundError, ValidationAppError


class LevelNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="LEVEL_NOT_FOUND", message="Level not found")


class InvalidLevelPrerequisiteError(ValidationAppError):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid level prerequisite configuration",
            details={"unlockConfig": ["Prerequisite level is invalid"]},
        )


class DuplicateLevelOrderError(ConflictError):
    def __init__(self) -> None:
        super().__init__(
            code="DUPLICATE_LEVEL_ORDER",
            message="Display order must be unique within the category",
        )
