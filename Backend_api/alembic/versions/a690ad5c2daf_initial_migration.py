"""Initial migration

Revision ID: a690ad5c2daf
Revises: 
Create Date: 2024-11-03 10:34:55.763872

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a690ad5c2daf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new UUID column
    op.add_column('users', sa.Column('new_id', sa.UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')))
    
    # Optionally: Populate new_id with unique values (if gen_random_uuid() is not used)
    # connection = op.get_bind()
    # connection.execute(sa.text("UPDATE users SET new_id = gen_random_uuid()"))
    
    # Drop the old integer ID column
    op.drop_column('users', 'id')
    
    # Rename the new_id to id
    op.alter_column('users', 'new_id', new_column_name='id', existing_type=sa.UUID(), existing_nullable=False)


def downgrade() -> None:
    # Add back the old integer column
    op.add_column('users', sa.Column('id', sa.INTEGER(), nullable=False))

    # Optionally: Populate the old id column if necessary
    # connection = op.get_bind()
    # connection.execute(sa.text("UPDATE users SET id = ..."))  # logic to regenerate ids

    # Drop the new UUID column
    op.drop_column('users', 'new_id')
