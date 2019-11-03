"""La orden puede ser un favor

Revision ID: 0e67e96bfa21
Revises: 32812fba1973
Create Date: 2019-11-02 21:51:42.693266

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '0e67e96bfa21'
down_revision = '32812fba1973'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('favor', sa.Boolean))
    op.add_column('orders', sa.Column('creation_date', sa.DateTime))
    op.add_column('orders', sa.Column('price', sa.Float))
    orders = sa.Table('orders',
                       sa.MetaData(),
                       sa.Column('id'),
                       sa.Column('favor'),
                       sa.Column('creation_date'),
                       sa.Column('price'),
                      )
    conn = op.get_bind()
    conn.execute(orders.update().values(favor=False))
    conn.execute(orders.update().values(creation_date=datetime.utcnow()))
    conn.execute(orders.update().values(price=0))

def downgrade():
    op.drop_column('orders', 'favor')
    op.drop_column('orders', 'creation_date')
    op.drop_column('price')
