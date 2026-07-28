from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.leaderboards.domain.entities import LeaderboardEntry
from app.modules.leaderboards.domain.enums import LeaderboardPeriod
from app.modules.leaderboards.infrastructure.repository import LeaderboardRepository
from app.shared.events.dispatcher import DomainEvent


class LeaderboardService:
    def __init__(
        self,
        session: AsyncSession,
        repository: LeaderboardRepository | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or LeaderboardRepository(session)

    async def handle_progress_updated(self, event: DomainEvent) -> None:
        user_id = UUID(str(event.payload["userId"]))
        xp = int(event.payload.get("totalXp", event.payload.get("xp", 0)))
        for period in LeaderboardPeriod:
            period_key = LeaderboardRepository.current_period_key(period)
            await self._repo.upsert_xp(user_id, period, period_key, xp)

    async def get_rankings(
        self,
        period: LeaderboardPeriod,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[LeaderboardEntry], int]:
        period_key = LeaderboardRepository.current_period_key(period)
        return await self._repo.list_rankings(period, period_key, page=page, page_size=page_size)

    async def get_my_ranking(
        self, user_id: UUID, period: LeaderboardPeriod
    ) -> LeaderboardEntry | None:
        period_key = LeaderboardRepository.current_period_key(period)
        return await self._repo.get_user_entry(user_id, period, period_key)
