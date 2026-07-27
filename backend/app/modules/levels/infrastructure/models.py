from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import JSON, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.levels.domain.enums import LevelStatus
from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class LevelModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "level"
    __table_args__ = (
        UniqueConstraint("category_id", "display_order", name="uq_level_category_display_order"),
    )

    category_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("category.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[LevelStatus] = mapped_column(
        Enum(LevelStatus, name="level_status", native_enum=False),
        nullable=False,
        default=LevelStatus.ACTIVE,
        index=True,
    )
    unlock_config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
