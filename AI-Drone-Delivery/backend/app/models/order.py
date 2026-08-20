from app import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    sender_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    receiver_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50))