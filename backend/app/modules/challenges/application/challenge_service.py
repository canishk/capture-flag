from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.application.category_service import CategoryService
from app.modules.categories.domain.exceptions import CategoryNotFoundError
from app.modules.challenges.domain import events as challenge_events
from app.modules.challenges.domain.entities import Challenge
from app.modules.challenges.domain.enums import (
    ChallengeDifficulty,
    ChallengeStatus,
    ChallengeType,
)
from app.modules.challenges.domain.exceptions import (
    ChallengeNotFoundError,
    DuplicateChallengeTitleError,
    InvalidChallengeConfigurationError,
    InvalidChallengeStatusTransitionError,
)
from app.modules.challenges.domain.interfaces import ChallengeRepositoryProtocol
from app.modules.challenges.infrastructure.repository import ChallengeRepository
from app.modules.levels.application.level_service import LevelService
from app.modules.levels.domain.exceptions import LevelNotFoundError
from app.shared.audit.service import AuditService
from app.shared.events.dispatcher import EventDispatcher, get_event_dispatcher

_PUBLISHABLE_STATUSES = {ChallengeStatus.DRAFT, ChallengeStatus.REVIEW, ChallengeStatus.HIDDEN}
_ARCHIVABLE_STATUSES = {ChallengeStatus.PUBLISHED, ChallengeStatus.HIDDEN}


