from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.leaderboards.domain.enums import LeaderboardPeriod


@dataclass(frozen=True)
class LeaderboardEntry:
    user_id: UUID
    period: LeaderboardPeriod
    period_key: str
    xp: int
    rank: int | None
    updated_at: datetime
