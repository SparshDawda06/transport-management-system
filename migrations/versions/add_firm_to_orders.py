"""add firm to orders

Revision ID: add_firm_to_orders
Revises: 978eeaca3f79
Create Date: 2025-10-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_firm_to_orders'
down_revision = '978eeaca3f79'
branch_labels = None
depends_on = None


def upgrade():
    # Add firm column to orders table
    op.add_column('orders', sa.Column('firm', sa.String(length=255), nullable=False, server_default='New Jalaram Transport Service'))


def downgrade():
    # Remove firm column from orders table
    op.drop_column('orders', 'firm')

