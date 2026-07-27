"""add challenge table

Revision ID: 0004_challenge
Revises: 0003_level
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0004_challenge"
down_revision: Union[str, None] = "0003_level"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "challenge",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("level_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("objectives", sa.JSON(), nullable=False),
        sa.Column("challenge_type", sa.String(), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=False),
        sa.Column("estimated_duration_minutes", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("base_score", sa.Integer(), nullable=False),
        sa.Column("scoring_config", sa.JSON(), nullable=False),
        sa.Column("evaluation_strategy", sa.JSON(), nullable=False),
        sa.Column("unlock_config", sa.JSON(), nullable=False),
        sa.Column("is_required", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["category.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["level_id"], ["level.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("level_id", "title", name="uq_challenge_level_title"),
        sa.UniqueConstraint("level_id", "display_order", name="uq_challenge_level_display_order"),
    )
    op.create_index("ix_challenge_category_id", "challenge", ["category_id"], unique=False)
    op.create_index("ix_challenge_level_id", "challenge", ["level_id"], unique=False)
    op.create_index("ix_challenge_status", "challenge", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_challenge_status", table_name="challenge")
    op.drop_index("ix_challenge_level_id", table_name="challenge")
    op.drop_index("ix_challenge_category_id", table_name="challenge")
    op.drop_table("challenge")
