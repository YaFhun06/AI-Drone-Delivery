from src.infrastructure.models.order_model import OrderModel
from src.infrastructure.models.station_model import StationModel
from sqlalchemy import func
from src.infrastructure.databases.base import db
from datetime import datetime, timedelta

BASE_DELIVERY_FEE = 15000
FEE_PER_PACKAGE_WEIGHT = 5000

class AnalyticsService:
    def get_order_status_summary(self):
        # Truy vấn thật từ bảng orders trên Supabase
        results = (
            db.session.query(OrderModel.status, func.count(OrderModel.id))
            .group_by(OrderModel.status)
            .all()
        )
        summary = {status: count for status, count in results}
        total = sum(summary.values())
        
        # Nếu DB chưa có đơn hàng nào, trả về 0 thay vì làm sập trang web
        return {
            "total_orders": total,
            "by_status": summary if summary else {"PENDING": 0, "DELIVERED": 0}
        }

    def get_station_performance(self):
        # Trả về danh sách trạm (tạm thời trả về khung chuẩn để biểu đồ vẽ được)
        return [
            {"station_name": "Trạm Trung Tâm", "completed_orders": 0, "active_drones": 0},
            {"station_name": "Trạm Thủ Đức", "completed_orders": 0, "active_drones": 0},
        ]

    def get_delivery_success_rate(self):
        total = db.session.query(func.count(OrderModel.id)).scalar() or 0
        success = db.session.query(func.count(OrderModel.id)).filter(
            OrderModel.status.in_(["DELIVERED", "COMPLETED", "success"])
        ).scalar() or 0
        
        rate = round((success / total * 100), 1) if total > 0 else 0.0
        return {
            "success_rate": rate,
            "total_delivered": success,
            "total_orders": total
        }

    def get_operating_cost_summary(self):
        # Khi chưa có bảng log chi phí, trả về cơ cấu mặc định mức 0
        return {
            "total_cost": 0,
            "drone_maintenance": 0,
            "battery_charging": 0,
            "system_operation": 0
        }
