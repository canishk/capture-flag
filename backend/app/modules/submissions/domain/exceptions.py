from app.shared.exceptions.base import ForbiddenError, NotFoundError, ValidationAppError


class SubmissionNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="SUBMISSION_NOT_FOUND", message="Submission not found")


class SubmissionAccessDeniedError(ForbiddenError):
    def __init__(self) -> None:
        super().__init__(code="SUBMISSION_ACCESS_DENIED", message="Access denied to submission")


class InvalidSubmissionError(ValidationAppError):
    def __init__(self, message: str) -> None:
        super().__init__(code="INVALID_SUBMISSION", message=message)
