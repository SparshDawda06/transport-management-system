"""Create phone book system

Revision ID: create_phonebook_system
Revises: e876916215e1
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_phonebook_system'
down_revision = 'e876916215e1'
branch_labels = None
depends_on = None


def upgrade():
    # Create phone_book table
    op.create_table('phone_book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=32), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('phone_number', sa.String(length=32), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=True),
        sa.Column('label', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_phone_entity', 'phone_book', ['entity_type', 'entity_id'], unique=False)
    op.create_index(op.f('ix_phone_book_entity_id'), 'phone_book', ['entity_id'], unique=False)
    op.create_index(op.f('ix_phone_book_entity_type'), 'phone_book', ['entity_type'], unique=False)
    op.create_index(op.f('ix_phone_book_phone_number'), 'phone_book', ['phone_number'], unique=True)
    op.create_index(op.f('ix_phone_book_is_primary'), 'phone_book', ['is_primary'], unique=False)
    op.create_index(op.f('ix_phone_book_label'), 'phone_book', ['label'], unique=False)
    
    # Add unique constraint for primary phone per entity
    op.create_unique_constraint('uq_primary_phone', 'phone_book', ['entity_type', 'entity_id', 'is_primary'])


def downgrade():
    # Drop phone_book table
    op.drop_constraint('uq_primary_phone', 'phone_book', type_='unique')
    op.drop_index(op.f('ix_phone_book_label'), table_name='phone_book')
    op.drop_index(op.f('ix_phone_book_is_primary'), table_name='phone_book')
    op.drop_index(op.f('ix_phone_book_phone_number'), table_name='phone_book')
    op.drop_index(op.f('ix_phone_book_entity_type'), table_name='phone_book')
    op.drop_index(op.f('ix_phone_book_entity_id'), table_name='phone_book')
    op.drop_index('ix_phone_entity', table_name='phone_book')
    op.drop_table('phone_book')
