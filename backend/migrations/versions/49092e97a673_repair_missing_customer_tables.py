"""repair missing customer tables

Revision ID: 49092e97a673
Revises: 9caa19fcbc19
Create Date: 2026-09-05

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49092e97a673'
down_revision = '9caa19fcbc19'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # Create addresses table if it does not exist
    if 'addresses' not in inspector.get_table_names():
        op.create_table(
            'addresses',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('street', sa.String(length=255), nullable=False),
            sa.Column('city', sa.String(length=100), nullable=True),
            sa.Column('latitude', sa.Float(), nullable=True),
            sa.Column('longitude', sa.Float(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Create customers table if it does not exist
    if 'customers' not in inspector.get_table_names():
        op.create_table(
            'customers',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=True),
            sa.Column('full_name', sa.String(length=150), nullable=False),
            sa.Column('phone', sa.String(length=20), nullable=True),
            sa.Column('address_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['address_id'], ['addresses.id']),
            sa.ForeignKeyConstraint(['user_id'], ['users.id']),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if 'customers' in inspector.get_table_names():
        op.drop_table('customers')

    if 'addresses' in inspector.get_table_names():
        op.drop_table('addresses')