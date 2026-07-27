from uuid import UUID

from pydantic import Field

from app.shared.schemas.response import ApiModel


class CreateSubmissionRequest(ApiModel):
    challenge_id: UUID
    answer: str = Field(min_length=1)
