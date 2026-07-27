from datetime import datetime
from uuid import UUID

from app.modules.progress.domain.entities import LearnerProgress, ProgressSummary
from app.shared.schemas.response import ApiModel


class LearnerProgressResponse(ApiModel):
    user_id: UUID
    total_xp: int
    challenges_attempted: int
    challenges_completed: int
    last_active_challenge_id: UUID | None
    updated_at: datetime

    @classmethod
    def from_entity(cls, progress: LearnerProgress) -> "LearnerProgressResponse":
        return cls(
            user_id=progress.user_id,
            total_xp=progress.total_xp,
            challenges_attempted=progress.challenges_attempted,
            challenges_completed=progress.challenges_completed,
            last_active_challenge_id=progress.last_active_challenge_id,
            updated_at=progress.updated_at,
        )


class ProgressSummaryResponse(ApiModel):
    user_id: UUID
    total_xp: int
    challenges_attempted: int
    challenges_completed: int
    levels_completed: int
    categories_completed: int
    completion_percentage: float
    last_active_challenge_id: UUID | None

    @classmethod
    def from_entity(cls, summary: ProgressSummary) -> "ProgressSummaryResponse":
        return cls(
            user_id=summary.user_id,
            total_xp=summary.total_xp,
            challenges_attempted=summary.challenges_attempted,
            challenges_completed=summary.challenges_completed,
            levels_completed=summary.levels_completed,
            categories_completed=summary.categories_completed,
            completion_percentage=summary.completion_percentage,
            last_active_challenge_id=summary.last_active_challenge_id,
        )
