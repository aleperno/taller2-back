"""Agrego delivery_id a la orden

Revision ID: 129bdbf1bdc1
Revises: 0e67e96bfa21
Create Date: 2019-11-16 12:06:06.181849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '129bdbf1bdc1'
down_revision = '0e67e96bfa21'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('delivery_id', sa.Integer))


def downgrade():
    op.drop_column('orders', 'delivery_id')
