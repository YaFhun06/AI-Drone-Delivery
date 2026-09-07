from src.infrastructure.repositories.package_repository import PackageRepository
from src.infrastructure.repositories.package_status_history_repository import (
    PackageStatusHistoryRepository
)

from src.domain.exceptions import PackageNotFoundError


class PackageTimelineService:

    def __init__(
        self,
        package_repository=None,
        history_repository=None
    ):
        self.package_repository = (
            package_repository or PackageRepository()
        )
        self.history_repository = (
            history_repository or PackageStatusHistoryRepository()
        )

    def get_timeline(self, package_id):
        package = self.package_repository.find_by_id(package_id)

        if not package:
            raise PackageNotFoundError()

        histories = self.history_repository.find_by_package_id(
            package_id
        )

        return histories