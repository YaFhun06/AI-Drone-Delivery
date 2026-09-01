from src.infrastructure.models.order_model import OrderModel
from sqlalchemy import func
from src.infrastructure.databases.base import db


class AnalyticsService:
    def get_order_status_summary(self):
        results = (
            db.session.query(OrderModel.status, func.count(OrderModel.id))
            .group_by(OrderModel.status)
            .all()
        )
        summary = {status: count for status, count in results}
        total = sum(summary.values())
        return {
            "total_orders": total,
            "by_status": summary,
        }