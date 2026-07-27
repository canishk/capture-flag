from typing import Any
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.resources.domain.entities import Resource
from app.modules.resources.domain.enums import ResourceStatus, ResourceType
from app.modules.resources.infrastructure.models import ChallengeResourceModel, ResourceModel


class ResourceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

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
    ) -> Resource:
        model = ResourceModel(
            title=title,
            summary=summary,
            description=description,
            resource_type=resource_type,
            url=url,
            file_path=file_path,
            author=author,
            source=source,
            tags=tags,
            status=status,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, resource_id: UUID) -> Resource | None:
        result = await self._session.execute(
            select(ResourceModel).where(ResourceModel.id == resource_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_resources(
        self,
        *,
        page: int,
        page_size: int,
        status: ResourceStatus | None = None,
        resource_type: ResourceType | None = None,
        search: str | None = None,
        tag: str | None = None,
    ) -> tuple[list[Resource], int]:
        stmt = select(ResourceModel)
        count_stmt = select(func.count()).select_from(ResourceModel)
        if status is not None:
            stmt = stmt.where(ResourceModel.status == status)
            count_stmt = count_stmt.where(ResourceModel.status == status)
        if resource_type is not None:
            stmt = stmt.where(ResourceModel.resource_type == resource_type)
            count_stmt = count_stmt.where(ResourceModel.resource_type == resource_type)
        if search:
            pattern = f"%{search}%"
            condition = or_(
                ResourceModel.title.ilike(pattern),
                ResourceModel.summary.ilike(pattern),
            )
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)
        if tag:
            stmt = stmt.where(ResourceModel.tags.contains([tag]))
            count_stmt = count_stmt.where(ResourceModel.tags.contains([tag]))
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(ResourceModel.title.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()], total

    async def update(self, resource_id: UUID, **kwargs: Any) -> Resource | None:
        model = await self._get_model(resource_id)
        if model is None:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(model, key):
                setattr(model, key, value)
        await self._session.flush()
        return self._to_entity(model)

    async def list_by_challenge(
        self,
        challenge_id: UUID,
        *,
        page: int,
        page_size: int,
        status: ResourceStatus | None = None,
    ) -> tuple[list[Resource], int]:
        stmt = (
            select(ResourceModel)
            .join(ChallengeResourceModel, ChallengeResourceModel.resource_id == ResourceModel.id)
            .where(ChallengeResourceModel.challenge_id == challenge_id)
        )
        count_stmt = (
            select(func.count())
            .select_from(ResourceModel)
            .join(ChallengeResourceModel, ChallengeResourceModel.resource_id == ResourceModel.id)
            .where(ChallengeResourceModel.challenge_id == challenge_id)
        )
        if status is not None:
            stmt = stmt.where(ResourceModel.status == status)
            count_stmt = count_stmt.where(ResourceModel.status == status)
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(ResourceModel.title.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()], total

    async def link_to_challenge(self, resource_id: UUID, challenge_id: UUID) -> None:
        if await self.is_linked(resource_id, challenge_id):
            return
        self._session.add(
            ChallengeResourceModel(challenge_id=challenge_id, resource_id=resource_id)
        )
        await self._session.flush()

    async def unlink_from_challenge(self, resource_id: UUID, challenge_id: UUID) -> None:
        result = await self._session.execute(
            select(ChallengeResourceModel).where(
                ChallengeResourceModel.challenge_id == challenge_id,
                ChallengeResourceModel.resource_id == resource_id,
            )
        )
        link = result.scalar_one_or_none()
        if link is not None:
            await self._session.delete(link)
            await self._session.flush()

    async def is_linked(self, resource_id: UUID, challenge_id: UUID) -> bool:
        result = await self._session.scalar(
            select(func.count())
            .select_from(ChallengeResourceModel)
            .where(
                ChallengeResourceModel.challenge_id == challenge_id,
                ChallengeResourceModel.resource_id == resource_id,
            )
        )
        return int(result or 0) > 0

    async def _get_model(self, resource_id: UUID) -> ResourceModel | None:
        result = await self._session.execute(
            select(ResourceModel).where(ResourceModel.id == resource_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def _to_entity(model: ResourceModel) -> Resource:
        return Resource(
            id=model.id,
            title=model.title,
            summary=model.summary,
            description=model.description,
            resource_type=model.resource_type,
            url=model.url,
            file_path=model.file_path,
            author=model.author,
            source=model.source,
            tags=model.tags,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
