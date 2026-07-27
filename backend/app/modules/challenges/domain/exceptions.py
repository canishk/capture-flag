from app.shared.exceptions.base import ConflictError, NotFoundError, ValidationAppError


class ChallengeNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="CHALLENGE_NOT_FOUND", message="Challenge not found")


class DuplicateChallengeTitleError(ConflictError):
    def __init__(self) -> None:
        super().__init__(
            code="DUPLICATE_CHALLENGE_TITLE",
            message="Challenge title already exists in this level",
        )


class InvalidChallengeStatusTransitionError(ValidationAppError):
    def __init__(self, message: str = "Invalid challenge status transition") -> None:
        super().__init__(code="INVALID_CHALLENGE_STATUS_TRANSITION", message=message)


class InvalidChallengeConfigurationError(ValidationAppError):
    def __init__(self, message: str) -> None:
        super().__init__(code="INVALID_CHALLENGE_CONFIGURATION", message=message)
