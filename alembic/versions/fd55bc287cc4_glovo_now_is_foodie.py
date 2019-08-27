"""Glovo now is Foodie

Revision ID: fd55bc287cc4
Revises: cfe2936efc9a
Create Date: 2019-08-26 20:38:11.480886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd55bc287cc4'
down_revision = 'cfe2936efc9a'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('glovo_user', 'foodie_user')
    op.rename_table('glovo_user_id_seq', 'foodie_user_id_seq')


def downgrade():
    op.rename_table('foodie_user', 'glovo_user')
    op.rename_table('foodie_user_id_seq', 'glovo_user_id_seq')
