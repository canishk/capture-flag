from datetime import datetime
from uuid import UUID

from app.modules.resources.domain.entities import Resource
from app.shared.schemas.response import ApiModel


class ResourceResponse(ApiModel):
    id: UUID
    title: str
    summary: str | None
    description: str | None
    resource_type: str
    url: str | None
    file_path: str | None
    author: str | None
    source: str | None
    tags: list[str]
    status: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, resource: Resource) -> "ResourceResponse":
        return cls(
            id=resource.id,
            title=resource.title,
            summary=resource.summary,
            description=resource.description,
            resource_type=resource.resource_type.value,
            url=resource.url,
            file_path=resource.file_path,
            author=resource.author,
            source=resource.source,
            tags=resource.tags,
            status=resource.status.value,
            created_at=resource.created_at,
            updated_at=resource.updated_at,
        )
