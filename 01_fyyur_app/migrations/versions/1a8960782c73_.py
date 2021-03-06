"""empty message

Revision ID: 1a8960782c73
Revises: 51df084b602d
Create Date: 2020-06-01 10:14:05.288068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a8960782c73'
down_revision = '51df084b602d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.drop_column('artist', 'seeking_msg')
    op.add_column('venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('venue', sa.Column('website_link', sa.String(length=500), nullable=True))
    op.drop_column('venue', 'seeking_message')
    op.drop_column('venue', 'web_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('web_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('venue', sa.Column('seeking_message', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('venue', 'website_link')
    op.drop_column('venue', 'seeking_description')
    op.add_column('artist', sa.Column('seeking_msg', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('artist', 'seeking_description')
    # ### end Alembic commands ###
