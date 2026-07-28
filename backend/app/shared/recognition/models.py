from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base


class ProcessedRecognitionEventModel(Base):
    __tablename__ = "processed_recognition_event"
    __table_args__ = (
        UniqueConstraint("consumer", "event_id", name="uq_processed_recognition_event"),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    consumer: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    event_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    processed_at: Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(UTC))
