"""add package status history

Revision ID: 4fc914cdcc6c
Revises: b16a2b464308
Create Date: 2026-09-06 01:34:43.022601

"""

from alembic import op
import sqlalchemy as sa


revision = '4fc914cdcc6c'
down_revision = 'b16a2b464308'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'package_status_histories',
        sa.Column(
            'id',
            sa.Integer,
            primary_key=True,
            autoincrement=True
        ),
        sa.Column(
            'package_id',
            sa.Integer,
            sa.ForeignKey('packages.id'),
            nullable=False
        ),
        sa.Column(
            'status',
            sa.String(length=50),
            nullable=False
        ),
        sa.Column(
            'created_at',
            sa.DateTime,
            nullable=False
        )
    )


def downgrade():
    op.drop_table('package_status_histories')