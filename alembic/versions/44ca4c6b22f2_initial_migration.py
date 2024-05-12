"""Initial migration

Revision ID: 44ca4c6b22f2
Revises: 
Create Date: 2024-05-12 15:51:56.477716

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.config import settings


# revision identifiers, used by Alembic.
revision: str = "44ca4c6b22f2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "transaction",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("userid", sa.String(length=128), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(),
            default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=128), nullable=False),
        sa.Column("offer_id", sa.Integer(), nullable=False),
        sa.Column("nationality", sa.String(length=128), nullable=False),
        schema=settings.SCHEMA_NAME,
    )


def downgrade() -> None:
    op.drop_table("transaction", schema=settings.SCHEMA_NAME)
