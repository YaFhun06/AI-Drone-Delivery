from app import db

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String(255), nullable=False) # hoặc name/address_line
    district = db.Column(db.String(100))
    city = db.Column(db.String(100))
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))