from liceo.infra.domain.vo import Paged, Pagination
from liceo.security.permissions.application import ports
from liceo.security.permissions.domain.entities import Permission


PERMISSIONS: dict[str, Permission] = {}


class PermissionMemoryRepository(ports.SavePermissionPort, ports.ListPermissionsPort):
    def save_permission(self, permission: Permission) -> Permission:
        PERMISSIONS[permission.id.id] = permission
        return permission

    def list_permissions(self, pagination: Pagination) -> Paged[Permission]:
        from_offset = pagination.offset
        to_offset = (pagination.offset + pagination.max) - 1
        permissions = list(PERMISSIONS.values())

        return Paged(
            total=pagination.max,
            data=permissions[from_offset:to_offset]
        )
