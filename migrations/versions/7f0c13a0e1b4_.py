"""empty message

Revision ID: 7f0c13a0e1b4
Revises: 
Create Date: 2021-08-13 12:46:04.130674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f0c13a0e1b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('base',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.Column('color', sa.String(length=8), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bullet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.Column('side', sa.String(length=6), nullable=True),
    sa.Column('speed', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('object',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=100), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=32), nullable=True),
    sa.Column('code', sa.Text(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=False),
    sa.Column('bullets', sa.Integer(), nullable=False),
    sa.Column('has_flag', sa.Boolean(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.Column('side', sa.String(length=6), nullable=True),
    sa.Column('inventory', sa.JSON(), nullable=True),
    sa.Column('base_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['base_id'], ['base.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player')
    op.drop_table('users')
    op.drop_table('object')
    op.drop_table('bullet')
    op.drop_table('base')
    # ### end Alembic commands ###
