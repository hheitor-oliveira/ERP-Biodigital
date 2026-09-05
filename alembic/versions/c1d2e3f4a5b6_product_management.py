"""canonicalize and constrain product names

Revision ID: c1d2e3f4a5b6
Revises: bba7ec3010b3
Create Date: 2026-09-04
"""

from typing import Sequence, Union

from alembic import op


revision: str = "c1d2e3f4a5b6"
down_revision: Union[str, Sequence[str], None] = "bba7ec3010b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Canonicalize existing product names and enforce uniqueness."""
    op.execute(
        """
        UPDATE product
        SET product_name = upper(
            regexp_replace(btrim(product_name), '\\s+', ' ', 'g')
        )
        """
    )

    op.create_unique_constraint(
        "product_product_name_key",
        "product",
        ["product_name"],
    )


def downgrade() -> None:
    """Remove the canonical product-name uniqueness constraint."""
    op.drop_constraint(
        "product_product_name_key",
        "product",
        type_="unique",
    )
