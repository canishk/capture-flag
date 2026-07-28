from datetime import datetime
from uuid import UUID

from app.modules.leaderboards.domain.entities import LeaderboardEntry
from app.shared.schemas.response import ApiModel


class LeaderboardEntryResponse(ApiModel):
    user_id: UUID
    period: str
    period_key: str
    xp: int
    rank: int | None
    updated_at: datetime

    @classmethod
    def from_entity(cls, entry: LeaderboardEntry) -> "LeaderboardEntryResponse":
        return cls(
            user_id=entry.user_id,
            period=entry.period.value,
            period_key=entry.period_key,
            xp=entry.xp,
            rank=entry.rank,
            updated_at=entry.updated_at,
        )
