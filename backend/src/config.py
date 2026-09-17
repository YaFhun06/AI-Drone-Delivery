import os
from pathlib import Path

from dotenv import load_dotenv


# Thư mục backend/
BASE_DIR = Path(__file__).resolve().parents[1]

# Đọc file backend/.env nếu có
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)


class Config:
    """
    Cấu hình dùng chung cho Flask application.

    Không lưu password database hoặc secret trực tiếp trong source code.
    Các giá trị nhạy cảm phải được cấu hình trong file .env.
    """

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY")

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600")
    )

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gemini AI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # CORS
    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173",
    )

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            FRONTEND_URL,
        ).split(",")
        if origin.strip()
    ]

    # Flask environment
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    TESTING = os.getenv("TESTING", "false").lower() == "true"

    @classmethod
    def validate(cls):
        """
        Kiểm tra các biến môi trường bắt buộc.

        Không kiểm tra DATABASE_URL khi đang chạy test,
        vì test dùng SQLite in-memory.
        """
        required_values = {
            "SECRET_KEY": cls.SECRET_KEY,
            "JWT_SECRET_KEY": cls.JWT_SECRET_KEY,
        }

        if not cls.TESTING:
            required_values["DATABASE_URL"] = cls.SQLALCHEMY_DATABASE_URI

        missing_values = [
            key
            for key, value in required_values.items()
            if not value
        ]

        if missing_values:
            raise RuntimeError(
                "Thiếu biến môi trường bắt buộc: "
                + ", ".join(missing_values)
            )