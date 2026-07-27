"""add hint table

Revision ID: 0005_hint
Revises: 0004_challenge
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0005_hint"
down_revision: Union[str, None] = "0004_challenge"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hint",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("challenge_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("penalty_config", sa.JSON(), nullable=False),
        sa.Column("unlock_config", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["challenge_id"], ["challenge.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("challenge_id", "display_order", name="uq_hint_challenge_display_order"),
    )
    op.create_index("ix_hint_challenge_id", "hint", ["challenge_id"], unique=False)
    op.create_index("ix_hint_status", "hint", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_hint_status", table_name="hint")
    op.drop_index("ix_hint_challenge_id", table_name="hint")
    op.drop_table("hint")
