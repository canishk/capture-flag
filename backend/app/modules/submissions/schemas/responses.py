from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.submissions.domain.entities import Submission
from app.shared.schemas.response import ApiModel


class SubmissionResponse(ApiModel):
    id: UUID
    user_id: UUID
    challenge_id: UUID
    answer: str
    attempt_number: int
    status: str
    evaluation_strategy_snapshot: dict[str, Any]
    feedback: str | None
    processing_time_ms: int | None
    submitted_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, submission: Submission, *, include_answer: bool = True) -> "SubmissionResponse":
        return cls(
            id=submission.id,
            user_id=submission.user_id,
            challenge_id=submission.challenge_id,
            answer=submission.answer if include_answer else "",
            attempt_number=submission.attempt_number,
            status=submission.status.value,
            evaluation_strategy_snapshot=submission.evaluation_strategy_snapshot,
            feedback=submission.feedback,
            processing_time_ms=submission.processing_time_ms,
            submitted_at=submission.submitted_at,
            updated_at=submission.updated_at,
        )
