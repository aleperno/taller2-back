"""Agrego address a las ordenes

Revision ID: 88fe7441b5c7
Revises: 0fa35904d9c2
Create Date: 2019-12-04 19:01:00.993184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88fe7441b5c7'
down_revision = '0fa35904d9c2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('address', sa.String))


def downgrade():
    op.drop_column('orders', 'address')
