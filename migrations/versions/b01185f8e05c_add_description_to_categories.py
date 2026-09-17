"""add description to categories

Revision ID: b01185f8e05c
Revises: 49dce3c22e2e
Create Date: 2026-09-16 12:47:23.386313
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b01185f8e05c"
down_revision: Union[str, Sequence[str], None] = "49dce3c22e2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "categories",
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
    )

    op.alter_column(
        "categories",
        "restaurant_id",
        existing_type=sa.Integer(),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "categories",
        "restaurant_id",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.drop_column(
        "categories",
        "description",
    )