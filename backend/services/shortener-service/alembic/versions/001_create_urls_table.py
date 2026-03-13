"""create urls table

Revision ID: 001
Revises:
Create Date: 2026-03-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "urls",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("short_code", sa.String(20), unique=True, nullable=False, index=True),
        sa.Column("original_url", sa.String(2048), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("urls")
