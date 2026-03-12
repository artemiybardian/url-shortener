"""add country to clicks

Revision ID: 002
Revises: 001
Create Date: 2026-03-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: str | None = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("clicks", sa.Column("country", sa.String(2), server_default=""))


def downgrade() -> None:
    op.drop_column("clicks", "country")
