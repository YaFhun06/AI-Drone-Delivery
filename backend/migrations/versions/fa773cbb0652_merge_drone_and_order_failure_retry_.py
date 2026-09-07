"""Merge drone and order failure/retry migrations

Revision ID: fa773cbb0652
Revises: 4fc914cdcc6c, 52d90b778c11
Create Date: 2026-09-07 09:44:42.592821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa773cbb0652'
down_revision = ('4fc914cdcc6c', '52d90b778c11')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
