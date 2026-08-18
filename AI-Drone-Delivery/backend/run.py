from app import create_app

app = create_app()

@app.route('/test-db')
def test_db():
    return "Ket noi PostgreSQL thanh cong!"

if __name__ == '__main__':
    app.run(debug=True)