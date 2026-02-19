from dataclasses import dataclass
from liceo.infra.domain.vo import Paged
from ..application import dtos
from ..domain import entities


@dataclass
class ListRolesResponses:
    data: list[dtos.RoleDTO]
    total_count: int

    @staticmethod
    def from_dto(paged: Paged):
        return ListRolesResponses(data=paged.data, total_count=paged.total)


@dataclass
class ShowRolePermissionResponse:
    id: str
    name: str
    description: str


@dataclass
class ShowRoleResponse:
    id: str
    version: int
    name: str
    description: str
    permissions: list[ShowRolePermissionResponse]

    @staticmethod
    def from_role(role: dtos.FullRoleDTO | None) -> "ShowRoleResponse | None":
        if not role:
            return
        return ShowRoleResponse(
            id=role.id,
            version=role.version,
            name=role.name,
            description=role.description,
            permissions=[ShowRolePermissionResponse(
                id=p.id, name=p.name, description=p.description) for p in role.permissions]
        )
