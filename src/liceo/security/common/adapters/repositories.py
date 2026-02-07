from liceo.labs.db.sql import SQLRepository, sql
from ..application.repositories import PermissionsRepository


class PoirotPermissionsRepository(PermissionsRepository, SQLRepository):
    @sql(lambda rows: [row["role_name"] for row in rows])
    def find_all_roles_by_permission_name(self, name: str) -> list[str]:
        return []
