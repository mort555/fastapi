"""convert products to dishes

Revision ID: 8a3a756a2cfe
Revises: b01185f8e05c
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8a3a756a2cfe"
down_revision: Union[str, Sequence[str], None] = "b01185f8e05c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column(
            "restaurant_id",
            sa.Integer(),
            nullable=False,
        ),
    )

    op.add_column(
        "products",
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "products",
        sa.Column(
            "is_available",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    op.add_column(
        "products",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.alter_column(
        "products",
        "weight",
        existing_type=sa.Numeric(),
        type_=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "products",
        "price",
        existing_type=sa.Numeric(),
        type_=sa.Numeric(10, 2),
        nullable=False,
    )

    op.create_foreign_key(
        "fk_products_restaurant_id",
        "products",
        "restaurants",
        ["restaurant_id"],
        ["id"],
    )

    op.drop_column("products", "sku")
    op.drop_column("products", "stock")
    op.drop_column("products", "supplier_id")
    op.drop_column("products", "cost_price")
    op.drop_column("products", "unit_id")


def downgrade() -> None:
    op.add_column(
        "products",
        sa.Column(
            "unit_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "products",
        sa.Column(
            "cost_price",
            sa.Numeric(),
            nullable=True,
        ),
    )

    op.add_column(
        "products",
        sa.Column(
            "supplier_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "products",
        sa.Column(
            "stock",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "products",
        sa.Column(
            "sku",
            sa.String(100),
            nullable=True,
        ),
    )

    op.drop_constraint(
        "fk_products_restaurant_id",
        "products",
        type_="foreignkey",
    )

    op.alter_column(
        "products",
        "price",
        existing_type=sa.Numeric(10, 2),
        type_=sa.Numeric(),
    )

    op.alter_column(
        "products",
        "weight",
        existing_type=sa.Integer(),
        type_=sa.Numeric(),
        nullable=True,
    )

    op.drop_column("products", "updated_at")
    op.drop_column("products", "is_available")
    op.drop_column("products", "description")
    op.drop_column("products", "restaurant_id")