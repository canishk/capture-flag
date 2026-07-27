from __future__ import annotations

from sqlalchemy import Enum, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.categories.domain.enums import CategoryStatus
from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CategoryModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "category"
    __table_args__ = (UniqueConstraint("name", name="uq_category_name"),)

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(120), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    status: Mapped[CategoryStatus] = mapped_column(
        Enum(CategoryStatus, name="category_status", native_enum=False),
        nullable=False,
        default=CategoryStatus.ACTIVE,
        index=True,
    )
