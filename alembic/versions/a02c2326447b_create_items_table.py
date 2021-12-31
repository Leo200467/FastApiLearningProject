"""create items table

Revision ID: a02c2326447b
Revises: 
Create Date: 2021-12-30 16:48:09.127845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a02c2326447b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('items', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False)
        )
    pass


def downgrade():
    op.drop_table('items')
    pass
