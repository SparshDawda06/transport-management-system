"""add order type and from/to stations

Revision ID: add_order_type_and_stations
Revises: add_firm_to_orders
Create Date: 2025-10-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_order_type_and_stations'
down_revision = 'add_firm_to_orders'
branch_labels = None
depends_on = None


def upgrade():
    # Add order_type column
    op.add_column('orders', sa.Column('order_type', sa.String(length=32), nullable=False, server_default='PARTY'))
    
    # Add from_station_id and to_station_id
    op.add_column('orders', sa.Column('from_station_id', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('to_station_id', sa.Integer(), nullable=True))
    
    # Add foreign key constraints
    op.create_foreign_key('fk_orders_from_station', 'orders', 'stations', ['from_station_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('fk_orders_to_station', 'orders', 'stations', ['to_station_id'], ['id'], ondelete='RESTRICT')
    
    # Make consignor_id and consignee_id nullable (since AGENT orders won't have them)
    op.alter_column('orders', 'consignor_id', nullable=True, existing_type=sa.Integer())
    op.alter_column('orders', 'consignee_id', nullable=True, existing_type=sa.Integer())
    op.alter_column('orders', 'station_id', nullable=True, existing_type=sa.Integer())


def downgrade():
    op.drop_constraint('fk_orders_from_station', 'orders', type_='foreignkey')
    op.drop_constraint('fk_orders_to_station', 'orders', type_='foreignkey')
    op.drop_column('orders', 'to_station_id')
    op.drop_column('orders', 'from_station_id')
    op.drop_column('orders', 'order_type')
    op.alter_column('orders', 'consignor_id', nullable=False, existing_type=sa.Integer())
    op.alter_column('orders', 'consignee_id', nullable=False, existing_type=sa.Integer())
    op.alter_column('orders', 'station_id', nullable=False, existing_type=sa.Integer())