class ChallengeService:
    def __init__(
        self,
        session: AsyncSession,
        repository: ChallengeRepositoryProtocol | None = None,
        category_service: CategoryService | None = None,
        level_service: LevelService | None = None,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or ChallengeRepository(session)
        self._categories = category_service or CategoryService(session)
        self._levels = level_service or LevelService(session)
        self._audit = AuditService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()

    async def create_challenge(
        self,
        *,
        actor_id: UUID,
        category_id: UUID,
        level_id: UUID,
        title: str,
        summary: str | None,
        description: str,
        objectives: list[str],
        challenge_type: ChallengeType,
        difficulty: ChallengeDifficulty,
        estimated_duration_minutes: int | None,
        base_score: int,
        evaluation_strategy: dict[str, Any],
        scoring_config: dict[str, Any] | None = None,
        unlock_config: dict[str, Any] | None = None,
        is_required: bool = False,
        display_order: int | None = None,
    ) -> Challenge:
        await self._ensure_placement(category_id, level_id, include_hidden=True)
        self._validate_configuration(objectives, base_score, evaluation_strategy)
        if await self._repo.get_by_title_in_level(level_id, title) is not None:
            raise DuplicateChallengeTitleError()
        order = (
            display_order
            if display_order is not None
            else await self._repo.get_max_display_order(level_id) + 1
        )
        challenge = await self._repo.create(
            category_id=category_id,
            level_id=level_id,
            title=title,
            summary=summary,
            description=description,
            objectives=objectives,
            challenge_type=challenge_type,
            difficulty=difficulty,
            estimated_duration_minutes=estimated_duration_minutes,
            status=ChallengeStatus.DRAFT,
            display_order=order,
            base_score=base_score,
            scoring_config=scoring_config or {},
            evaluation_strategy=evaluation_strategy,
            unlock_config=unlock_config or {},
            is_required=is_required,
        )
        await self._dispatcher.publish(
            challenge_events.challenge_created(challenge.id, challenge.level_id, challenge.title)
        )
        await self._audit.record(
            actor_id=actor_id,
            action="challenge.created",
            resource="challenge",
            metadata={"challengeId": str(challenge.id), "levelId": str(level_id)},
        )
        return challenge

    async def get_challenge(self, challenge_id: UUID, *, include_non_published: bool) -> Challenge:
        challenge = await self._repo.get_by_id(challenge_id)
        if challenge is None:
            raise ChallengeNotFoundError()
        if not include_non_published and challenge.status != ChallengeStatus.PUBLISHED:
            raise ChallengeNotFoundError()
        return challenge

    async def list_challenges(
        self,
        *,
        page: int,
        page_size: int,
        include_non_published: bool,
        category_id: UUID | None = None,
        level_id: UUID | None = None,
        search: str | None = None,
    ) -> tuple[list[Challenge], int]:
        status = None if include_non_published else ChallengeStatus.PUBLISHED
        if category_id is not None:
            await self._categories.get_category(category_id, include_hidden=include_non_published)
        if level_id is not None:
            await self._levels.get_level(level_id, include_hidden=include_non_published)
        return await self._repo.list_challenges(
            page=page,
            page_size=page_size,
            status=status,
            category_id=category_id,
            level_id=level_id,
            search=search,
        )

    async def update_challenge(
        self,
        *,
        actor_id: UUID,
        challenge_id: UUID,
        title: str | None = None,
        summary: str | None = None,
        description: str | None = None,
        objectives: list[str] | None = None,
        challenge_type: ChallengeType | None = None,
        difficulty: ChallengeDifficulty | None = None,
        estimated_duration_minutes: int | None = None,
        base_score: int | None = None,
        evaluation_strategy: dict[str, Any] | None = None,
        scoring_config: dict[str, Any] | None = None,
        unlock_config: dict[str, Any] | None = None,
        is_required: bool | None = None,
    ) -> Challenge:
        existing = await self._repo.get_by_id(challenge_id)
        if existing is None:
            raise ChallengeNotFoundError()
        if title is not None and title != existing.title:
            duplicate = await self._repo.get_by_title_in_level(existing.level_id, title)
            if duplicate is not None:
                raise DuplicateChallengeTitleError()
        if objectives is not None or base_score is not None or evaluation_strategy is not None:
            self._validate_configuration(
                objectives if objectives is not None else existing.objectives,
                base_score if base_score is not None else existing.base_score,
                evaluation_strategy
                if evaluation_strategy is not None
                else existing.evaluation_strategy,
            )
        updated = await self._repo.update(
            challenge_id,
            title=title,
            summary=summary,
            description=description,
            objectives=objectives,
            challenge_type=challenge_type,
            difficulty=difficulty,
            estimated_duration_minutes=estimated_duration_minutes,
            base_score=base_score,
            evaluation_strategy=evaluation_strategy,
            scoring_config=scoring_config,
            unlock_config=unlock_config,
            is_required=is_required,
        )
        if updated is None:
            raise ChallengeNotFoundError()
        await self._dispatcher.publish(challenge_events.challenge_updated(updated.id))
        await self._audit.record(
            actor_id=actor_id,
            action="challenge.updated",
            resource="challenge",
            metadata={"challengeId": str(challenge_id)},
        )
        return updated

    async def publish_challenge(self, *, actor_id: UUID, challenge_id: UUID) -> Challenge:
        existing = await self._repo.get_by_id(challenge_id)
        if existing is None:
            raise ChallengeNotFoundError()
        if existing.status not in _PUBLISHABLE_STATUSES:
            raise InvalidChallengeStatusTransitionError(
                "Only draft, review, or hidden challenges can be published"
            )
        self._validate_configuration(
            existing.objectives, existing.base_score, existing.evaluation_strategy
        )
        updated = await self._repo.update(challenge_id, status=ChallengeStatus.PUBLISHED)
        if updated is None:
            raise ChallengeNotFoundError()
        await self._dispatcher.publish(challenge_events.challenge_published(challenge_id))
        await self._audit.record(
            actor_id=actor_id,
            action="challenge.published",
            resource="challenge",
            metadata={"challengeId": str(challenge_id)},
        )
        return updated

    async def hide_challenge(self, *, actor_id: UUID, challenge_id: UUID) -> Challenge:
        existing = await self._repo.get_by_id(challenge_id)
        if existing is None:
            raise ChallengeNotFoundError()
        updated = await self._repo.update(challenge_id, status=ChallengeStatus.HIDDEN)
        if updated is None:
            raise ChallengeNotFoundError()
        await self._dispatcher.publish(challenge_events.challenge_hidden(challenge_id))
        await self._audit.record(
            actor_id=actor_id,
            action="challenge.hidden",
            resource="challenge",
            metadata={"challengeId": str(challenge_id)},
        )
        return updated

    async def archive_challenge(self, *, actor_id: UUID, challenge_id: UUID) -> Challenge:
        existing = await self._repo.get_by_id(challenge_id)
        if existing is None:
            raise ChallengeNotFoundError()
        if existing.status not in _ARCHIVABLE_STATUSES:
            raise InvalidChallengeStatusTransitionError(
                "Only published or hidden challenges can be archived"
            )
        updated = await self._repo.update(challenge_id, status=ChallengeStatus.ARCHIVED)
        if updated is None:
            raise ChallengeNotFoundError()
        await self._dispatcher.publish(challenge_events.challenge_archived(challenge_id))
        await self._audit.record(
            actor_id=actor_id,
            action="challenge.archived",
            resource="challenge",
            metadata={"challengeId": str(challenge_id)},
        )
        return updated

    async def reorder_challenge(
        self,
        *,
        actor_id: UUID,
        challenge_id: UUID,
        display_order: int,
    ) -> Challenge:
        updated = await self._repo.update_display_order(challenge_id, display_order)
        if updated is None:
            raise ChallengeNotFoundError()
        await self._audit.record(
            actor_id=actor_id,
            action="challenge.reordered",
            resource="challenge",
            metadata={"challengeId": str(challenge_id), "displayOrder": display_order},
        )
        return updated

    async def challenge_exists(self, challenge_id: UUID) -> bool:
        return await self._repo.get_by_id(challenge_id) is not None

    async def _ensure_placement(
        self, category_id: UUID, level_id: UUID, *, include_hidden: bool
    ) -> None:
        try:
            await self._categories.get_category(category_id, include_hidden=include_hidden)
            level = await self._levels.get_level(level_id, include_hidden=include_hidden)
        except (CategoryNotFoundError, LevelNotFoundError) as exc:
            raise InvalidChallengeConfigurationError("Invalid category or level") from exc
        if level.category_id != category_id:
            raise InvalidChallengeConfigurationError("Level does not belong to category")

    @staticmethod
    def _validate_configuration(
        objectives: list[str],
        base_score: int,
        evaluation_strategy: dict[str, Any],
    ) -> None:
        if not [o for o in objectives if o.strip()]:
            raise InvalidChallengeConfigurationError("At least one learning objective is required")
        if base_score <= 0:
            raise InvalidChallengeConfigurationError("Base score must be a positive integer")
        if not evaluation_strategy:
            raise InvalidChallengeConfigurationError("Evaluation strategy is required")
