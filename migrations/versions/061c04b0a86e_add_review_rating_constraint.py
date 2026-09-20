"""add review rating constraint

Revision ID: 061c04b0a86e
Revises: ed5e87a3f5aa
Create Date: 2026-09-20 01:21:51.368933

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "061c04b0a86e"
down_revision: Union[str, Sequence[str], None] = "ed5e87a3f5aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_review_rating",
        "reviews",
        "rating >= 1 AND rating <= 5",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_review_rating",
        "reviews",
        type_="check",
    )