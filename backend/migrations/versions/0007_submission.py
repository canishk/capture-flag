"""add submission table

Revision ID: 0007_submission
Revises: 0006_resource
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0007_submission"
down_revision: Union[str, None] = "0006_resource"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "submission",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("challenge_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("evaluation_strategy_snapshot", sa.JSON(), nullable=False),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("processing_time_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["challenge_id"], ["challenge.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "challenge_id", "attempt_number", name="uq_submission_user_challenge_attempt"
        ),
    )
    op.create_index("ix_submission_user_id", "submission", ["user_id"], unique=False)
    op.create_index("ix_submission_challenge_id", "submission", ["challenge_id"], unique=False)
    op.create_index("ix_submission_status", "submission", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_submission_status", table_name="submission")
    op.drop_index("ix_submission_challenge_id", table_name="submission")
    op.drop_index("ix_submission_user_id", table_name="submission")
    op.drop_table("submission")
