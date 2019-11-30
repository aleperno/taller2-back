"""Agrego Status id a las ordenes

Revision ID: b2c55745a650
Revises: 76685d2b5bb5
Create Date: 2019-11-28 00:58:42.536334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2c55745a650'
down_revision = '76685d2b5bb5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('status_id', sa.Integer))
    op.add_column('orders', sa.Column('product_prices', sa.Float))


def downgrade():
    op.drop_column('orders, status_id')
    op.drop_column('orders, product_prices')
