"""Create user balance

Revision ID: ae664610dec2
Revises: 76685d2b5bb5
Create Date: 2019-11-27 16:29:19.879093

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.types import Integer, Float

# revision identifiers, used by Alembic.
revision = 'ae664610dec2'
down_revision = '76685d2b5bb5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('foodie_user', sa.Column('cash_balance', sa.Float))
    op.add_column('foodie_user', sa.Column('favor_balance', sa.Float))

    f_users = table('foodie_user',
                    column('id', Integer),
                    column('cash_balance', Float),
                    column('favor_balance', Float),
                    )
    op.execute(f_users.update().values(cash_balance=0, favor_balance=0))


def downgrade():
    op.drop_column('foodie_user', 'cash_balance')
    op.drop_column('foodie_user', 'favor_balance')
