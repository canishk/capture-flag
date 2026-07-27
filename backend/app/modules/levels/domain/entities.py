from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.levels.domain.enums import LevelStatus


@dataclass
class Level:
    id: UUID
    category_id: UUID
    name: str
    description: str | None
    display_order: int
    status: LevelStatus
    unlock_config: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
