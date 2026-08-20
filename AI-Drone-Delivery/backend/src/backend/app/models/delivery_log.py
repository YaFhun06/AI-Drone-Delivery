from app import db
from datetime import datetime

class DeliveryLog(db.Model):
    __tablename__ = 'delivery_logs'
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('deliveries.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status_note = db.Column(db.String(255))