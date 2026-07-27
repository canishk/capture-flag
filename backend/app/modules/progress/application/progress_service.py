from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.challenges.application.challenge_service import ChallengeService
from app.modules.challenges.domain.enums import ChallengeStatus
from app.modules.levels.application.level_service import LevelService
from app.modules.progress.domain import events as progress_events
from app.modules.progress.domain.entities import LearnerProgress, ProgressSummary
from app.modules.progress.infrastructure.repository import ProgressRepository
from app.shared.events.dispatcher import DomainEvent, EventDispatcher, get_event_dispatcher


class ProgressProjectionService:
    def __init__(
        self,
        session: AsyncSession,
        repository: ProgressRepository | None = None,
        challenge_service: ChallengeService | None = None,
        level_service: LevelService | None = None,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or ProgressRepository(session)
        self._challenges = challenge_service or ChallengeService(session)
        self._levels = level_service or LevelService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()

    async def handle_submission_created(self, event: DomainEvent) -> None:
        user_id = UUID(str(event.payload["userId"]))
        challenge_id = UUID(str(event.payload["challengeId"]))
        await self._repo.increment_attempt(user_id, challenge_id)

    async def handle_evaluation_completed(self, event: DomainEvent) -> None:
        if not event.payload.get("passed"):
            await self._dispatcher.publish(
                progress_events.progress_updated(UUID(str(event.payload["userId"])))
            )
            return
        user_id = UUID(str(event.payload["userId"]))
        challenge_id = UUID(str(event.payload["challengeId"]))
        score = int(event.payload["score"])
        challenge = await self._challenges.get_challenge(challenge_id, include_non_published=True)
        already_complete = await self._repo.has_challenge_completion(user_id, challenge_id)
        await self._repo.record_challenge_completion(
            user_id=user_id,
            challenge_id=challenge_id,
            level_id=challenge.level_id,
            category_id=challenge.category_id,
            score=score,
        )
        if not already_complete:
            await self._dispatcher.publish(
                progress_events.challenge_completed(user_id, challenge_id, score)
            )
            await self._check_level_completion(user_id, challenge.level_id, challenge.category_id)
        await self._dispatcher.publish(progress_events.progress_updated(user_id))

    async def get_my_progress(self, user_id: UUID) -> LearnerProgress:
        return await self._repo.get_or_create_progress(user_id)

    async def get_summary(self, user_id: UUID) -> ProgressSummary:
        _, total = await self._challenges.list_challenges(
            page=1, page_size=1, include_non_published=False
        )
        return await self._repo.get_summary(user_id, total)

    async def _check_level_completion(
        self, user_id: UUID, level_id: UUID, category_id: UUID
    ) -> None:
        challenges, _ = await self._challenges.list_challenges(
            page=1,
            page_size=500,
            include_non_published=True,
            level_id=level_id,
        )
        required = [c for c in challenges if c.is_required and c.status == ChallengeStatus.PUBLISHED]
        if not required:
            required = [c for c in challenges if c.status == ChallengeStatus.PUBLISHED]
        if not required:
            return
        completed = await self._repo.get_completed_challenge_ids_for_level(user_id, level_id)
        if not all(c.id in completed for c in required):
            return
        if await self._repo.has_level_completion(user_id, level_id):
            return
        await self._repo.record_level_completion(user_id, level_id, category_id)
        await self._dispatcher.publish(progress_events.level_completed(user_id, level_id))
        await self._check_category_completion(user_id, category_id)

    async def _check_category_completion(self, user_id: UUID, category_id: UUID) -> None:
        levels, _ = await self._levels.list_levels(
            page=1, page_size=500, include_hidden=False, category_id=category_id
        )
        if not levels:
            return
        completed_levels = await self._repo.get_completed_level_ids_for_category(user_id, category_id)
        if not all(level.id in completed_levels for level in levels):
            return
        if await self._repo.has_category_completion(user_id, category_id):
            return
        await self._repo.record_category_completion(user_id, category_id)
        await self._dispatcher.publish(progress_events.category_completed(user_id, category_id))
