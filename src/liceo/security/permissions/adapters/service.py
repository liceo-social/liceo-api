from dataclasses import dataclass
from liceo.infra.domain.vo import Paged
from liceo.labs.db.core import AbstractService, managed_service
from ..application import service, repository


@dataclass
@managed_service
class DatabasePermissionService(service.PermissionsService, AbstractService):
    permissions: repository.PermissionsRepository

    def filter(self, dto: service.FilterPermissionsDTO) -> Paged[service.Permission]:
        return self.permissions.filter_permissions(dto.name, pagination=dto.pagination)
