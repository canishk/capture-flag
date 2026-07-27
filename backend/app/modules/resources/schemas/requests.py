from uuid import UUID

from pydantic import Field

from app.modules.resources.domain.enums import ResourceType
from app.shared.schemas.response import ApiModel


class CreateResourceRequest(ApiModel):
    title: str = Field(min_length=1, max_length=200)
    summary: str | None = Field(default=None, max_length=500)
    description: str | None = None
    resource_type: ResourceType
    url: str | None = Field(default=None, max_length=2048)
    file_path: str | None = Field(default=None, max_length=500)
    author: str | None = Field(default=None, max_length=200)
    source: str | None = Field(default=None, max_length=200)
    tags: list[str] = Field(default_factory=list)


class UpdateResourceRequest(ApiModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    summary: str | None = Field(default=None, max_length=500)
    description: str | None = None
    resource_type: ResourceType | None = None
    url: str | None = Field(default=None, max_length=2048)
    file_path: str | None = Field(default=None, max_length=500)
    author: str | None = Field(default=None, max_length=200)
    source: str | None = Field(default=None, max_length=200)
    tags: list[str] | None = None


class LinkResourceRequest(ApiModel):
    challenge_id: UUID
