from datetime import datetime

from src.infrastructure.databases.base import db


class PackagePickupModel(db.Model):
    __tablename__ = "package_pickups"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    package_id = db.Column(
        db.Integer,
        nullable=False
    )

    station_id = db.Column(
        db.Integer,
        db.ForeignKey("stations.id"),
        nullable=False
    )

    picked_up_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    picked_up_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )