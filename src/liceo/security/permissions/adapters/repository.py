from typing import Any
from liceo.infra.domain.vo import Paged, Pagination
from liceo.labs.db.sql import SQLRepository
from liceo.security.permissions.domain.entities import Permission
from ..application.repository import PermissionsRepository
from ..domain.vo import PermissionId


class SQLPermissionsRepository(PermissionsRepository, SQLRepository):
    def _map_to_row_to_permission(self, row: dict) -> Permission:
        permission = Permission()
        permission.id = PermissionId(id=row["id"])
        permission.name = row["name"]
        permission.description = row["description"]
        return permission

    def filter_permissions(self, name: str | None, pagination: Pagination) -> Paged[Permission]:
        sql = self.resolve_sql(self.filter_permissions)
        params: dict = {
            "offset": pagination.get_offset(),
            "max": pagination.max
        }

        if name is not None:
            params.update({"name": f"%{name}%"})

        result = self._get_connection().all(
            self.sql_optimize_params(sql, params=params),
            params
        )

        data = list(map(self._map_to_row_to_permission, result))
        total_count = result[0]["total_count"] if len(data) > 0 else 0
        return Paged(total=total_count, data=data)
