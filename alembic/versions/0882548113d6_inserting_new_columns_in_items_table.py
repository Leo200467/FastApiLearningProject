"""
inserting new columns in items table

Revision ID: 0882548113d6
Revises: a02c2326447b
Create Date: 2021-12-30 17:03:25.819619

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import FetchedValue


# revision identifiers, used by Alembic.
revision = '0882548113d6'
down_revision = 'a02c2326447b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('items', 
        sa.Column('tax', sa.Float(), nullable=False))
    op.add_column('items', 
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('items', 'tax')
    op.drop_column('items', 'created_at')
    pass
