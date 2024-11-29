"""empty message

Revision ID: e8fa8ede44dc
Revises: 5b430461ffd7
Create Date: 2024-11-25 09:21:58.667151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8fa8ede44dc'
down_revision: Union[str, None] = '5b430461ffd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'product', 'category', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'category_id')
    # ### end Alembic commands ###
