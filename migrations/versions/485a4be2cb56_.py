"""empty message

Revision ID: 485a4be2cb56
Revises: 0781d396d3cb
Create Date: 2020-02-28 22:28:26.866315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '485a4be2cb56'
down_revision = '0781d396d3cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('album', sa.Column('description', sa.String(length=500), nullable=True))
    op.drop_column('album', 'desciption')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('album', sa.Column('desciption', mysql.VARCHAR(length=500), nullable=True))
    op.drop_column('album', 'description')
    # ### end Alembic commands ###
