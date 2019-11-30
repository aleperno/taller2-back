"""Agrego metadata a las ordenes

Revision ID: 76685d2b5bb5
Revises: c21af18add96
Create Date: 2019-11-24 13:00:58.023989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76685d2b5bb5'
down_revision = 'c21af18add96'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('order_metadata', sa.VARCHAR))


def downgrade():
    op.drop_column('orders', 'order_metadata')
