"""Adding sp500 data and migration

Revision ID: 4cfcb116dbd5
Revises: a509bc8a7f80
Create Date: 2024-04-27 18:42:53.393758

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import csv
from sqlalchemy.sql import table, column
from sqlalchemy import String, Float, BigInteger

# revision identifiers, used by Alembic.
revision = "4cfcb116dbd5"
down_revision = "a509bc8a7f80"
branch_labels = None
depends_on = None


def upgrade():
    pass
    # Add user_id column to the existing stock table
    # op.add_column(
    #     "stock",
    #     sa.Column(
    #         "user_id",
    #         sa.Integer,
    #         sa.ForeignKey("user.id", ondelete="CASCADE"),
    #         nullable=False,
    #     ),
    # )


def downgrade():
    pass
    # # Drop the user_id column from the stock table
    # op.drop_column("stock", "user_id")
