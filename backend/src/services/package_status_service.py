from src.infrastructure.repositories.package_repository import PackageRepository

from src.domain.exceptions import (
    PackageNotFoundError,
    InvalidPackageStatusError,
)


class PackageStatusService:
    ALLOWED_STATUSES = {
        "RECEIVED",
        "PROCESSING",
        "DISPATCHED",
    }

    STATUS_TRANSITIONS = {
        "RECEIVED": "PROCESSING",
        "PROCESSING": "DISPATCHED",
    }

    def __init__(self, package_repository=None):
        self.package_repository = (
            package_repository or PackageRepository()
        )

    def update_status(self, package_id, new_status):
        package = self.package_repository.find_by_id(package_id)

        if not package:
            raise PackageNotFoundError()

        if new_status not in self.ALLOWED_STATUSES:
            raise InvalidPackageStatusError()

        current_status = package.status

        if current_status == "DISPATCHED":
            raise InvalidPackageStatusError(
                "Package đã ở trạng thái DISPATCHED"
            )

        expected_status = self.STATUS_TRANSITIONS.get(current_status)

        if new_status != expected_status:
            raise InvalidPackageStatusError(
                f"Không thể chuyển trạng thái từ {current_status} sang {new_status}"
            )

        return self.package_repository.update_status(
            package,
            new_status
        )