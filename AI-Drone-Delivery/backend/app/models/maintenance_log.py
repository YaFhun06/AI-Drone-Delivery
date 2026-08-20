from app import db

class MaintenanceLog(db.Model):
    __tablename__ = 'maintenance_logs'
    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('drones.id'), nullable=False)
    maintenance_date = db.Column(db.DateTime, nullable=False)
    details = db.Column(db.String(255))