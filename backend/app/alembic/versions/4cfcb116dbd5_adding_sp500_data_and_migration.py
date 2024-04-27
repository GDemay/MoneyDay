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
csv_file_path = "app/alembic/data/constituents-financials.csv"


def upgrade():
    op.create_table(
        "constituents",
        sa.Column("Symbol", sa.String(length=10), primary_key=True),
        sa.Column("Name", sa.String(length=255), nullable=False),
        sa.Column("Sector", sa.String(length=100), nullable=False),
        sa.Column("Price", sa.Float, nullable=False),
        sa.Column("Price_Earnings", sa.Float, nullable=True),
        sa.Column("Dividend_Yield", sa.Float, nullable=True),
        sa.Column("Earnings_Share", sa.Float, nullable=True),
        sa.Column("Week_Low_52", sa.Float, nullable=True),
        sa.Column("Week_High_52", sa.Float, nullable=True),
        sa.Column("Market_Cap", sa.BigInteger, nullable=True),
        sa.Column("EBITDA", sa.BigInteger, nullable=True),
        sa.Column("Price_Sales", sa.Float, nullable=True),
        sa.Column("Price_Book", sa.Float, nullable=True),
        sa.Column("SEC_Filings", sa.String(length=255), nullable=True),
    )
    # Define the table
    companies_table = table(
        "constituents",
        column("Symbol", String),
        column("Name", String),
        column("Sector", String),
        column("Price", Float),
        column("Price_Earnings", Float),
        column("Dividend_Yield", Float),
        column("Earnings_Share", Float),
        column("Week_Low_52", Float),
        column("Week_High_52", Float),
        column("Market_Cap", BigInteger),
        column("EBITDA", BigInteger),
        column("Price_Sales", Float),
        column("Price_Book", Float),
        column("SEC_Filings", String),
    )

    # Read data from CSV
    with open(csv_file_path, "r") as file:
        data = csv.DictReader(file)
        op.bulk_insert(
            companies_table, [{key: row[key] for key in row} for row in data]
        )


def downgrade():
    op.drop_table("constituents")
