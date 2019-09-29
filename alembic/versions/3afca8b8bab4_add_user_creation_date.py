"""Add user creation date

Revision ID: 3afca8b8bab4
Revises: 599d89654c3a
Create Date: 2019-09-22 13:35:56.229639

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '3afca8b8bab4'
down_revision = '599d89654c3a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('foodie_user', sa.Column('creation_date', sa.DateTime))
    f_users = sa.Table('foodie_user',
                       sa.MetaData(),
                       sa.Column('id'),
                       sa.Column('creation_date'))
    conn = op.get_bind()
    conn.execute(f_users.update().values(creation_date=datetime.utcnow()))


def downgrade():
    op.drop_column('foodie_user', 'creation_date')
