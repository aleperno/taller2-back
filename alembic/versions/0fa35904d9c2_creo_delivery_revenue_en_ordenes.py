"""Creo 'delivery_revenue' en ordenes

Revision ID: 0fa35904d9c2
Revises: b2c55745a650
Create Date: 2019-12-01 12:44:28.482462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fa35904d9c2'
down_revision = 'b2c55745a650'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('delivery_revenue', sa.Float))


def downgrade():
    op.drop_column('orders', 'delivery_revenue')
