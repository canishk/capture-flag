from enum import StrEnum


class SubmissionStatus(StrEnum):
    PENDING = "pending"
    EVALUATING = "evaluating"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
