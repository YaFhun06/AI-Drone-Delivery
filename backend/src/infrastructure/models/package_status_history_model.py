from datetime import datetime

from src.infrastructure.databases.base import db


class PackageStatusHistoryModel(db.Model):
    __tablename__ = "package_status_histories"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    package_id = db.Column(
        db.Integer,
        db.ForeignKey("packages.id"),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )