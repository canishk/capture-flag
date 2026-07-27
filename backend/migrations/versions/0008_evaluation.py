"""add evaluation table

Revision ID: 0008_evaluation
Revises: 0007_submission
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0008_evaluation"
down_revision: Union[str, None] = "0007_submission"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "evaluation",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("submission_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("challenge_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("strategy_type", sa.String(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("feedback", sa.Text(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("processing_time_ms", sa.Integer(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["submission_id"], ["submission.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["challenge_id"], ["challenge.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("submission_id", name="uq_evaluation_submission_id"),
    )
    op.create_index("ix_evaluation_submission_id", "evaluation", ["submission_id"], unique=False)
    op.create_index("ix_evaluation_user_id", "evaluation", ["user_id"], unique=False)
    op.create_index("ix_evaluation_challenge_id", "evaluation", ["challenge_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_evaluation_challenge_id", table_name="evaluation")
    op.drop_index("ix_evaluation_user_id", table_name="evaluation")
    op.drop_index("ix_evaluation_submission_id", table_name="evaluation")
    op.drop_table("evaluation")
