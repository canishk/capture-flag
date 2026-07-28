from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.trophies.domain.entities import TrophyAward, TrophyDefinition
from app.shared.schemas.response import ApiModel


class TrophyDefinitionResponse(ApiModel):
    id: UUID
    code: str
    name: str
    description: str
    icon: str
    trigger_type: str
    criteria: dict[str, Any]
    is_repeatable: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, trophy: TrophyDefinition) -> "TrophyDefinitionResponse":
        return cls(
            id=trophy.id,
            code=trophy.code,
            name=trophy.name,
            description=trophy.description,
            icon=trophy.icon,
            trigger_type=trophy.trigger_type.value,
            criteria=trophy.criteria,
            is_repeatable=trophy.is_repeatable,
            is_active=trophy.is_active,
            created_at=trophy.created_at,
            updated_at=trophy.updated_at,
        )


class TrophyAwardResponse(ApiModel):
    id: UUID
    trophy_id: UUID
    user_id: UUID
    awarded_at: datetime
    trophy: TrophyDefinitionResponse

    @classmethod
    def from_entities(cls, award: TrophyAward, trophy: TrophyDefinition) -> "TrophyAwardResponse":
        return cls(
            id=award.id,
            trophy_id=award.trophy_id,
            user_id=award.user_id,
            awarded_at=award.awarded_at,
            trophy=TrophyDefinitionResponse.from_entity(trophy),
        )
