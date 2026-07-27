from app.shared.exceptions.base import NotFoundError


class UserNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="USER_NOT_FOUND", message="User not found")
