"""add package pickups table

Revision ID: fa00437a3ad1
Revises: 9fe93334a6f5
Create Date: 2026-08-29

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fa00437a3ad1"
down_revision = "9fe93334a6f5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "package_pickups",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False
        ),
        sa.Column(
            "package_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "station_id",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "picked_up_at",
            sa.DateTime(),
            nullable=False
        ),
        sa.Column(
            "picked_up_by",
            sa.Integer(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["station_id"],
            ["stations.id"]
        ),
        sa.ForeignKeyConstraint(
            ["picked_up_by"],
            ["users.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade():
    op.drop_table("package_pickups")