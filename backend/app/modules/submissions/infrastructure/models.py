from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import JSON, Enum, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.submissions.domain.enums import SubmissionStatus
from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class SubmissionModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "submission"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "challenge_id", "attempt_number", name="uq_submission_user_challenge_attempt"
        ),
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
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[SubmissionStatus] = mapped_column(
        Enum(SubmissionStatus, name="submission_status", native_enum=False),
        nullable=False,
        default=SubmissionStatus.PENDING,
        index=True,
    )
    evaluation_strategy_snapshot: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    @property
    def submitted_at(self):
        return self.created_at
