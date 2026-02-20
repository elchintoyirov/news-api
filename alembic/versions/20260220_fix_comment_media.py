"""fix comment media nullable

Revision ID: 20260220_fix_comment_media
Revises: 20260220_add_user_sessions_table
Create Date: 2026-02-20 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260220_fix_comment_media"
down_revision: Union[str, Sequence[str], None] = "20260220_add_user_sessions_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("comment", "media_id", existing_type=sa.BigInteger(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("comment", "media_id", existing_type=sa.BigInteger(), nullable=False)
