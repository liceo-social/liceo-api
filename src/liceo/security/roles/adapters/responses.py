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
    def from_dto(role: dtos.FullRoleDTO | None) -> "ShowRoleResponse | None":
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


@dataclass
class CreateRoleResponse:
    id: str
    version: int
    name: str
    description: str

    @staticmethod
    def from_dto(dto: dtos.RoleDTO):
        return CreateRoleResponse(
            id=dto.id,
            version=dto.version,
            name=dto.name,
            description=dto.description
        )


@dataclass
class UpdateRoleDetailsResponse:
    id: str
    version: int
    name: str
    description: str

    @staticmethod
    def from_role(role: entities.Role | None) -> "UpdateRoleDetailsResponse | None":
        if not role:
            return

        return UpdateRoleDetailsResponse(
            id=role.id.id,
            version=role._version,
            name=role.name,
            description=role.description
        )


@dataclass
class UpdateRolePermissionsResponse:
    id: str
    version: int
    permissions: list[str]

    @staticmethod
    def from_role(role: entities.Role | None):
        if not role:
            return

        return UpdateRolePermissionsResponse(
            id=role.id.id,
            version=role._version,
            permissions=[p.id for p in role.permissions]
        )


@dataclass
class DeleteRoleResponse:
    id: str
    version: int

    @staticmethod
    def from_role(role: entities.Role | None):
        if not role:
            return None
        return DeleteRoleResponse(id=role.id.id, version=role._version)
