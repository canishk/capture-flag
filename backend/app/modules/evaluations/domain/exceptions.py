from dataclasses import dataclass

from app.shared.exceptions.base import NotFoundError, ValidationAppError


class EvaluationNotFoundError(NotFoundError):
    def __init__(self) -> None:
        super().__init__(code="EVALUATION_NOT_FOUND", message="Evaluation not found")


class UnsupportedEvaluationStrategyError(ValidationAppError):
    def __init__(self, strategy: str) -> None:
        super().__init__(
            code="UNSUPPORTED_EVALUATION_STRATEGY",
            message=f"Unsupported evaluation strategy: {strategy}",
        )


class EvaluationConfigurationError(ValidationAppError):
    def __init__(self, message: str) -> None:
        super().__init__(code="EVALUATION_CONFIGURATION_ERROR", message=message)


@dataclass(frozen=True)
class StrategyResult:
    passed: bool
    score: int
    feedback: str
    metadata: dict | None = None
