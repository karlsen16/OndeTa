"""renomear_e_adicionar_colunas

Revision ID: 3ab44dbc4064
Revises: bf7c8bbc2d39
Create Date: 2026-06-12 03:22:40.801879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ab44dbc4064'
down_revision: Union[str, Sequence[str], None] = 'bf7c8bbc2d39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('posts', 'name', new_column_name='pet_name', existing_type=sa.String(100))
    op.alter_column('posts', 'type', new_column_name='pet_type', existing_type=sa.String(50))

    op.add_column('posts', sa.Column('category', sa.String(20), nullable=True))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('posts', sa.Column('updated_at', sa.DateTime(), nullable=True))

    op.execute("UPDATE posts SET category = 'perdido' WHERE category IS NULL")
    op.execute("UPDATE posts SET created_at = date WHERE created_at IS NULL")
    op.execute("UPDATE posts SET updated_at = date WHERE updated_at IS NULL")

    op.add_column('users', sa.Column('role', sa.String(20), nullable=True))
    op.add_column('users', sa.Column('status', sa.String(20), nullable=True))

    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL")
    op.execute("UPDATE users SET status = 'active' WHERE status IS NULL")

    op.alter_column('users', 'role', server_default='user', nullable=False)
    op.alter_column('users', 'status', server_default='active', nullable=False)

    op.alter_column('images', 'pet_id', new_column_name='post_id', existing_type=sa.Integer())


def downgrade():
    op.alter_column('images', 'post_id', new_column_name='pet_id', existing_type=sa.Integer())

    op.drop_column('users', 'status')
    op.drop_column('users', 'role')

    op.drop_column('posts', 'updated_at')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'category')
    op.alter_column('posts', 'pet_type', new_column_name='type', existing_type=sa.String(50))
    op.alter_column('posts', 'pet_name', new_column_name='name', existing_type=sa.String(100))