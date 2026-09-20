"""rename products to dishes

Revision ID: 9460b586f086
Revises: 061c04b0a86e
Create Date: 2026-09-20

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9460b586f086"
down_revision: Union[str, Sequence[str], None] = "061c04b0a86e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "order_items_dish_id_fkey",
        "order_items",
        type_="foreignkey",
    )

    op.rename_table("products", "dishes")

    op.create_foreign_key(
        "order_items_dish_id_fkey",
        "order_items",
        "dishes",
        ["dish_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "order_items_dish_id_fkey",
        "order_items",
        type_="foreignkey",
    )

    op.rename_table("dishes", "products")

    op.create_foreign_key(
        "order_items_dish_id_fkey",
        "order_items",
        "products",
        ["dish_id"],
        ["id"],
    )