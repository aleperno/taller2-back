"""Add status column for users

Revision ID: 32812fba1973
Revises: d74347cb7438
Create Date: 2019-10-27 02:27:10.561771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32812fba1973'
down_revision = 'd74347cb7438'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('foodie_user', sa.Column('status', sa.String))
    f_users = sa.Table('foodie_user',
                       sa.MetaData(),
                       sa.Column('id'),
                       sa.Column('status'))
    conn = op.get_bind()
    conn.execute(f_users.update().values(status='active'))


def downgrade():
    op.drop_column('foodie_user', 'status')
