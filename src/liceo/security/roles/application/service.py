from abc import ABC, abstractmethod
from liceo.infra.domain.vo import Paged
from .dtos import ListRolesDTO, RoleDTO, CreateRoleDTO, UpdateRoleDetailsDTO, UpdateRolePermissionsDTO, DeleteRoleDTO, ShowRoleDTO
from ..domain.entities import Role


class RolesService(ABC):
    @abstractmethod
    def show(self, dto: ShowRoleDTO) -> Role | None:
        pass

    @abstractmethod
    def list(self, dto: ListRolesDTO) -> Paged[RoleDTO]:
        pass

    @abstractmethod
    def create_role(self, dto: CreateRoleDTO) -> RoleDTO:
        pass

    @abstractmethod
    def update_role_name(self, dto: UpdateRoleDetailsDTO) -> Role | None:
        pass

    @abstractmethod
    def update_role_permissions(self, dto: UpdateRolePermissionsDTO) -> Role | None:
        pass

    @abstractmethod
    def delete_role(self, dto: DeleteRoleDTO) -> None:
        pass
