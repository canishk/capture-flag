from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.hints.domain.entities import Hint
from app.shared.schemas.response import ApiModel


class HintResponse(ApiModel):
    id: UUID
    challenge_id: UUID
    title: str
    content: str
    display_order: int
    penalty_config: dict[str, Any]
    unlock_config: dict[str, Any]
    status: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, hint: Hint) -> "HintResponse":
        return cls(
            id=hint.id,
            challenge_id=hint.challenge_id,
            title=hint.title,
            content=hint.content,
            display_order=hint.display_order,
            penalty_config=hint.penalty_config,
            unlock_config=hint.unlock_config,
            status=hint.status.value,
            created_at=hint.created_at,
            updated_at=hint.updated_at,
        )
