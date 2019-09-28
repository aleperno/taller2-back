"""Add photo_url column

Revision ID: d74347cb7438
Revises: 3afca8b8bab4
Create Date: 2019-09-28 12:34:22.314742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd74347cb7438'
down_revision = '3afca8b8bab4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('foodie_user', sa.Column('photo_url', sa.VARCHAR))


def downgrade():
    op.drop_column('foodie_user', 'photo_url')
