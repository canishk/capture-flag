from app.shared.exceptions.base import NotFoundError


class ProgressNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="PROGRESS_NOT_FOUND", message="Progress not found")
