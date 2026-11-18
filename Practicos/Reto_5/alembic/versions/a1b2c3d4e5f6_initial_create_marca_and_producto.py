"""Initial: Create Marca and Producto

Revision ID: a1b2c3d4e5f6
Revises: 
Create Date: 2026-09-24 22:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlmodel
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('marca',
    sa.Column('nombre', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('pais', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('producto',
    sa.Column('nombre', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('precio', sa.Float(), nullable=False),
    sa.Column('activo', sa.Boolean(), nullable=False),
    sa.Column('marca_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['marca_id'], ['marca.id'], name='fk_producto_marca_id'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('producto')
    op.drop_table('marca')
