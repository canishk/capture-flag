"""add resource and challenge_resource tables

Revision ID: 0006_resource
Revises: 0005_hint
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006_resource"
down_revision: Union[str, None] = "0005_hint"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "resource",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("resource_type", sa.String(), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=True),
        sa.Column("file_path", sa.String(length=500), nullable=True),
        sa.Column("author", sa.String(length=200), nullable=True),
        sa.Column("source", sa.String(length=200), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_resource_resource_type", "resource", ["resource_type"], unique=False)
    op.create_index("ix_resource_status", "resource", ["status"], unique=False)

    op.create_table(
        "challenge_resource",
        sa.Column("challenge_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["challenge_id"], ["challenge.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["resource_id"], ["resource.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("challenge_id", "resource_id"),
    )


def downgrade() -> None:
    op.drop_table("challenge_resource")
    op.drop_index("ix_resource_status", table_name="resource")
    op.drop_index("ix_resource_resource_type", table_name="resource")
    op.drop_table("resource")
