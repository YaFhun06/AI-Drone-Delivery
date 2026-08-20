from app import db

class Staff(db.Model):
    __tablename__ = 'staffs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    staff_code = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(100))