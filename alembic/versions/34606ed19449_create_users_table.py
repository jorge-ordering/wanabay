"""create_users_table

Revision ID: 34606ed19449
Revises:
Create Date: 2022-03-12 21:57:11.205452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34606ed19449'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True,unique=True),
        sa.Column('username', sa.String(100), unique=True),
        sa.Column('hashed_password', sa.String(100)),
        sa.Column('email', sa.String(200)),
        sa.Column('enabled', sa.Boolean),
        sa.Column('created_at', sa.DateTime)
    )

def downgrade():
    op.drop_table('users')
