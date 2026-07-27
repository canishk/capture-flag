from typing import Any
from uuid import UUID

from pydantic import Field

from app.modules.challenges.domain.enums import ChallengeDifficulty, ChallengeType
from app.shared.schemas.response import ApiModel


class CreateChallengeRequest(ApiModel):
    category_id: UUID
    level_id: UUID
    title: str = Field(min_length=2, max_length=200)
    summary: str | None = Field(default=None, max_length=500)
    description: str = Field(min_length=1)
    objectives: list[str] = Field(min_length=1)
    challenge_type: ChallengeType
    difficulty: ChallengeDifficulty = ChallengeDifficulty.BEGINNER
    estimated_duration_minutes: int | None = Field(default=None, ge=1)
    base_score: int = Field(ge=1)
    evaluation_strategy: dict[str, Any]
    scoring_config: dict[str, Any] = Field(default_factory=dict)
    unlock_config: dict[str, Any] = Field(default_factory=dict)
    is_required: bool = False
    display_order: int | None = Field(default=None, ge=0)


class UpdateChallengeRequest(ApiModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    summary: str | None = Field(default=None, max_length=500)
    description: str | None = Field(default=None, min_length=1)
    objectives: list[str] | None = Field(default=None, min_length=1)
    challenge_type: ChallengeType | None = None
    difficulty: ChallengeDifficulty | None = None
    estimated_duration_minutes: int | None = Field(default=None, ge=1)
    base_score: int | None = Field(default=None, ge=1)
    evaluation_strategy: dict[str, Any] | None = None
    scoring_config: dict[str, Any] | None = None
    unlock_config: dict[str, Any] | None = None
    is_required: bool | None = None


class ReorderChallengeRequest(ApiModel):
    display_order: int = Field(ge=0)
