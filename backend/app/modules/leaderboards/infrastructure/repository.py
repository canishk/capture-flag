from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.leaderboards.domain.entities import LeaderboardEntry
from app.modules.leaderboards.domain.enums import LeaderboardPeriod
from app.modules.leaderboards.infrastructure.models import LeaderboardEntryModel


def _period_key(period: LeaderboardPeriod) -> str:
    now = datetime.now(UTC)
    if period == LeaderboardPeriod.ALL_TIME:
        return "all"
    if period == LeaderboardPeriod.WEEKLY:
        return f"{now.isocalendar().year}-W{now.isocalendar().week:02d}"
    return f"{now.year}-{now.month:02d}"


class LeaderboardRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert_xp(
        self, user_id: UUID, period: LeaderboardPeriod, period_key: str, xp: int
    ) -> None:
        result = await self._session.execute(
            select(LeaderboardEntryModel).where(
                LeaderboardEntryModel.user_id == user_id,
                LeaderboardEntryModel.period == period,
                LeaderboardEntryModel.period_key == period_key,
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            model = LeaderboardEntryModel(
                user_id=user_id, period=period, period_key=period_key, xp=xp
            )
            self._session.add(model)
        else:
            model.xp = xp
        await self._session.flush()

    async def list_rankings(
        self, period: LeaderboardPeriod, period_key: str, *, page: int, page_size: int
    ) -> tuple[list[LeaderboardEntry], int]:
        stmt = select(LeaderboardEntryModel).where(
            LeaderboardEntryModel.period == period,
            LeaderboardEntryModel.period_key == period_key,
        )
        count_stmt = select(func.count()).select_from(LeaderboardEntryModel).where(
            LeaderboardEntryModel.period == period,
            LeaderboardEntryModel.period_key == period_key,
        )
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = stmt.order_by(LeaderboardEntryModel.xp.desc()).offset((page - 1) * page_size).limit(page_size)
        result = await self._session.execute(stmt)
        entries = []
        for rank_offset, model in enumerate(result.scalars().all(), start=(page - 1) * page_size + 1):
            entries.append(
                LeaderboardEntry(
                    user_id=model.user_id,
                    period=model.period,
                    period_key=model.period_key,
                    xp=model.xp,
                    rank=rank_offset,
                    updated_at=model.updated_at,
                )
            )
        return entries, total

    async def get_user_entry(
        self, user_id: UUID, period: LeaderboardPeriod, period_key: str
    ) -> LeaderboardEntry | None:
        result = await self._session.execute(
            select(LeaderboardEntryModel).where(
                LeaderboardEntryModel.user_id == user_id,
                LeaderboardEntryModel.period == period,
                LeaderboardEntryModel.period_key == period_key,
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        higher = await self._session.scalar(
            select(func.count())
            .select_from(LeaderboardEntryModel)
            .where(
                LeaderboardEntryModel.period == period,
                LeaderboardEntryModel.period_key == period_key,
                LeaderboardEntryModel.xp > model.xp,
            )
        )
        return LeaderboardEntry(
            user_id=model.user_id,
            period=model.period,
            period_key=model.period_key,
            xp=model.xp,
            rank=int(higher or 0) + 1,
            updated_at=model.updated_at,
        )

    @staticmethod
    def current_period_key(period: LeaderboardPeriod) -> str:
        return _period_key(period)
