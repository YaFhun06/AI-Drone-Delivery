from src.infrastructure.databases.base import db
from datetime import datetime


class OrderModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=True)
    status = db.Column(db.String(50), default='PENDING', nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    packages = db.relationship('PackageModel', backref='order', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'station_id': self.station_id,
            'status': self.status,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }