from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.achievements.domain.enums import AchievementCriteriaType
from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AchievementDefinitionModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "achievement_definition"

    code: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str] = mapped_column(String(80), nullable=False)
    criteria_type: Mapped[AchievementCriteriaType] = mapped_column(
        Enum(AchievementCriteriaType, name="achievement_criteria_type", native_enum=False),
        nullable=False,
        index=True,
    )
    target_count: Mapped[int] = mapped_column(Integer, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)


class UserAchievementProgressModel(Base):
    __tablename__ = "user_achievement_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement_progress"),
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    )
    achievement_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("achievement_definition.id", ondelete="CASCADE"),
        primary_key=True,
    )
    current_progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unlocked_at: Mapped[datetime | None] = mapped_column(nullable=True)
