from shortuuid import uuid
from liceo.infra.domain.vo import Paged
from liceo.labs.db.sql import SQLRepository, sql
from liceo.security.roles.domain.entities import Role
from liceo.security.roles.domain.vo import Permission, RoleId
from ..application.repository import RolesRepository
from . import mappers


class SQLRolesRepository(RolesRepository, SQLRepository):
    def generate_id(self) -> RoleId:
        return RoleId(id=uuid())

    @sql(mappers.map_from_row_to_role)
    def find_by_id(self, id: str) -> Role | None:
        return None

    @sql(mappers.map_from_rows_to_paged_role)
    def paged_roles(self, max: int, offset: int) -> Paged[Role]:
        return Paged.empty()

    def save(self, role: Role) -> Role:
        self._get_connection().insert(
            self.resolve_sql(self.save),
            params={
                "id": role.id,
                "version": role._version,
                "name": role.name,
                "description": role.description,
                "created_by": role.audit.created_by,
                "created_at": role.audit.created_at
            }
        )
        return role

    def update(self, role: Role) -> Role:
        self._get_connection().execute(
            self.resolve_sql(self.update),
            params={
                "id": role.id,
                "version": role._version,
                "name": role.name,
                "description": role.description,
                "last_updated_at": role.audit.last_updated_at,
                "last_updated_by": role.audit.last_updated_by
            }
        )
        return role

    @sql(mappers.map_rows_to_permissions)
    def find_all_permissions_by_role_id(self, role_id: str) -> list[Permission]:
        return []

    @sql()
    def _delete_role_permissions(self, role_id: str) -> None:
        pass

    def update_role_permissions(self, role: Role) -> Role:
        # deleting previous role permissions
        self._delete_role_permissions(role.id)
        # adding new permissions
        sql = self.resolve_sql(self.update_role_permissions)
        params = [
            {
                "permission_id": p.id,
                "role_id": role.id
            } for p in role.permissions
        ]
        self._get_connection().execute(sql, params=params)
        # returning modified role
        return role

    def delete(self, role: Role) -> None:
        self._get_connection().execute(self.resolve_sql(
            self.delete), params={"id": role.id, })
