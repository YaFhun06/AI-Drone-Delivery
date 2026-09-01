from app import create_app, db

# Định nghĩa các bảng phụ thuộc để thỏa mãn Foreign Keys của Order
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)

app = create_app()

with app.app_context():
    from app.models.order import Order
    from app.models.package import Package
    
    db.create_all()
    print("--- DONE MIGRATION ---")