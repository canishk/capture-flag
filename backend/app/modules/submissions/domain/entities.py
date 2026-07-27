from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.submissions.domain.enums import SubmissionStatus


@dataclass(frozen=True)
class Submission:
    id: UUID
    user_id: UUID
    challenge_id: UUID
    answer: str
    attempt_number: int
    status: SubmissionStatus
    evaluation_strategy_snapshot: dict[str, Any]
    feedback: str | None
    processing_time_ms: int | None
    submitted_at: datetime
    updated_at: datetime
