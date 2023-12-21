"""initial data

Revision ID: f3b93c753022
Revises: dea77b8a0a92
Create Date: 2023-12-21 11:48:29.696620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3b93c753022'
down_revision: Union[str, None] = 'dea77b8a0a92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_tbl = sa.sql.table(
        "user",
        sa.sql.column("email", sa.String),
        sa.sql.column("password", sa.String),
        sa.sql.column("role_type", sa.String),
    )
    op.bulk_insert(user_tbl, [
        {
            "email": "superadmin@gmail.com",
            "password": "superadmin",
            "role_type": "superadmin"
        }
    ])
    
    complaint_status_tbl = sa.sql.table(
        "complaint_status",
        sa.sql.column("name", sa.String),
    )
    op.bulk_insert(complaint_status_tbl, [
        {"name": "PENDING"},
        {"name": "ASSIGNED"},
        {"name": "DONE"},
        {"name": "RESOLVED"},
    ])


def downgrade() -> None:
    pass
