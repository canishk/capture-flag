from __future__ import annotations

from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.leaderboards.domain.enums import LeaderboardPeriod
from app.shared.database.base import Base, TimestampMixin


class LeaderboardEntryModel(Base, TimestampMixin):
    __tablename__ = "leaderboard_entry"
    __table_args__ = (
        UniqueConstraint("user_id", "period", "period_key", name="uq_leaderboard_entry"),
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )
    period: Mapped[LeaderboardPeriod] = mapped_column(
        Enum(LeaderboardPeriod, name="leaderboard_period", native_enum=False),
        primary_key=True,
    )
    period_key: Mapped[str] = mapped_column(String(20), primary_key=True)
    xp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
