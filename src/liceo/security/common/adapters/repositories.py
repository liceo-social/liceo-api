from liceo.labs.poirot.core import Repository, sql
from ..application.repositories import PermissionsRepository


class PoirotPermissionsRepository(PermissionsRepository, Repository):
    @sql(lambda rows: [row["role_name"] for row in rows])
    def find_all_roles_by_permission_name(self, name: str) -> list[str]:
        return []
