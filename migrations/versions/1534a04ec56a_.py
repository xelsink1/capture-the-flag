"""empty message

Revision ID: 1534a04ec56a
Revises: a92e27064518
Create Date: 2021-08-09 20:11:46.780385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1534a04ec56a'
down_revision = 'a92e27064518'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
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
    op.drop_table('NewTable')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('NewTable',
    sa.Column('Column1', sa.NUMERIC(), nullable=True)
    )
    op.drop_table('user')
    # ### end Alembic commands ###