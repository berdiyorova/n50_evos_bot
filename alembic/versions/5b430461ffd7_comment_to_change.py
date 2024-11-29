"""comment to change

Revision ID: 5b430461ffd7
Revises: b3140c8f3e47
Create Date: 2024-11-25 05:24:22.344560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b430461ffd7'
down_revision: Union[str, None] = 'b3140c8f3e47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('feedback_user_id_fkey', 'feedback', type_='foreignkey')
    op.create_foreign_key(None, 'feedback', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'feedback', type_='foreignkey')
    op.create_foreign_key('feedback_user_id_fkey', 'feedback', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
