from typing import Any, Protocol
from uuid import UUID

from app.modules.resources.domain.entities import Resource
from app.modules.resources.domain.enums import ResourceStatus, ResourceType


class ResourceRepositoryProtocol(Protocol):
    async def create(
        self,
        *,
        title: str,
        summary: str | None,
        description: str | None,
        resource_type: ResourceType,
        url: str | None,
        file_path: str | None,
        author: str | None,
        source: str | None,
        tags: list[str],
        status: ResourceStatus,
    ) -> Resource: ...

    async def get_by_id(self, resource_id: UUID) -> Resource | None: ...

    async def list_resources(
        self,
        *,
        page: int,
        page_size: int,
        status: ResourceStatus | None = None,
        resource_type: ResourceType | None = None,
        search: str | None = None,
        tag: str | None = None,
    ) -> tuple[list[Resource], int]: ...

    async def update(self, resource_id: UUID, **kwargs: Any) -> Resource | None: ...

    async def list_by_challenge(
        self,
        challenge_id: UUID,
        *,
        page: int,
        page_size: int,
        status: ResourceStatus | None = None,
    ) -> tuple[list[Resource], int]: ...

    async def link_to_challenge(self, resource_id: UUID, challenge_id: UUID) -> None: ...

    async def unlink_from_challenge(self, resource_id: UUID, challenge_id: UUID) -> None: ...

    async def is_linked(self, resource_id: UUID, challenge_id: UUID) -> bool: ...
