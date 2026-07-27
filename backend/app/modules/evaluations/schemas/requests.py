from typing import Any

from pydantic import Field

from app.shared.schemas.response import ApiModel


class PreviewEvaluationRequest(ApiModel):
    answer: str = Field(min_length=1)
    evaluation_strategy: dict[str, Any]
    base_score: int = Field(ge=1, default=100)
