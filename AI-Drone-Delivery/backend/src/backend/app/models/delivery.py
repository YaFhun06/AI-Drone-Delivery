from app import db

class Delivery(db.Model):
    __tablename__ = 'deliveries'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    drone_id = db.Column(db.Integer, db.ForeignKey('drones.id'), nullable=False)
    dispatcher_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)
    departure_station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    arrival_station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(50))