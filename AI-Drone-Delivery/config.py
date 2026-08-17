import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route('/test-db')
def test_db():
    try:
        db.session.execute(text('SELECT 1'))
        return 'Ket noi PostgreSQL thanh cong!'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True, port=5000)