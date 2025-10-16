"""merge heads

Revision ID: a26df6dacb6b
Revises: b6c50de5cd04, create_concerned_persons_and_phonebook_update
Create Date: 2025-10-13 13:10:54.720619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a26df6dacb6b'
down_revision = ('b6c50de5cd04', 'create_concerned_persons_and_phonebook_update')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
