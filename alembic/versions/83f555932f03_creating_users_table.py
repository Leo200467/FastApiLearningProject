"""creating users table

Revision ID: 83f555932f03
Revises: 0882548113d6
Create Date: 2021-12-30 20:46:24.607893

"""
from alembic import op
import sqlalchemy as sa

from app.models import Items, Users

# revision identifiers, used by Alembic.
revision = '83f555932f03'
down_revision = '0882548113d6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
        )
    pass


def downgrade():
    op.drop_table('users')
    pass
