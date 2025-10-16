"""add rate, phonebook, and agent station

Revision ID: add_rate_phonebook_agent_station  
Revises: add_order_type_and_stations
Create Date: 2025-10-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_rate_phonebook_agent_station'
down_revision = 'add_order_type_and_stations'
branch_labels = None
depends_on = None


def upgrade():
    # Add rate to orders
    op.add_column('orders', sa.Column('rate', sa.Float(), nullable=True))
    
    # Add station_id to booking_agents
    op.add_column('booking_agents', sa.Column('station_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_booking_agents_station', 'booking_agents', 'stations', ['station_id'], ['id'], ondelete='SET NULL')
    
    # Create phone_book table
    op.create_table('phone_book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=32), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('phone_number', sa.String(length=32), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_phone_entity', 'phone_book', ['entity_type', 'entity_id'])
    op.create_index(op.f('ix_phone_book_entity_type'), 'phone_book', ['entity_type'])


def downgrade():
    op.drop_index(op.f('ix_phone_book_entity_type'), table_name='phone_book')
    op.drop_index('ix_phone_entity', table_name='phone_book')
    op.drop_table('phone_book')
    op.drop_constraint('fk_booking_agents_station', 'booking_agents', type_='foreignkey')
    op.drop_column('booking_agents', 'station_id')
    op.drop_column('orders', 'rate')

