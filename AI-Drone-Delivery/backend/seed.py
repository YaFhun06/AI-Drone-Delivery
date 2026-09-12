import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'src', 'backend'))
from app import create_app
from app.extensions import db
app = create_app()
with app.app_context():
    db.create_all()
    print('=== SEED DỮ LIỆU THÀNH CÔNG 100% ===')
