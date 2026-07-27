from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import JSON, Boolean, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.evaluations.domain.enums import EvaluationStatus, EvaluationStrategyType
from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class EvaluationModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "evaluation"
    __table_args__ = (UniqueConstraint("submission_id", name="uq_evaluation_submission_id"),)

    submission_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("submission.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    challenge_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("challenge.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    strategy_type: Mapped[EvaluationStrategyType] = mapped_column(
        Enum(EvaluationStrategyType, name="evaluation_strategy_type", native_enum=False),
        nullable=False,
    )
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    feedback: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[EvaluationStatus] = mapped_column(
        Enum(EvaluationStatus, name="evaluation_status", native_enum=False),
        nullable=False,
    )
    processing_time_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, nullable=False, default=dict)
