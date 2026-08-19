# Hướng dẫn Setup Database (Backend)

## Bước 1 — Cài PostgreSQL + pgAdmin (nếu chưa có)
Tải tại: https://www.postgresql.org/download/windows/
Nhớ ghi lại mật khẩu đã đặt cho user `postgres`.

## Bước 2 — Tạo database rỗng
Mở pgAdmin → chuột phải vào **Databases** → **Create → Database** → đặt tên: `dronedelivery` → Save

## Bước 3 — Kéo code mới nhất từ main
git checkout main
git pull
cd AI-Drone-Delivery/src/backend

## Bước 4 — Tạo và kích hoạt môi trường ảo
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

## Bước 5 — Tạo file .env
Tạo file `.env` trong thư mục `backend`, nội dung:
SECRET_KEY=abc1234
JWT_SECRET_KEY=123456
DATABASE_URL=postgresql://postgres:MAT_KHAU_CUA_BAN@localhost:5432/dronedelivery
GEMINI_API_KEY=
Đổi `MAT_KHAU_CUA_BAN` thành mật khẩu PostgreSQL thật của bạn.

## Bước 6 — Tạo bảng thật từ migration có sẵn
**Không chạy `flask db init` hay `flask db migrate`** — chỉ cần: flask db upgrade

## Bước 7 — Seed dữ liệu Role mẫu
flask shell
```python
from app import db
from app.models.role import Role
roles = [
    Role(name='Customer', description='Khách hàng'),
    Role(name='Dispatcher', description='Điều phối viên'),
    Role(name='StationOperator', description='Vận hành trạm'),
    Role(name='LogisticsManager', description='Quản lý vận hành'),
    Role(name='Admin', description='Quản trị hệ thống'),
]
db.session.add_all(roles)
db.session.commit()
exit()
```
## Bước 8 — Kiểm tra thành công
Vào `http://127.0.0.1:5000/test-db` — thấy **"Ket noi PostgreSQL thanh cong!"** là xong.

## Lưu ý quan trọng
- Mỗi người có database riêng trên máy mình, không dùng chung qua mạng
- Bước 7 nếu báo lỗi "duplicate key" nghĩa là đã seed rồi, bỏ qua, không cần lo
