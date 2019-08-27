"""Create new user fields

Revision ID: 599d89654c3a
Revises: fd55bc287cc4
Create Date: 2019-08-26 22:22:54.784076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '599d89654c3a'
down_revision = 'fd55bc287cc4'
branch_labels = None
depends_on = None

new_columns = ['phone', 'role', 'subscription']

def upgrade():
    for col in new_columns:
        op.add_column('foodie_user', sa.Column(col, sa.VARCHAR))


def downgrade():
    for col in new_columns:
        op.drop_column('foodie_user', col)
