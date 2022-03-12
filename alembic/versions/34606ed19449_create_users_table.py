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
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')
