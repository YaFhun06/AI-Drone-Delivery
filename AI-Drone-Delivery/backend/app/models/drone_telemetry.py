from app import db
from datetime import datetime

class DroneTelemetry(db.Model):
    __tablename__ = 'drone_telemetries'
    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('drones.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    current_latitude = db.Column(db.Float, nullable=False)
    current_longitude = db.Column(db.Float, nullable=False)
    current_battery = db.Column(db.Float, nullable=False)