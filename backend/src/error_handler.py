from flask import jsonify
from src.domain.exceptions import DomainException

def register_error_handlers(app):
    @app.errorhandler(DomainException)
    def handle_domain_exception(e):
        return jsonify({"error": e.message}), e.status_code

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({"error": "Không tìm thấy tài nguyên"}), 404

    @app.errorhandler(500)
    def handle_server_error(e):
        return jsonify({"error": "Lỗi hệ thống nội bộ"}), 500