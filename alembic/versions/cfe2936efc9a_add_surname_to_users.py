"""Add surname to users

Revision ID: cfe2936efc9a
Revises:
Create Date: 2019-08-25 20:11:33.963975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfe2936efc9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('glovo_user', sa.Column('surname', sa.VARCHAR))


def downgrade():
    op.drop_column('glovo_user', 'surname')
