"""Adding stock fields

Revision ID: a509bc8a7f80
Revises: e2412789c190
Create Date: 2024-04-18 20:24:57.120001

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'a509bc8a7f80'
down_revision = 'e2412789c190'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'stock',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('quantity', sa.Integer, nullable=False),
    sa.Column('purchase_price', sa.Float, nullable=False),
    sa.Column('current_price', sa.Float, nullable=True),
    sa.Column('purchase_date', sa.Date, nullable=False),
    )
    op.create_index('ix_stock_symbol', 'stock', ['symbol'], unique=False)


def downgrade():
    op.drop_index('ix_stock_symbol', table_name='stock')
    op.drop_table('stock')