from app.shared.exceptions.base import ConflictError, UnauthorizedError, ValidationAppError


class InvalidCredentialsError(UnauthorizedError):
    def __init__(self) -> None:
        super().__init__(code="INVALID_CREDENTIALS", message="Invalid email or password")


class EmailAlreadyRegisteredError(ConflictError):
    def __init__(self) -> None:
        super().__init__(
            code="EMAIL_ALREADY_REGISTERED",
            message="An account with this email already exists",
        )


class EmailNotVerifiedError(UnauthorizedError):
    def __init__(self) -> None:
        super().__init__(code="EMAIL_NOT_VERIFIED", message="Email address is not verified")


class InvalidTokenError(UnauthorizedError):
    def __init__(self, message: str = "Invalid or expired token") -> None:
        super().__init__(code="INVALID_TOKEN", message=message)


class WeakPasswordError(ValidationAppError):
    def __init__(self) -> None:
        super().__init__(
            message="Password does not meet requirements",
            details={"password": ["Password must be at least 8 characters"]},
        )
