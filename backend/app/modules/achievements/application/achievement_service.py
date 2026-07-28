from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.achievements.domain import events as achievement_events
from app.modules.achievements.domain.entities import AchievementDefinition, UserAchievementProgress
from app.modules.achievements.domain.enums import AchievementCriteriaType
from app.modules.achievements.domain.exceptions import (
    AchievementNotFoundError,
    DuplicateAchievementCodeError,
)
from app.modules.achievements.infrastructure.repository import AchievementRepository
from app.shared.audit.service import AuditService
from app.shared.events.dispatcher import DomainEvent, EventDispatcher, get_event_dispatcher


class AchievementService:
    def __init__(
        self,
        session: AsyncSession,
        repository: AchievementRepository | None = None,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or AchievementRepository(session)
        self._audit = AuditService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()

    async def create_definition(
        self,
        *,
        actor_id: UUID,
        code: str,
        name: str,
        description: str,
        icon: str,
        criteria_type: AchievementCriteriaType,
        target_count: int,
        is_hidden: bool = False,
    ) -> AchievementDefinition:
        if await self._repo.get_by_code(code) is not None:
            raise DuplicateAchievementCodeError()
        achievement = await self._repo.create_definition(
            code=code,
            name=name,
            description=description,
            icon=icon,
            criteria_type=criteria_type,
            target_count=target_count,
            is_hidden=is_hidden,
        )
        await self._audit.record(
            actor_id=actor_id,
            action="achievement.created",
            resource="achievement",
            metadata={"achievementId": str(achievement.id)},
        )
        return achievement

    async def list_definitions(
        self, *, page: int, page_size: int, include_hidden: bool
    ) -> tuple[list[AchievementDefinition], int]:
        return await self._repo.list_definitions(
            page=page, page_size=page_size, include_hidden=include_hidden
        )

    async def list_my_achievements(
        self, user_id: UUID, *, page: int, page_size: int
    ) -> tuple[list[tuple[UserAchievementProgress, AchievementDefinition]], int]:
        return await self._repo.list_user_progress(user_id, page=page, page_size=page_size)

    async def get_definition(self, achievement_id: UUID) -> AchievementDefinition:
        achievement = await self._repo.get_by_id(achievement_id)
        if achievement is None:
            raise AchievementNotFoundError()
        return achievement

    async def handle_challenge_completed(self, event: DomainEvent) -> None:
        user_id = UUID(str(event.payload["userId"]))
        await self._increment_criteria(user_id, AchievementCriteriaType.CHALLENGE_COUNT, 1)

    async def handle_progress_updated(self, event: DomainEvent) -> None:
        user_id = UUID(str(event.payload["userId"]))
        xp = int(event.payload.get("totalXp", event.payload.get("xp", 0)))
        await self._set_criteria_progress(user_id, AchievementCriteriaType.XP_TOTAL, xp)

    async def handle_trophy_awarded(self, event: DomainEvent) -> None:
        user_id = UUID(str(event.payload["userId"]))
        await self._increment_criteria(user_id, AchievementCriteriaType.TROPHY_COUNT, 1)

    async def _increment_criteria(
        self, user_id: UUID, criteria_type: AchievementCriteriaType, delta: int
    ) -> None:
        achievements = await self._repo.list_by_criteria(criteria_type)
        for achievement in achievements:
            existing = await self._repo.get_progress(user_id, achievement.id)
            current = (existing.current_progress if existing else 0) + delta
            await self._maybe_unlock(user_id, achievement, current)

    async def _set_criteria_progress(
        self, user_id: UUID, criteria_type: AchievementCriteriaType, value: int
    ) -> None:
        achievements = await self._repo.list_by_criteria(criteria_type)
        for achievement in achievements:
            await self._maybe_unlock(user_id, achievement, value)

    async def _maybe_unlock(
        self, user_id: UUID, achievement: AchievementDefinition, progress: int
    ) -> None:
        existing = await self._repo.get_progress(user_id, achievement.id)
        if existing and existing.unlocked_at is not None:
            return
        unlocked = progress >= achievement.target_count
        await self._repo.upsert_progress(
            user_id, achievement.id, min(progress, achievement.target_count), unlocked
        )
        if unlocked and (existing is None or existing.unlocked_at is None):
            await self._dispatcher.publish(
                achievement_events.achievement_unlocked(achievement.id, user_id, achievement.code)
            )
            await self._audit.record(
                actor_id=user_id,
                action="achievement.unlocked",
                resource="achievement",
                metadata={"achievementId": str(achievement.id)},
            )
