from typing import List
from liceo.infra.domain.vo import Paged
from ..domain import vo, entities
from ..application import dtos


def map_from_row_to_role(row: dict | None) -> entities.Role | None:
    if not row:
        return None

    role = entities.Role(
        id=vo.RoleId(id=row["id"])
    )
    role._version = row["version"]
    role.name = row["name"]
    role.description = row["description"]
    role.permissions = row["permissions"]
    return role


def map_from_role_to_dto(role: entities.Role) -> dtos.RoleDTO:
    return dtos.RoleDTO(
        id=role.id.id,
        version=role._version,
        name=role.name,
        description=role.description
    )


def map_rows_to_permissions(rows: list[dict]) -> list[vo.Permission]:
    return [
        vo.Permission(
            id=row["id"],
            name=row["name"],
            description=row["description"]
        ) for row in rows
    ]


def map_from_rows_to_paged_role(rows: list[dict]) -> Paged[entities.Role]:
    if not rows or len(rows) <= 0:
        return Paged.empty()

    roles = [map_from_row_to_role(row) for row in rows]
    return Paged(
        total=rows[0]["total_count"],
        data=[role for role in roles if role is not None]
    )


def map_permissions(ps: List[str]) -> set[vo.PermissionId]:
    return set([vo.PermissionId(id=p) for p in ps])


def map_role_to_full_role_dto(role: entities.Role, permissions: list[vo.Permission]) -> dtos.FullRoleDTO:
    permission_dtos = [dtos.PermissionDTO(
        id=p.id, name=p.name, description=p.description) for p in permissions]
    return dtos.FullRoleDTO(
        id=role.id.id,
        name=role.name,
        description=role.description,
        version=role._version,
        permissions=permission_dtos
    )
