"""create clicks table

Revision ID: 001
Revises:
Create Date: 2026-03-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "clicks",
        sa.Column("id", sa.Uuid, primary_key=True),
        sa.Column("url_id", sa.String(36), nullable=False, index=True),
        sa.Column("short_code", sa.String(20), nullable=False, index=True),
        sa.Column("ip_address", sa.String(45), nullable=False),
        sa.Column("user_agent", sa.String(1024), server_default=""),
        sa.Column("referrer", sa.String(2048), server_default=""),
        sa.Column("clicked_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("clicks")
