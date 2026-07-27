"""add progress projection tables

Revision ID: 0009_progress
Revises: 0008_evaluation
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0009_progress"
down_revision: Union[str, None] = "0008_evaluation"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "learner_progress",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("total_xp", sa.Integer(), nullable=False),
        sa.Column("challenges_attempted", sa.Integer(), nullable=False),
        sa.Column("challenges_completed", sa.Integer(), nullable=False),
        sa.Column("last_active_challenge_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_table(
        "challenge_completion",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("challenge_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("level_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["challenge_id"], ["challenge.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "challenge_id"),
    )
    op.create_index("ix_challenge_completion_level_id", "challenge_completion", ["level_id"])
    op.create_index("ix_challenge_completion_category_id", "challenge_completion", ["category_id"])
    op.create_table(
        "level_completion",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("level_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["level_id"], ["level.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "level_id"),
    )
    op.create_index("ix_level_completion_category_id", "level_completion", ["category_id"])
    op.create_table(
        "category_completion",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["category_id"], ["category.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "category_id"),
    )


def downgrade() -> None:
    op.drop_table("category_completion")
    op.drop_index("ix_level_completion_category_id", table_name="level_completion")
    op.drop_table("level_completion")
    op.drop_index("ix_challenge_completion_category_id", table_name="challenge_completion")
    op.drop_index("ix_challenge_completion_level_id", table_name="challenge_completion")
    op.drop_table("challenge_completion")
    op.drop_table("learner_progress")
