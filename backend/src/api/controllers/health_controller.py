from flask import Blueprint, jsonify
from src.infrastructure.databases.base import db
from sqlalchemy import text
import os

health_bp = Blueprint("health", __name__)


@health_bp.route("/api/health", methods=["GET"])
def health_check():
    status = {"status": "ok", "database": "unknown", "ai_service": "unknown"}

    try:
        db.session.execute(text("SELECT 1"))
        status["database"] = "ok"
    except Exception:
        status["database"] = "error"
        status["status"] = "degraded"

    if os.getenv("GEMINI_API_KEY"):
        status["ai_service"] = "configured"
    else:
        status["ai_service"] = "not_configured"

    http_code = 200 if status["status"] == "ok" else 503
    return jsonify(status), http_code
