from app import db

class AiPrediction(db.Model):
    __tablename__ = 'ai_predictions'
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('deliveries.id'), nullable=False)
    predicted_eta = db.Column(db.DateTime, nullable=False)
    delivery_summary = db.Column(db.Text)