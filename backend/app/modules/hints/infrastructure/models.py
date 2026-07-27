from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import JSON, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.hints.domain.enums import HintStatus
from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class HintModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "hint"
    __table_args__ = (
        UniqueConstraint("challenge_id", "display_order", name="uq_hint_challenge_display_order"),
    )

    challenge_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("challenge.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)
    penalty_config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    unlock_config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[HintStatus] = mapped_column(
        Enum(HintStatus, name="hint_status", native_enum=False),
        nullable=False,
        default=HintStatus.DRAFT,
        index=True,
    )
