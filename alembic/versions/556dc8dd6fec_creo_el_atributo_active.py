"""Creo el atributo 'active'

Revision ID: 556dc8dd6fec
Revises: 129bdbf1bdc1
Create Date: 2019-11-29 21:16:13.255908

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.types import Integer, Float, Boolean


# revision identifiers, used by Alembic.
revision = '556dc8dd6fec'
down_revision = '129bdbf1bdc1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('foodie_user', sa.Column('active', sa.Boolean))
    op.add_column('foodie_shop', sa.Column('active', sa.Boolean))
    op.add_column('product', sa.Column('active', sa.Boolean))

    users = table('foodie_user', column('id', Integer), column('active', Boolean))
    shops = table('foodie_shop', column('id', Integer), column('active', Boolean))
    products = table('product', column('id', Integer), column('active', Boolean))

    op.execute(users.update().values(active=True))
    op.execute(shops.update().values(active=True))
    op.execute(products.update().values(active=True))


def downgrade():
    op.drop_column('foodie_user', 'active')
    op.drop_column('foodie_shop', 'active')
    op.drop_column('product', 'active')
