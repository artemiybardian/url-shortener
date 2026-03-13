"""make user_id nullable"""

revision = "002"
down_revision = "001"

from alembic import op


def upgrade() -> None:
    op.alter_column("urls", "user_id", nullable=True)


def downgrade() -> None:
    op.alter_column("urls", "user_id", nullable=False)
