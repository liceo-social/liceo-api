from abc import ABC, abstractmethod
from liceo.infra.domain.vo import Pagination, Paged
from liceo.security.permissions.domain import entities


class PermissionsRepository(ABC):
    @abstractmethod
    def filter_permissions(self, name: str | None, pagination: Pagination) -> Paged[entities.Permission]:
        pass
