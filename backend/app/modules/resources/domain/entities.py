from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.resources.domain.enums import ResourceStatus, ResourceType


@dataclass(frozen=True)
class Resource:
    id: UUID
    title: str
    summary: str | None
    description: str | None
    resource_type: ResourceType
    url: str | None
    file_path: str | None
    author: str | None
    source: str | None
    tags: list[str]
    status: ResourceStatus
    created_at: datetime
    updated_at: datetime
