"""add str type to 'is_correct'

Revision ID: 7f4a94583803
Revises: cf48bcd91367
Create Date: 2025-06-11 21:02:55.703789

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7f4a94583803"
down_revision: Union[str, None] = "cf48bcd91367"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "options",
        "is_correct",
        type_=sa.JSON,
        postgresql_using="is_correct::text::json",  # Преобразование через текст
        nullable=False,
    )


def downgrade():
    op.alter_column(
        "options",
        "is_correct",
        type_=sa.Boolean,
        postgresql_using="is_correct::boolean",  # Обратное преобразование
        nullable=False,
    )
