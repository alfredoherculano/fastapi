"""add content column to posts table

Revision ID: 26b155016a23
Revises: f7485664fae7
Create Date: 2024-01-24 12:01:37.887373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26b155016a23'
down_revision: Union[str, None] = 'f7485664fae7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
