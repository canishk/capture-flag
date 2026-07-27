from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.hints.domain.enums import HintStatus


@dataclass(frozen=True)
class Hint:
    id: UUID
    challenge_id: UUID
    title: str
    content: str
    display_order: int
    penalty_config: dict[str, Any]
    unlock_config: dict[str, Any]
    status: HintStatus
    created_at: datetime
    updated_at: datetime
