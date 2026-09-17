"""add orders and order items

Revision ID: fe0aed3d0745
Revises: 4acec7345011
Create Date: 2026-09-16 13:41:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "fe0aed3d0745"
down_revision: Union[str, Sequence[str], None] = "4acec7345011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем старые внешние ключи orders.
    op.drop_constraint(
        "orders_manager_id_fkey",
        "orders",
        type_="foreignkey",
    )

    op.drop_constraint(
        "orders_payment_method_id_fkey",
        "orders",
        type_="foreignkey",
    )

    # Удаляем старые поля orders.
    op.drop_column(
        "orders",
        "status_id",
    )

    op.drop_column(
        "orders",
        "delivery_price",
    )

    op.drop_column(
        "orders",
        "manager_id",
    )

    op.drop_column(
        "orders",
        "payment_method_id",
    )

    # Добавляем новые поля orders.
    op.add_column(
        "orders",
        sa.Column(
            "restaurant_id",
            sa.Integer(),
            nullable=False,
        ),
    )

    op.add_column(
        "orders",
        sa.Column(
            "status",
            sa.String(50),
            nullable=False,
            server_default="NEW",
        ),
    )

    op.add_column(
        "orders",
        sa.Column(
            "total_price",
            sa.Numeric(10, 2),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "orders",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    # Связь заказа с рестораном.
    op.create_foreign_key(
        "orders_restaurant_id_fkey",
        "orders",
        "restaurants",
        ["restaurant_id"],
        ["id"],
    )

    # Создаём позиции заказа.
    op.create_table(
        "order_items",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "order_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "dish_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "quantity",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "price",
            sa.Numeric(10, 2),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["products.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Старые таблицы не удаляем:
    # units
    # suppliers
    # payment_methods
    # order_statuses
    # countries
    # managers
    # product_details


def downgrade() -> None:
    op.drop_table("order_items")

    op.drop_constraint(
        "orders_restaurant_id_fkey",
        "orders",
        type_="foreignkey",
    )

    op.drop_column(
        "orders",
        "updated_at",
    )

    op.drop_column(
        "orders",
        "total_price",
    )

    op.drop_column(
        "orders",
        "status",
    )

    op.drop_column(
        "orders",
        "restaurant_id",
    )

    op.add_column(
        "orders",
        sa.Column(
            "payment_method_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "orders",
        sa.Column(
            "manager_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "orders",
        sa.Column(
            "delivery_price",
            sa.Numeric(10, 2),
            nullable=True,
        ),
    )

    op.add_column(
        "orders",
        sa.Column(
            "status_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "orders_manager_id_fkey",
        "orders",
        "managers",
        ["manager_id"],
        ["id"],
    )

    op.create_foreign_key(
        "orders_payment_method_id_fkey",
        "orders",
        "payment_methods",
        ["payment_method_id"],
        ["id"],
    )