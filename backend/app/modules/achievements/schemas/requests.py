
from pydantic import Field

from app.modules.achievements.domain.enums import AchievementCriteriaType
from app.shared.schemas.response import ApiModel


class CreateAchievementRequest(ApiModel):
    code: str = Field(min_length=2, max_length=80)
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=1)
    icon: str = Field(min_length=1, max_length=80)
    criteria_type: AchievementCriteriaType
    target_count: int = Field(ge=1)
    is_hidden: bool = False
