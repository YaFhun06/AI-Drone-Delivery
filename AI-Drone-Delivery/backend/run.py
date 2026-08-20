from app import create_app, db
from sqlalchemy import text

app = create_app()

@app.route('/test-db')
def test_db():
    try:
        # Thử thực thi câu lệnh SQL để kiểm tra kết nối thật
        db.session.execute(text('SELECT 1'))
        return "Ket noi PostgreSQL thanh cong!"
    except Exception as e:
        return f"Loi ket noi PostgreSQL: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)