"""Create concerned persons and update phone book system

Revision ID: create_concerned_persons_and_phonebook_update
Revises: create_phonebook_system
Create Date: 2024-01-01 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'create_concerned_persons_and_phonebook_update'
down_revision = 'create_phonebook_system'
branch_labels = None
depends_on = None


def upgrade():
    # Drop old phone_book constraints and columns
    op.drop_constraint('uq_primary_phone', 'phone_book', type_='unique')
    op.drop_index('ix_phone_entity', table_name='phone_book')
    op.drop_column('phone_book', 'entity_type')
    op.drop_column('phone_book', 'entity_id')
    
    # Create concerned_persons table
    op.create_table('concerned_persons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=32), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('designation', sa.String(length=128), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_concerned_entity', 'concerned_persons', ['entity_type', 'entity_id'], unique=False)
    op.create_index(op.f('ix_concerned_persons_entity_id'), 'concerned_persons', ['entity_id'], unique=False)
    op.create_index(op.f('ix_concerned_persons_entity_type'), 'concerned_persons', ['entity_type'], unique=False)
    op.create_index(op.f('ix_concerned_persons_is_primary'), 'concerned_persons', ['is_primary'], unique=False)
    op.create_unique_constraint('uq_primary_concerned', 'concerned_persons', ['entity_type', 'entity_id', 'is_primary'])
    
    # Add concerned_person_id to phone_book
    op.add_column('phone_book', sa.Column('concerned_person_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_phone_book_concerned_person', 'phone_book', 'concerned_persons', ['concerned_person_id'], ['id'], ondelete='CASCADE')
    op.create_unique_constraint('uq_primary_phone_per_person', 'phone_book', ['concerned_person_id', 'is_primary'])


def downgrade():
    # Remove concerned_person_id from phone_book
    op.drop_constraint('uq_primary_phone_per_person', 'phone_book', type_='unique')
    op.drop_constraint('fk_phone_book_concerned_person', 'phone_book', type_='foreignkey')
    op.drop_column('phone_book', 'concerned_person_id')
    
    # Add back old phone_book columns
    op.add_column('phone_book', sa.Column('entity_type', sa.String(length=32), nullable=False))
    op.add_column('phone_book', sa.Column('entity_id', sa.Integer(), nullable=False))
    op.create_index('ix_phone_entity', 'phone_book', ['entity_type', 'entity_id'], unique=False)
    op.create_unique_constraint('uq_primary_phone', 'phone_book', ['entity_type', 'entity_id', 'is_primary'])
    
    # Drop concerned_persons table
    op.drop_constraint('uq_primary_concerned', 'concerned_persons', type_='unique')
    op.drop_index(op.f('ix_concerned_persons_is_primary'), table_name='concerned_persons')
    op.drop_index(op.f('ix_concerned_persons_entity_type'), table_name='concerned_persons')
    op.drop_index(op.f('ix_concerned_persons_entity_id'), table_name='concerned_persons')
    op.drop_index('ix_concerned_entity', table_name='concerned_persons')
    op.drop_table('concerned_persons')
