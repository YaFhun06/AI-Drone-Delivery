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
## 2. Công nghệ triển khai:
- Frontend: ReactJS, Flutter  
- Backend: Python, Flask  
- Database: PostgreSQL, PostGIS  
- AI:Gemini API
- Deployment: Docker, Docker Compose
## 3. Các tasks chính:
- Phân tích yêu cầu và nghiệp vụ
- Thiết kế hệ thống và cơ sở dữ liệu
- Thiết kế UI/UX
- Phát triển Backend API
- Phát triển Web Application
- Phát triển Mobile Application
- Phát triển AI Services
- Tích hợp và kiểm thử hệ thống
- Docker hóa và triển khai hệ thống
- Hoàn thiện tài liệu và báo cáo
## 4. Cấu trúc dự án:
```text
AI-Drone-Delivery/
├── backend/                        # Flask API - Clean Architecture
│   ├── .env
│   ├── requirements.txt
│   ├── SETUP.md
│   ├── migrations/
│   │   └── versions/
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_station.py
│   └── src/
│       ├── app.py                  # entry point: python -m src.app
│       ├── create_app.py           # app factory, đăng ký blueprint
│       ├── config.py
│       ├── error_handler.py
│       ├── logging.py
│       ├── api/
│       │   └── controllers/        # auth, role, address, customer,
│       │                           # station, eta, chatbot, delivery_summary
│       ├── domain/
│       │   ├── exceptions.py
│       │   └── constants.py
│       ├── services/
│       └── infrastructure/
│           ├── ai/                 # gemini_client.py
│           ├── databases/
│           ├── models/
│           └── repositories/
│
├── frontend/                       # ReactJS (Vite + Tailwind)
│   ├── public/
│   └── src/
│       ├── components/             # Header, Sidebar, Footer
│       ├── layouts/                # MainLayout
│       ├── pages/                  # Login, Dashboard
│       ├── App.jsx
│       └── main.jsx
│
├── mobile/                         # Flutter app
│   ├── android/
│   ├── ios/
│   ├── lib/
│   │   ├── main.dart
│   │   └── screens/                # login_screen, dashboard_screen
│   └── pubspec.yaml
│
├── database/                       # Script SQL, seed data
│
├── doc/
│   ├── Doc SRS/                    # main.tex, sections/, images/
│   └── UML/
│
├── .gitignore
└── README.md
```
