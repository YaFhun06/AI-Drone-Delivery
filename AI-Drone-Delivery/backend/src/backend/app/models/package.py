from app import db

class Package(db.Model):
    __tablename__ = 'packages'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    dimensions = db.Column(db.String(50))
    description = db.Column(db.String(255))