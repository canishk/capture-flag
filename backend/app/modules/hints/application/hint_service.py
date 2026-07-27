from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.challenges.application.challenge_service import ChallengeService
from app.modules.challenges.domain.exceptions import ChallengeNotFoundError
from app.modules.hints.domain import events as hint_events
from app.modules.hints.domain.entities import Hint
from app.modules.hints.domain.enums import HintStatus
from app.modules.hints.domain.exceptions import (
    DuplicateHintOrderError,
    HintNotFoundError,
    InvalidHintConfigurationError,
)
from app.modules.hints.domain.interfaces import HintRepositoryProtocol
from app.modules.hints.infrastructure.repository import HintRepository
from app.shared.audit.service import AuditService
from app.shared.events.dispatcher import EventDispatcher, get_event_dispatcher


class HintService:
    def __init__(
        self,
        session: AsyncSession,
        repository: HintRepositoryProtocol | None = None,
        challenge_service: ChallengeService | None = None,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or HintRepository(session)
        self._challenges = challenge_service or ChallengeService(session)
        self._audit = AuditService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()

    async def create_hint(
        self,
        *,
        actor_id: UUID,
        challenge_id: UUID,
        title: str,
        content: str,
        display_order: int | None = None,
        penalty_config: dict[str, Any] | None = None,
        unlock_config: dict[str, Any] | None = None,
    ) -> Hint:
        await self._ensure_challenge_exists(challenge_id, include_non_published=True)
        self._validate_content(content)
        order = (
            display_order
            if display_order is not None
            else await self._repo.get_max_display_order(challenge_id) + 1
        )
        if await self._repo.order_exists(challenge_id, order):
            raise DuplicateHintOrderError()
        hint = await self._repo.create(
            challenge_id=challenge_id,
            title=title,
            content=content,
            display_order=order,
            penalty_config=penalty_config or {},
            unlock_config=unlock_config or {},
            status=HintStatus.DRAFT,
        )
        await self._dispatcher.publish(hint_events.hint_created(hint.id, challenge_id))
        await self._audit.record(
            actor_id=actor_id,
            action="hint.created",
            resource="hint",
            metadata={"hintId": str(hint.id), "challengeId": str(challenge_id)},
        )
        return hint

    async def get_hint(self, hint_id: UUID, *, include_non_published: bool) -> Hint:
        hint = await self._repo.get_by_id(hint_id)
        if hint is None:
            raise HintNotFoundError()
        if not include_non_published and hint.status != HintStatus.PUBLISHED:
            raise HintNotFoundError()
        return hint

    async def list_hints_for_challenge(
        self,
        challenge_id: UUID,
        *,
        page: int,
        page_size: int,
        include_non_published: bool,
    ) -> tuple[list[Hint], int]:
        await self._ensure_challenge_exists(
            challenge_id, include_non_published=include_non_published
        )
        status = None if include_non_published else HintStatus.PUBLISHED
        return await self._repo.list_by_challenge(
            challenge_id, page=page, page_size=page_size, status=status
        )

    async def update_hint(
        self,
        *,
        actor_id: UUID,
        hint_id: UUID,
        title: str | None = None,
        content: str | None = None,
        penalty_config: dict[str, Any] | None = None,
        unlock_config: dict[str, Any] | None = None,
    ) -> Hint:
        existing = await self._repo.get_by_id(hint_id)
        if existing is None:
            raise HintNotFoundError()
        if content is not None:
            self._validate_content(content)
        updated = await self._repo.update(
            hint_id,
            title=title,
            content=content,
            penalty_config=penalty_config,
            unlock_config=unlock_config,
        )
        if updated is None:
            raise HintNotFoundError()
        await self._dispatcher.publish(hint_events.hint_updated(hint_id))
        await self._audit.record(
            actor_id=actor_id,
            action="hint.updated",
            resource="hint",
            metadata={"hintId": str(hint_id)},
        )
        return updated

    async def publish_hint(self, *, actor_id: UUID, hint_id: UUID) -> Hint:
        existing = await self._repo.get_by_id(hint_id)
        if existing is None:
            raise HintNotFoundError()
        updated = await self._repo.update(hint_id, status=HintStatus.PUBLISHED)
        if updated is None:
            raise HintNotFoundError()
        await self._dispatcher.publish(hint_events.hint_published(hint_id))
        await self._audit.record(
            actor_id=actor_id,
            action="hint.published",
            resource="hint",
            metadata={"hintId": str(hint_id)},
        )
        return updated

    async def hide_hint(self, *, actor_id: UUID, hint_id: UUID) -> Hint:
        existing = await self._repo.get_by_id(hint_id)
        if existing is None:
            raise HintNotFoundError()
        updated = await self._repo.update(hint_id, status=HintStatus.HIDDEN)
        if updated is None:
            raise HintNotFoundError()
        await self._dispatcher.publish(hint_events.hint_hidden(hint_id))
        await self._audit.record(
            actor_id=actor_id,
            action="hint.hidden",
            resource="hint",
            metadata={"hintId": str(hint_id)},
        )
        return updated

    async def reorder_hint(
        self,
        *,
        actor_id: UUID,
        challenge_id: UUID,
        hint_id: UUID,
        display_order: int,
    ) -> Hint:
        existing = await self._repo.get_by_id(hint_id)
        if existing is None or existing.challenge_id != challenge_id:
            raise HintNotFoundError()
        if await self._repo.order_exists(challenge_id, display_order, exclude_id=hint_id):
            raise DuplicateHintOrderError()
        updated = await self._repo.update_display_order(hint_id, display_order)
        if updated is None:
            raise HintNotFoundError()
        await self._audit.record(
            actor_id=actor_id,
            action="hint.reordered",
            resource="hint",
            metadata={"hintId": str(hint_id), "displayOrder": display_order},
        )
        return updated

    async def _ensure_challenge_exists(
        self, challenge_id: UUID, *, include_non_published: bool
    ) -> None:
        try:
            await self._challenges.get_challenge(
                challenge_id, include_non_published=include_non_published
            )
        except ChallengeNotFoundError as exc:
            raise InvalidHintConfigurationError("Challenge not found") from exc

    @staticmethod
    def _validate_content(content: str) -> None:
        if not content.strip():
            raise InvalidHintConfigurationError("Hint content is required")
