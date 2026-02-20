"""make user first/last name nullable

Revision ID: 20260220_user_name_nullable
Revises: 20260220_fix_comment_media
Create Date: 2026-02-20 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260220_user_name_nullable"
down_revision: Union[str, Sequence[str], None] = "20260220_fix_comment_media"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("user", "first_name", existing_type=sa.String(length=25), nullable=True)
    op.alter_column("user", "last_name", existing_type=sa.String(length=25), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("user", "last_name", existing_type=sa.String(length=25), nullable=False)
    op.alter_column("user", "first_name", existing_type=sa.String(length=25), nullable=False)
