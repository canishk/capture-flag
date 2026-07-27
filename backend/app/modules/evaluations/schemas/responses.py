from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.evaluations.domain.entities import Evaluation
from app.modules.evaluations.domain.exceptions import StrategyResult
from app.shared.schemas.response import ApiModel


class EvaluationResponse(ApiModel):
    id: UUID
    submission_id: UUID
    user_id: UUID
    challenge_id: UUID
    strategy_type: str
    passed: bool
    score: int
    feedback: str
    status: str
    processing_time_ms: int
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, evaluation: Evaluation) -> "EvaluationResponse":
        return cls(
            id=evaluation.id,
            submission_id=evaluation.submission_id,
            user_id=evaluation.user_id,
            challenge_id=evaluation.challenge_id,
            strategy_type=evaluation.strategy_type.value,
            passed=evaluation.passed,
            score=evaluation.score,
            feedback=evaluation.feedback,
            status=evaluation.status.value,
            processing_time_ms=evaluation.processing_time_ms,
            metadata=evaluation.metadata,
            created_at=evaluation.created_at,
            updated_at=evaluation.updated_at,
        )


class PreviewEvaluationResponse(ApiModel):
    passed: bool
    score: int
    feedback: str

    @classmethod
    def from_result(cls, result: StrategyResult) -> "PreviewEvaluationResponse":
        return cls(passed=result.passed, score=result.score, feedback=result.feedback)
