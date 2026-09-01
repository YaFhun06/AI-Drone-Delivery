from app import db
from datetime import datetime

class Package(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    dimensions = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'weight': self.weight,
            'dimensions': self.dimensions,
            'description': self.description
        }