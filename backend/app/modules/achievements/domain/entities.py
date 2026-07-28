from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.achievements.domain.enums import AchievementCriteriaType


@dataclass(frozen=True)
class AchievementDefinition:
    id: UUID
    code: str
    name: str
    description: str
    icon: str
    criteria_type: AchievementCriteriaType
    target_count: int
    is_hidden: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class UserAchievementProgress:
    user_id: UUID
    achievement_id: UUID
    current_progress: int
    unlocked_at: datetime | None
