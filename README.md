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
- Backend: Python, Flask (RESTful API, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-SocketIO ở mức nền tảng)
- Database: PostgreSQL trên Supabase, truy cập qua SQLAlchemy 
- AI: Gemini API (ETA, Chatbot, tóm tắt giao hàng)
- Deployment:Frontend Vite, Backend Flask, Supabase PostgreSQL 
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
AAI-Drone-Delivery/
├── backend/                        # Flask API - Clean Architecture
│   ├── .env
│   ├── requirements.txt
│   ├── SETUP.md
│   ├── migrations/
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_station.py
│   ├── venv/
│   └── src/
│       ├── app.py                  # entry point: python -m src.app
│       ├── config.py
│       ├── create_app.py           # app factory, đăng ký blueprint
│       ├── dependency_container.py 
│       ├── error_handler.py
│       ├── extensions.py
│       ├── logging.py
│       ├── sockets.py
│       ├── api/                    # controllers (auth, users, customers,
│       │                           # stations, orders, eta, chatbot...)
│       ├── domain/
│       ├── infrastructure/         # ai, databases, models, repositories
│       └── services/
│
├── frontend/                       # ReactJS (Vite + Tailwind)
│   ├── dist/
│   ├── node_modules/
│   ├── public/
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── README.md
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx                
│       │                           
│       │                           
│       ├── App.css
│       ├── index.css
│       ├── main.jsx
│       ├── components/            
│       └── services/                
│
├── mobile/                         # Flutter app
│   ├── android/
│   ├── ios/
│   ├── lib/                                        
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
