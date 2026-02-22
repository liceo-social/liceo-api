from abc import ABC, abstractmethod
from liceo.infra.domain.vo import Paged

from .dtos import FilterPermissionsDTO
from ..domain.entities import Permission


class PermissionsService(ABC):
    @abstractmethod
    def filter(self, dto: FilterPermissionsDTO) -> Paged[Permission]:
        pass
