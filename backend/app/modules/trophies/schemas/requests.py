from typing import Any

from pydantic import Field

from app.modules.trophies.domain.enums import TrophyTriggerType
from app.shared.schemas.response import ApiModel


class CreateTrophyRequest(ApiModel):
    code: str = Field(min_length=2, max_length=80)
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=1)
    icon: str = Field(min_length=1, max_length=80)
    trigger_type: TrophyTriggerType
    criteria: dict[str, Any] = Field(default_factory=dict)
    is_repeatable: bool = False
