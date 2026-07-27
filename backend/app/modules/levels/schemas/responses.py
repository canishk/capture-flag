from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.levels.domain.entities import Level
from app.shared.schemas.response import ApiModel


class LevelResponse(ApiModel):
    id: UUID
    category_id: UUID
    name: str
    description: str | None
    display_order: int
    status: str
    unlock_config: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, level: Level) -> "LevelResponse":
        return cls(
            id=level.id,
            category_id=level.category_id,
            name=level.name,
            description=level.description,
            display_order=level.display_order,
            status=level.status.value,
            unlock_config=level.unlock_config,
            created_at=level.created_at,
            updated_at=level.updated_at,
        )
