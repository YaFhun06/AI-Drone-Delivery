"""Add location column to stations

Revision ID: add_location_to_stations
Revises: 9caa19fcbc19
"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry


# revision identifiers, used by Alembic.
revision = 'add_location_to_stations'
down_revision = '9caa19fcbc19'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'stations',
        sa.Column(
            'location',
            Geometry(geometry_type='POINT', srid=4326),
            nullable=True
        )
    )


def downgrade():
    op.drop_column('stations', 'location')