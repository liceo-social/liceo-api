from liceo.labs.poirot.core import Repository, sql
from ..application.repositories import PermissionsRepository


class PoirotPermissionsRepository(PermissionsRepository, Repository):
    @sql()
    def find_all_roles_by_permission_name(self, name: str) -> list[str]:
        return []
