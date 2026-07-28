from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.trophies.domain.enums import TrophyTriggerType


@dataclass(frozen=True)
class TrophyDefinition:
    id: UUID
    code: str
    name: str
    description: str
    icon: str
    trigger_type: TrophyTriggerType
    criteria: dict[str, Any]
    is_repeatable: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class TrophyAward:
    id: UUID
    trophy_id: UUID
    user_id: UUID
    source_event_id: UUID
    awarded_at: datetime
