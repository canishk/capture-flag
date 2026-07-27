from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import JSON, Boolean, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.challenges.domain.enums import (
    ChallengeDifficulty,
    ChallengeStatus,
    ChallengeType,
)
from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ChallengeModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "challenge"
    __table_args__ = (
        UniqueConstraint("level_id", "title", name="uq_challenge_level_title"),
        UniqueConstraint("level_id", "display_order", name="uq_challenge_level_display_order"),
    )

    category_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("category.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    level_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("level.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    objectives: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    challenge_type: Mapped[ChallengeType] = mapped_column(
        Enum(ChallengeType, name="challenge_type", native_enum=False),
        nullable=False,
    )
    difficulty: Mapped[ChallengeDifficulty] = mapped_column(
        Enum(ChallengeDifficulty, name="challenge_difficulty", native_enum=False),
        nullable=False,
        default=ChallengeDifficulty.BEGINNER,
    )
    estimated_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[ChallengeStatus] = mapped_column(
        Enum(ChallengeStatus, name="challenge_status", native_enum=False),
        nullable=False,
        default=ChallengeStatus.DRAFT,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)
    base_score: Mapped[int] = mapped_column(Integer, nullable=False)
    scoring_config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    evaluation_strategy: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    unlock_config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
