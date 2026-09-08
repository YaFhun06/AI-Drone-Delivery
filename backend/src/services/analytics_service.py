from src.infrastructure.models.order_model import OrderModel
from src.infrastructure.models.station_model import StationModel
from sqlalchemy import func
from src.infrastructure.databases.base import db
from datetime import datetime, timedelta

BASE_DELIVERY_FEE = 15000
FEE_PER_PACKAGE_WEIGHT = 5000


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

    def get_operating_cost_summary(self):
        from src.infrastructure.models.package_model import PackageModel

        total_orders = OrderModel.query.count()
        total_weight = db.session.query(func.coalesce(func.sum(PackageModel.weight), 0)).scalar()
        estimated_cost = (total_orders * BASE_DELIVERY_FEE) + (total_weight * FEE_PER_PACKAGE_WEIGHT)

        return {
            "total_orders": total_orders,
            "total_package_weight_kg": float(total_weight),
            "estimated_total_cost_vnd": estimated_cost,
            "average_cost_per_order_vnd": round(estimated_cost / total_orders, 0) if total_orders else 0,
        }

    def get_station_performance(self):
        results = (
            db.session.query(
                StationModel.id,
                StationModel.name,
                func.count(OrderModel.id).label("orders_handled"),
            )
            .outerjoin(OrderModel, OrderModel.station_id == StationModel.id)
            .group_by(StationModel.id, StationModel.name)
            .all()
        )

        return [
            {
                "station_id": station_id,
                "station_name": name,
                "orders_handled": orders_handled,
            }
            for station_id, name, orders_handled in results
        ]

    def get_delivery_success_rate(self):
        total = OrderModel.query.count()
        completed = OrderModel.query.filter_by(status="COMPLETED").count()
        failed = OrderModel.query.filter_by(status="FAILED").count()
        in_progress = total - completed - failed

        return {
            "total_orders": total,
            "completed": completed,
            "failed": failed,
            "in_progress": in_progress,
            "success_rate_percent": round((completed / total) * 100, 2) if total else 0,
            "failure_rate_percent": round((failed / total) * 100, 2) if total else 0,
        }

    def get_orders_trend(self, days=7):
        """Thong ke so don hang theo tung ngay, N ngay gan nhat."""
        start_date = datetime.utcnow() - timedelta(days=days)

        results = (
            db.session.query(
                func.date(OrderModel.created_at).label("date"),
                func.count(OrderModel.id).label("count"),
            )
            .filter(OrderModel.created_at >= start_date)
            .group_by(func.date(OrderModel.created_at))
            .order_by(func.date(OrderModel.created_at))
            .all()
        )

        return [
            {"date": str(date), "order_count": count}
            for date, count in results
        ]
