"""add order status history

Revision ID: ed5e87a3f5aa
Revises: c96f315ad32f
Create Date: 2026-09-17 20:01:15.036964

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ed5e87a3f5aa"
down_revision: Union[str, Sequence[str], None] = "c96f315ad32f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "order_status_history",
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
            "old_status",
            sa.String(50),
            nullable=True,
        ),
        sa.Column(
            "new_status",
            sa.String(50),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("order_status_history")