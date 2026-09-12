from app.extensions import db

class Drone(db.Model):
    __tablename__ = 'drones'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='IDLE')
    battery_level = db.Column(db.Integer, default=100)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'battery_level': self.battery_level,
            'station_id': self.station_id
        }