"""inserting description in items table

Revision ID: be41094918a3
Revises: 83f555932f03
Create Date: 2022-01-03 22:35:03.625779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be41094918a3'
down_revision = '83f555932f03'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('items', 
        sa.Column('description', sa.String(), nullable=True))
    op.add_column('items',
        sa.Column('price_with_tax', sa.Float(), nullable=False, server_default=sa.Computed('price + tax')))
    pass


def downgrade():
    op.drop_column('items', 'description')
    op.drop_column('items', 'price_with_tax')
    pass
