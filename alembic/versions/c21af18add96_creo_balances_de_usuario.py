"""Creo balances de usuario

Revision ID: c21af18add96
Revises: 556dc8dd6fec
Create Date: 2019-11-30 13:24:35.591737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c21af18add96'
down_revision = '556dc8dd6fec'
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
