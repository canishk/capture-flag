from typing import Any


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code=code, message=message, status_code=404)


class ConflictError(AppError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code=code, message=message, status_code=409)


class UnauthorizedError(AppError):
    def __init__(self, code: str = "UNAUTHORIZED", message: str = "Unauthorized") -> None:
        super().__init__(code=code, message=message, status_code=401)


class ForbiddenError(AppError):
    def __init__(self, code: str = "FORBIDDEN", message: str = "Forbidden") -> None:
        super().__init__(code=code, message=message, status_code=403)


class ValidationAppError(AppError):
    def __init__(self, message: str, details: dict[str, Any]) -> None:
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=422,
            details=details,
        )
