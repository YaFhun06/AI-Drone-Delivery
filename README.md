# Dự án: AI-powered Drone Delivery Management Platform

## 1. Các main-flow chính:
1. Đăng nhập và phân quyền người dùng.
2. Quản lý khách hàng.
3. Quản lý đơn giao hàng.
4. Quản lý kiện hàng.
5. Quản lý trạm hạ cánh.
6. Thực hiện và theo dõi giao hàng.
7. Xác nhận hoàn thành giao hàng.
8. Dashboard, thống kê và báo cáo.
9. AI hỗ trợ (ước tính ETA, tóm tắt giao hàng, chatbot hỗ trợ khách hàng).

## 2. Công nghệ triển khai

- **Frontend:** ReactJS (Web), Flutter (Mobile)
- **Backend:** Python (Flask), SQLAlchemy, Flask-Migrate
- **Database:** PostgreSQL, PostGIS
- **AI:** Gemini API (chính), Groq API (dự phòng) — tích hợp trực tiếp trong Backend
- **Storage:** MinIO
- **Deployment:** Docker, Docker Compose

## 3. Các task chính

- Phân tích yêu cầu và nghiệp vụ
- Thiết kế hệ thống và cơ sở dữ liệu
- Thiết kế UI/UX
- Phát triển Backend API
- Phát triển Web Application
- Phát triển Mobile Application
- Tích hợp AI Services (Gemini/Groq) vào Backend
- Tích hợp và kiểm thử hệ thống
- Docker hóa và triển khai hệ thống
- Hoàn thiện tài liệu và báo cáo

## 4. Cấu trúc dự án
\```
AI-Drone-Delivery/
├── doc/
│   └── Doc SRS/
│       ├── main.tex
│       ├── sections/      # Chapter 1-4, tài liệu tham khảo
│       └── images/        # Ảnh + sơ đồ
├── backend/               # Flask (Python)
│   ├── app/
│   │   ├── models/
│   │   └── routes/
│   ├── run.py
│   ├── requirements.txt
│   └── .env                # không commit lên GitHub
├── web/                     # ReactJS
├── mobile/                  # Flutter
├── database/                # Migration scripts, seed data mẫu
├── README.md
└── .gitignore
\```