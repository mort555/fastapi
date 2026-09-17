"""add customers

Revision ID: 4acec7345011
Revises: 8a3a756a2cfe
Create Date: 2026-09-16 13:17:08.797648

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4acec7345011"
down_revision: Union[str, Sequence[str], None] = "8a3a756a2cfe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "customers",
        sa.Column(
            "name",
            sa.String(255),
            nullable=False,
        ),
    )

    op.add_column(
        "customers",
        sa.Column(
            "email",
            sa.String(255),
            nullable=False,
        ),
    )

    op.add_column(
        "customers",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.alter_column(
        "customers",
        "phone",
        existing_type=sa.VARCHAR(length=30),
        type_=sa.String(50),
        existing_nullable=False,
    )

    op.create_unique_constraint(
        "uq_customer_email",
        "customers",
        ["email"],
    )

    op.drop_column(
        "customers",
        "first_name",
    )

    op.drop_column(
        "customers",
        "last_name",
    )


def downgrade() -> None:
    op.add_column(
        "customers",
        sa.Column(
            "first_name",
            sa.String(100),
            nullable=True,
        ),
    )

    op.add_column(
        "customers",
        sa.Column(
            "last_name",
            sa.String(100),
            nullable=True,
        ),
    )

    op.drop_constraint(
        "uq_customer_email",
        "customers",
        type_="unique",
    )

    op.alter_column(
        "customers",
        "phone",
        existing_type=sa.String(50),
        type_=sa.VARCHAR(length=30),
        existing_nullable=False,
    )

    op.drop_column(
        "customers",
        "created_at",
    )

    op.drop_column(
        "customers",
        "email",
    )

    op.drop_column(
        "customers",
        "name",
    )

    op.alter_column(
        "customers",
        "first_name",
        nullable=False,
    )

    op.alter_column(
        "customers",
        "last_name",
        nullable=False,
    )