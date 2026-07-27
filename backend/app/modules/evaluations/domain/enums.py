from enum import StrEnum


class EvaluationStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    ERROR = "error"


class EvaluationStrategyType(StrEnum):
    EXACT_MATCH = "exact_match"
    REGEX = "regex"
    NUMERIC_RANGE = "numeric_range"
    COSINE_SIMILARITY = "cosine_similarity"
    AI_JUDGE = "ai_judge"
    EXTERNAL_VALIDATOR = "external_validator"
