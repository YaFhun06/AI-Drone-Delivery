"""add status to packages

Revision ID: b16a2b464308
Revises: c9658ca525ec
Create Date: 2026-09-05 01:26:51.246023

"""

from alembic import op
import sqlalchemy as sa


revision = 'b16a2b464308'
down_revision = 'c9658ca525ec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'packages',
        sa.Column(
            'status',
            sa.String(length=50),
            nullable=False,
            server_default='RECEIVED'
        )
    )

    op.alter_column(
        'packages',
        'status',
        server_default=None
    )


def downgrade():
    op.drop_column('packages', 'status')