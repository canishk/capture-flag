from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.challenges.domain.enums import (
    ChallengeDifficulty,
    ChallengeStatus,
    ChallengeType,
)


@dataclass(frozen=True)
class Challenge:
    id: UUID
    category_id: UUID
    level_id: UUID
    title: str
    summary: str | None
    description: str
    objectives: list[str]
    challenge_type: ChallengeType
    difficulty: ChallengeDifficulty
    estimated_duration_minutes: int | None
    status: ChallengeStatus
    display_order: int
    base_score: int
    scoring_config: dict[str, Any]
    evaluation_strategy: dict[str, Any]
    unlock_config: dict[str, Any]
    is_required: bool
    created_at: datetime
    updated_at: datetime
