from alembic import op
import sqlalchemy as sa


revision = '9fe93334a6f5'
down_revision = 'add_location_to_stations'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'package_receipts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('package_id', sa.Integer(), nullable=False),
        sa.Column('station_id', sa.Integer(), nullable=False),
        sa.Column('received_at', sa.DateTime(), nullable=False),
        sa.Column('received_by', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['received_by'], ['users.id']),
        sa.ForeignKeyConstraint(['station_id'], ['stations.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('package_receipts')