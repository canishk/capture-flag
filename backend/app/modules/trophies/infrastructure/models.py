from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, Boolean, Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.trophies.domain.enums import TrophyTriggerType
from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class TrophyDefinitionModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "trophy_definition"

    code: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str] = mapped_column(String(80), nullable=False)
    trigger_type: Mapped[TrophyTriggerType] = mapped_column(
        Enum(TrophyTriggerType, name="trophy_trigger_type", native_enum=False),
        nullable=False,
        index=True,
    )
    criteria: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    is_repeatable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)


class TrophyAwardModel(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "trophy_award"
    __table_args__ = (
        UniqueConstraint("trophy_id", "user_id", name="uq_trophy_award_user"),
    )

    trophy_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("trophy_definition.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_event_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    awarded_at: Mapped[datetime] = mapped_column(nullable=False)
