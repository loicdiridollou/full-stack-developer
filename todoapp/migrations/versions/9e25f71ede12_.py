"""empty message

Revision ID: 9e25f71ede12
Revises: 
Create Date: 2020-05-29 18:36:54.325317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e25f71ede12'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('table1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('table1',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('descirption', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='table1_pkey')
    )
    # ### end Alembic commands ###
