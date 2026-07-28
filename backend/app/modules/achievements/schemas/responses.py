from datetime import datetime
from uuid import UUID

from app.modules.achievements.domain.entities import AchievementDefinition, UserAchievementProgress
from app.shared.schemas.response import ApiModel


class AchievementDefinitionResponse(ApiModel):
    id: UUID
    code: str
    name: str
    description: str
    icon: str
    criteria_type: str
    target_count: int
    is_hidden: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, a: AchievementDefinition) -> "AchievementDefinitionResponse":
        return cls(
            id=a.id,
            code=a.code,
            name=a.name,
            description=a.description,
            icon=a.icon,
            criteria_type=a.criteria_type.value,
            target_count=a.target_count,
            is_hidden=a.is_hidden,
            is_active=a.is_active,
            created_at=a.created_at,
            updated_at=a.updated_at,
        )


class UserAchievementResponse(ApiModel):
    achievement_id: UUID
    current_progress: int
    target_count: int
    unlocked_at: datetime | None
    achievement: AchievementDefinitionResponse

    @classmethod
    def from_entities(
        cls, progress: UserAchievementProgress, achievement: AchievementDefinition
    ) -> "UserAchievementResponse":
        return cls(
            achievement_id=progress.achievement_id,
            current_progress=progress.current_progress,
            target_count=achievement.target_count,
            unlocked_at=progress.unlocked_at,
            achievement=AchievementDefinitionResponse.from_entity(achievement),
        )
