from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class LearnerProgress:
    user_id: UUID
    total_xp: int
    challenges_attempted: int
    challenges_completed: int
    last_active_challenge_id: UUID | None
    updated_at: datetime


@dataclass(frozen=True)
class ChallengeCompletion:
    user_id: UUID
    challenge_id: UUID
    level_id: UUID
    category_id: UUID
    score: int
    completed_at: datetime


@dataclass(frozen=True)
class ProgressSummary:
    user_id: UUID
    total_xp: int
    challenges_attempted: int
    challenges_completed: int
    levels_completed: int
    categories_completed: int
    completion_percentage: float
    last_active_challenge_id: UUID | None
