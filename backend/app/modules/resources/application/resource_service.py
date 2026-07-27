from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.challenges.application.challenge_service import ChallengeService
from app.modules.challenges.domain.exceptions import ChallengeNotFoundError
from app.modules.resources.domain import events as resource_events
from app.modules.resources.domain.entities import Resource
from app.modules.resources.domain.enums import ResourceStatus, ResourceType
from app.modules.resources.domain.exceptions import (
    InvalidResourceConfigurationError,
    ResourceNotFoundError,
)
from app.modules.resources.domain.interfaces import ResourceRepositoryProtocol
from app.modules.resources.infrastructure.repository import ResourceRepository
from app.shared.audit.service import AuditService
from app.shared.events.dispatcher import EventDispatcher, get_event_dispatcher


class ResourceService:
    def __init__(
        self,
        session: AsyncSession,
        repository: ResourceRepositoryProtocol | None = None,
        challenge_service: ChallengeService | None = None,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or ResourceRepository(session)
        self._challenges = challenge_service or ChallengeService(session)
        self._audit = AuditService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()

    async def create_resource(
        self,
        *,
        actor_id: UUID,
        title: str,
        summary: str | None,
        description: str | None,
        resource_type: ResourceType,
        url: str | None,
        file_path: str | None,
        author: str | None,
        source: str | None,
        tags: list[str] | None = None,
    ) -> Resource:
        self._validate_location(resource_type, url, file_path)
        resource = await self._repo.create(
            title=title,
            summary=summary,
            description=description,
            resource_type=resource_type,
            url=url,
            file_path=file_path,
            author=author,
            source=source,
            tags=tags or [],
            status=ResourceStatus.DRAFT,
        )
        await self._dispatcher.publish(resource_events.resource_created(resource.id, resource.title))
        await self._audit.record(
            actor_id=actor_id,
            action="resource.created",
            resource="resource",
            metadata={"resourceId": str(resource.id)},
        )
        return resource

    async def get_resource(self, resource_id: UUID, *, include_non_published: bool) -> Resource:
        resource = await self._repo.get_by_id(resource_id)
        if resource is None:
            raise ResourceNotFoundError()
        if not include_non_published and resource.status != ResourceStatus.PUBLISHED:
            raise ResourceNotFoundError()
        return resource

    async def list_resources(
        self,
        *,
        page: int,
        page_size: int,
        include_non_published: bool,
        resource_type: ResourceType | None = None,
        search: str | None = None,
        tag: str | None = None,
    ) -> tuple[list[Resource], int]:
        status = None if include_non_published else ResourceStatus.PUBLISHED
        return await self._repo.list_resources(
            page=page,
            page_size=page_size,
            status=status,
            resource_type=resource_type,
            search=search,
            tag=tag,
        )

    async def list_resources_for_challenge(
        self,
        challenge_id: UUID,
        *,
        page: int,
        page_size: int,
        include_non_published: bool,
    ) -> tuple[list[Resource], int]:
        await self._ensure_challenge_exists(
            challenge_id, include_non_published=include_non_published
        )
        status = None if include_non_published else ResourceStatus.PUBLISHED
        return await self._repo.list_by_challenge(
            challenge_id, page=page, page_size=page_size, status=status
        )

    async def update_resource(
        self,
        *,
        actor_id: UUID,
        resource_id: UUID,
        title: str | None = None,
        summary: str | None = None,
        description: str | None = None,
        resource_type: ResourceType | None = None,
        url: str | None = None,
        file_path: str | None = None,
        author: str | None = None,
        source: str | None = None,
        tags: list[str] | None = None,
    ) -> Resource:
        existing = await self._repo.get_by_id(resource_id)
        if existing is None:
            raise ResourceNotFoundError()
        rtype = resource_type if resource_type is not None else existing.resource_type
        new_url = url if url is not None else existing.url
        new_path = file_path if file_path is not None else existing.file_path
        self._validate_location(rtype, new_url, new_path)
        updated = await self._repo.update(
            resource_id,
            title=title,
            summary=summary,
            description=description,
            resource_type=resource_type,
            url=url,
            file_path=file_path,
            author=author,
            source=source,
            tags=tags,
        )
        if updated is None:
            raise ResourceNotFoundError()
        await self._dispatcher.publish(resource_events.resource_updated(resource_id))
        await self._audit.record(
            actor_id=actor_id,
            action="resource.updated",
            resource="resource",
            metadata={"resourceId": str(resource_id)},
        )
        return updated

    async def publish_resource(self, *, actor_id: UUID, resource_id: UUID) -> Resource:
        existing = await self._repo.get_by_id(resource_id)
        if existing is None:
            raise ResourceNotFoundError()
        self._validate_location(existing.resource_type, existing.url, existing.file_path)
        updated = await self._repo.update(resource_id, status=ResourceStatus.PUBLISHED)
        if updated is None:
            raise ResourceNotFoundError()
        await self._dispatcher.publish(resource_events.resource_published(resource_id))
        await self._audit.record(
            actor_id=actor_id,
            action="resource.published",
            resource="resource",
            metadata={"resourceId": str(resource_id)},
        )
        return updated

    async def hide_resource(self, *, actor_id: UUID, resource_id: UUID) -> Resource:
        existing = await self._repo.get_by_id(resource_id)
        if existing is None:
            raise ResourceNotFoundError()
        updated = await self._repo.update(resource_id, status=ResourceStatus.HIDDEN)
        if updated is None:
            raise ResourceNotFoundError()
        await self._dispatcher.publish(resource_events.resource_hidden(resource_id))
        await self._audit.record(
            actor_id=actor_id,
            action="resource.hidden",
            resource="resource",
            metadata={"resourceId": str(resource_id)},
        )
        return updated

    async def link_to_challenge(
        self, *, actor_id: UUID, resource_id: UUID, challenge_id: UUID
    ) -> None:
        resource = await self._repo.get_by_id(resource_id)
        if resource is None:
            raise ResourceNotFoundError()
        await self._ensure_challenge_exists(challenge_id, include_non_published=True)
        await self._repo.link_to_challenge(resource_id, challenge_id)
        await self._dispatcher.publish(resource_events.resource_linked(resource_id, challenge_id))
        await self._audit.record(
            actor_id=actor_id,
            action="resource.linked",
            resource="resource",
            metadata={"resourceId": str(resource_id), "challengeId": str(challenge_id)},
        )

    async def unlink_from_challenge(
        self, *, actor_id: UUID, resource_id: UUID, challenge_id: UUID
    ) -> None:
        if await self._repo.get_by_id(resource_id) is None:
            raise ResourceNotFoundError()
        await self._repo.unlink_from_challenge(resource_id, challenge_id)
        await self._audit.record(
            actor_id=actor_id,
            action="resource.unlinked",
            resource="resource",
            metadata={"resourceId": str(resource_id), "challengeId": str(challenge_id)},
        )

    async def _ensure_challenge_exists(
        self, challenge_id: UUID, *, include_non_published: bool
    ) -> None:
        try:
            await self._challenges.get_challenge(
                challenge_id, include_non_published=include_non_published
            )
        except ChallengeNotFoundError as exc:
            raise InvalidResourceConfigurationError("Challenge not found") from exc

    @staticmethod
    def _validate_location(
        resource_type: ResourceType, url: str | None, file_path: str | None
    ) -> None:
        if resource_type == ResourceType.DOWNLOAD and not file_path:
            raise InvalidResourceConfigurationError("Download resources require a file path")
        if resource_type != ResourceType.DOWNLOAD and not url:
            raise InvalidResourceConfigurationError("Resource requires a URL")
