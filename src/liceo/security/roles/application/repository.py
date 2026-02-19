from abc import ABC, abstractmethod
from liceo.infra.domain.vo import Pagination, Paged
from ..domain.entities import Role
from ..domain.vo import RoleId, Permission


class RolesRepository(ABC):
    @abstractmethod
    def generate_id(self) -> RoleId:
        pass

    @abstractmethod
    def paged_roles(self, max: int, offset: int) -> Paged[Role]:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Role | None:
        pass

    @abstractmethod
    def find_all_permissions_by_role_id(self, role_id: str) -> list[Permission]:
        pass

    @abstractmethod
    def save(self, role: Role) -> Role:
        pass

    @abstractmethod
    def update(self, role: Role) -> Role:
        pass

    @abstractmethod
    def update_role_permissions(self, role: Role) -> Role:
        pass

    @abstractmethod
    def delete(self, role: Role) -> None:
        pass
