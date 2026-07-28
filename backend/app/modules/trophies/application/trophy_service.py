from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.trophies.domain import events as trophy_events
from app.modules.trophies.domain.entities import TrophyAward, TrophyDefinition
from app.modules.trophies.domain.enums import TrophyTriggerType
from app.modules.trophies.domain.exceptions import DuplicateTrophyCodeError, TrophyNotFoundError
from app.modules.trophies.infrastructure.repository import TrophyRepository
from app.shared.audit.service import AuditService
from app.shared.events.dispatcher import DomainEvent, EventDispatcher, get_event_dispatcher


class TrophyService:
    def __init__(
        self,
        session: AsyncSession,
        repository: TrophyRepository | None = None,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or TrophyRepository(session)
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
        trigger_type: TrophyTriggerType,
        criteria: dict[str, Any] | None = None,
        is_repeatable: bool = False,
    ) -> TrophyDefinition:
        if await self._repo.get_definition_by_code(code) is not None:
            raise DuplicateTrophyCodeError()
        trophy = await self._repo.create_definition(
            code=code,
            name=name,
            description=description,
            icon=icon,
            trigger_type=trigger_type,
            criteria=criteria or {},
            is_repeatable=is_repeatable,
        )
        await self._audit.record(
            actor_id=actor_id,
            action="trophy.created",
            resource="trophy",
            metadata={"trophyId": str(trophy.id), "code": code},
        )
        return trophy

    async def list_definitions(
        self, *, page: int, page_size: int, active_only: bool
    ) -> tuple[list[TrophyDefinition], int]:
        return await self._repo.list_definitions(
            page=page, page_size=page_size, active_only=active_only
        )

    async def list_my_awards(
        self, user_id: UUID, *, page: int, page_size: int
    ) -> tuple[list[tuple[TrophyAward, TrophyDefinition]], int]:
        return await self._repo.list_user_awards(user_id, page=page, page_size=page_size)

    async def get_definition(self, trophy_id: UUID) -> TrophyDefinition:
        trophy = await self._repo.get_definition_by_id(trophy_id)
        if trophy is None:
            raise TrophyNotFoundError()
        return trophy

    async def handle_challenge_completed(self, event: DomainEvent) -> None:
        user_id = UUID(str(event.payload["userId"]))
        challenge_id = UUID(str(event.payload["challengeId"]))
        await self._evaluate_trigger(
            TrophyTriggerType.FIRST_CHALLENGE, user_id, event, extra={"challengeId": str(challenge_id)}
        )
        await self._evaluate_trigger(
            TrophyTriggerType.CHALLENGE_COMPLETED, user_id, event, extra={"challengeId": str(challenge_id)}
        )

    async def handle_level_completed(self, event: DomainEvent) -> None:
        user_id = UUID(str(event.payload["userId"]))
        await self._evaluate_trigger(
            TrophyTriggerType.LEVEL_COMPLETED,
            user_id,
            event,
            extra={"levelId": str(event.payload.get("levelId", ""))},
        )

    async def handle_category_completed(self, event: DomainEvent) -> None:
        user_id = UUID(str(event.payload["userId"]))
        await self._evaluate_trigger(
            TrophyTriggerType.CATEGORY_COMPLETED,
            user_id,
            event,
            extra={"categoryId": str(event.payload.get("categoryId", ""))},
        )

    async def _evaluate_trigger(
        self,
        trigger_type: TrophyTriggerType,
        user_id: UUID,
        event: DomainEvent,
        *,
        extra: dict[str, str],
    ) -> None:
        trophies = await self._repo.list_by_trigger(trigger_type)
        for trophy in trophies:
            if not self._matches_criteria(trophy, extra):
                continue
            if not trophy.is_repeatable and await self._repo.has_award(trophy.id, user_id):
                continue
            award = await self._repo.create_award(
                trophy_id=trophy.id,
                user_id=user_id,
                source_event_id=event.event_id,
            )
            await self._dispatcher.publish(
                trophy_events.trophy_awarded(trophy.id, user_id, trophy.code)
            )
            await self._audit.record(
                actor_id=user_id,
                action="trophy.awarded",
                resource="trophy",
                metadata={"trophyId": str(trophy.id), "awardId": str(award.id)},
            )

    @staticmethod
    def _matches_criteria(trophy: TrophyDefinition, context: dict[str, str]) -> bool:
        criteria = trophy.criteria
        if not criteria:
            return True
        for key, expected in criteria.items():
            if context.get(key) != str(expected):
                return False
        return True
