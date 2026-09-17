"""add restaurant_id to categories

Revision ID: 49dce3c22e2e
Revises:
Create Date: 2026-09-09 20:27:07.717986
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "49dce3c22e2e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "categories",
        sa.Column(
            "restaurant_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_categories_restaurant_id",
        "categories",
        "restaurants",
        ["restaurant_id"],
        ["id"],
    )

    op.create_unique_constraint(
        "uq_category_restaurant_name",
        "categories",
        ["restaurant_id", "name"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_category_restaurant_name",
        "categories",
        type_="unique",
    )

    op.drop_constraint(
        "fk_categories_restaurant_id",
        "categories",
        type_="foreignkey",
    )

    op.drop_column(
        "categories",
        "restaurant_id",
    )