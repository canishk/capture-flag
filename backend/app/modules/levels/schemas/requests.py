from typing import Any
from uuid import UUID

from pydantic import Field

from app.shared.schemas.response import ApiModel


class CreateLevelRequest(ApiModel):
    category_id: UUID
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    display_order: int | None = Field(default=None, ge=0)
    unlock_config: dict[str, Any] = Field(default_factory=dict)


class UpdateLevelRequest(ApiModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    unlock_config: dict[str, Any] | None = None


class ReorderLevelRequest(ApiModel):
    display_order: int = Field(ge=0)
