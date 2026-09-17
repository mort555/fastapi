"""add reviews

Revision ID: c96f315ad32f
Revises: fe0aed3d0745
Create Date: 2026-09-17 19:56:11.303490

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c96f315ad32f"
down_revision: Union[str, Sequence[str], None] = "fe0aed3d0745"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "customer_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "restaurant_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "rating",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "text",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
        ),
        sa.ForeignKeyConstraint(
            ["restaurant_id"],
            ["restaurants.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("reviews")