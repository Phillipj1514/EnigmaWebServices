"""empty message

Revision ID: d924d05be254
Revises: 514be2c7ed85
Create Date: 2020-05-29 15:55:12.792961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd924d05be254'
down_revision = '514be2c7ed85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('merchantID', sa.Integer(), nullable=True),
    sa.Column('queue', sa.Text(), nullable=True),
    sa.Column('waitTime', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('merchants', sa.Column('address', sa.String(length=100), nullable=True))
    op.add_column('merchants', sa.Column('email', sa.String(length=100), nullable=True))
    op.add_column('merchants', sa.Column('estimatedWaitTime', sa.Integer(), nullable=True))
    op.add_column('merchants', sa.Column('joined_on', sa.DateTime(), nullable=True))
    op.add_column('merchants', sa.Column('location', sa.String(length=100), nullable=True))
    op.add_column('merchants', sa.Column('logo', sa.String(length=100), nullable=True))
    op.add_column('merchants', sa.Column('name', sa.String(length=100), nullable=True))
    op.add_column('merchants', sa.Column('password', sa.String(length=100), nullable=True))
    op.drop_column('merchants', 'gender')
    op.drop_column('merchants', 'last_name')
    op.drop_column('merchants', 'first_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('merchants', sa.Column('first_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('merchants', sa.Column('last_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('merchants', sa.Column('gender', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.drop_column('merchants', 'password')
    op.drop_column('merchants', 'name')
    op.drop_column('merchants', 'logo')
    op.drop_column('merchants', 'location')
    op.drop_column('merchants', 'joined_on')
    op.drop_column('merchants', 'estimatedWaitTime')
    op.drop_column('merchants', 'email')
    op.drop_column('merchants', 'address')
    op.drop_table('lines')
    # ### end Alembic commands ###