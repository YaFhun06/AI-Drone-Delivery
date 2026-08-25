from src.infrastructure.databases.base import db

class CustomerModel(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)