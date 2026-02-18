from typing import List
from liceo.infra.domain.vo import Paged
from ..domain import vo, entities
from ..application import dtos


def map_from_row_to_role(row: dict) -> entities.Role:
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
        name=role.name,
        description=role.description
    )


def map_from_rows_to_paged_role(rows: list[dict]) -> Paged[entities.Role]:
    if not rows or len(rows) <= 0:
        return Paged.empty()

    return Paged(
        total=rows[0]["total_count"],
        data=[map_from_row_to_role(r) for r in rows]
    )


def map_permissions(ps: List[str]) -> set[vo.PermissionId]:
    return set([vo.PermissionId(id=p) for p in ps])
