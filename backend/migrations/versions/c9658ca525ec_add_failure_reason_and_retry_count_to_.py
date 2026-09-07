"""add failure reason and retry count to orders

Revision ID: c9658ca525ec
Revises: f42829856e36
Create Date: 2026-09-05 00:39:27.172968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9658ca525ec'
down_revision = 'f42829856e36'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('failure_reason', sa.String(length=255), nullable=True)
        )
        batch_op.add_column(
            sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0')
        )


def downgrade():
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('retry_count')
        batch_op.drop_column('failure_reason')