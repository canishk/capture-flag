from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.evaluations.domain.enums import EvaluationStatus, EvaluationStrategyType


@dataclass(frozen=True)
class Evaluation:
    id: UUID
    submission_id: UUID
    user_id: UUID
    challenge_id: UUID
    strategy_type: EvaluationStrategyType
    passed: bool
    score: int
    feedback: str
    status: EvaluationStatus
    processing_time_ms: int
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime
