from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.challenges.domain.entities import Challenge
from app.shared.schemas.response import ApiModel


class ChallengeResponse(ApiModel):
    id: UUID
    category_id: UUID
    level_id: UUID
    title: str
    summary: str | None
    description: str
    objectives: list[str]
    challenge_type: str
    difficulty: str
    estimated_duration_minutes: int | None
    status: str
    display_order: int
    base_score: int
    scoring_config: dict[str, Any]
    evaluation_strategy: dict[str, Any]
    unlock_config: dict[str, Any]
    is_required: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, challenge: Challenge, *, include_sensitive: bool = False) -> "ChallengeResponse":
        strategy = challenge.evaluation_strategy if include_sensitive else {
            "type": challenge.evaluation_strategy.get("type"),
        }
        return cls(
            id=challenge.id,
            category_id=challenge.category_id,
            level_id=challenge.level_id,
            title=challenge.title,
            summary=challenge.summary,
            description=challenge.description,
            objectives=challenge.objectives,
            challenge_type=challenge.challenge_type.value,
            difficulty=challenge.difficulty.value,
            estimated_duration_minutes=challenge.estimated_duration_minutes,
            status=challenge.status.value,
            display_order=challenge.display_order,
            base_score=challenge.base_score,
            scoring_config=challenge.scoring_config,
            evaluation_strategy=strategy,
            unlock_config=challenge.unlock_config,
            is_required=challenge.is_required,
            created_at=challenge.created_at,
            updated_at=challenge.updated_at,
        )
