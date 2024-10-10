"""create posts table

Revision ID: 2b87bc81d393
Revises: 
Create Date: 2024-10-07 23:39:28.555456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b87bc81d393'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posters',sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title',sa.String(), nullable = False))
    pass
  


def downgrade():
    op.drop_table('posters')
    pass
