from app.shared.exceptions.base import ConflictError, NotFoundError


class TrophyNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="TROPHY_NOT_FOUND", message="Trophy not found")


class DuplicateTrophyCodeError(ConflictError):
    def __init__(self) -> None:
        super().__init__(code="DUPLICATE_TROPHY_CODE", message="Trophy code already exists")
