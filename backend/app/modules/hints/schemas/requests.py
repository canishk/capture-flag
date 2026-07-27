from typing import Any
from uuid import UUID

from pydantic import Field

from app.shared.schemas.response import ApiModel


class CreateHintRequest(ApiModel):
    challenge_id: UUID
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    display_order: int | None = Field(default=None, ge=1)
    penalty_config: dict[str, Any] = Field(default_factory=dict)
    unlock_config: dict[str, Any] = Field(default_factory=dict)


class UpdateHintRequest(ApiModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    penalty_config: dict[str, Any] | None = None
    unlock_config: dict[str, Any] | None = None


class ReorderHintRequest(ApiModel):
    hint_id: UUID
    display_order: int = Field(ge=1)
