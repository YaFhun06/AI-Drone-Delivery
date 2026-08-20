from app import db

class Drone(db.Model):
    __tablename__ = 'drones'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    battery_level = db.Column(db.Float, nullable=False)
    max_payload = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50))