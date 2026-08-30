from datetime import datetime

from src.infrastructure.databases.base import db


class PackageReceiptModel(db.Model):
    __tablename__ = "package_receipts"

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

    received_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    received_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )