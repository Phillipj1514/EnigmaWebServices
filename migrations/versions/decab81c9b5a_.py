"""empty message

Revision ID: decab81c9b5a
Revises: 310cebb3909a
Create Date: 2020-05-30 02:54:18.148769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'decab81c9b5a'
down_revision = '310cebb3909a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('chatID', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customers', 'chatID')
    # ### end Alembic commands ###
