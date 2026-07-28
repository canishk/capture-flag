from app.shared.exceptions.base import ConflictError, NotFoundError


class AchievementNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="ACHIEVEMENT_NOT_FOUND", message="Achievement not found")


class DuplicateAchievementCodeError(ConflictError):
    def __init__(self) -> None:
        super().__init__(code="DUPLICATE_ACHIEVEMENT_CODE", message="Achievement code already exists")
