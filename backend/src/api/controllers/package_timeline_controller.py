from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from src.services.package_timeline_service import PackageTimelineService
from src.domain.exceptions import DomainException


package_timeline_bp = Blueprint(
    "package_timeline",
    __name__
)

package_timeline_service = PackageTimelineService()


@package_timeline_bp.route(
    "/api/packages/<int:package_id>/timeline",
    methods=["GET"]
)
@jwt_required()
def get_package_timeline(package_id):

    try:
        histories = package_timeline_service.get_timeline(
            package_id
        )

    except DomainException as e:
        return jsonify({
            "error": e.message
        }), e.status_code

    return jsonify({
        "package_id": package_id,
        "timeline": [
            {
                "status": history.status,
                "created_at": history.created_at.isoformat()
            }
            for history in histories
        ]
    }), 200