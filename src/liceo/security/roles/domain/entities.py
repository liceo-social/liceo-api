from typing import Callable, Set
from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import AggregateEvent
from liceo.infra.domain.entities import AuditableAggregate, PermissionAwareCommand
from liceo.security.roles.domain import vo
from liceo.security.roles.domain import permissions


class Role(AuditableAggregate[vo.RoleId, vo.UserId]):
    @dataclass
    class CreateRoleCommand(PermissionAwareCommand[vo.UserId]):
        next_id: Callable[[], vo.RoleId]
        name: str
        created_by: vo.UserId

    @dataclass(kw_only=True)
    class RoleCreated(AggregateEvent):
        event_type: str = "ROLE_CREATED"
        name: str
        created_by: vo.UserId

        def handle(self, aggregate: "Role"):
            aggregate.name = self.name
            aggregate.mark_created_by(self.created_by)

    @dataclass
    class AddPermissionsCommand(PermissionAwareCommand[vo.UserId]):
        permissions: Set[vo.PermissionId]
        added_by: vo.UserId

    @dataclass(kw_only=True)
    class PermissionsAdded(AggregateEvent):
        event_type: str = "ROLE_PERMISSIONS_ADDED"
        permissions: Set[vo.PermissionId]
        added_by: vo.UserId

        def handle(self, aggregate: "Role"):
            for permission in self.permissions:
                aggregate.permissions.add(permission)

            aggregate.mark_updated_by(self.added_by)

    @dataclass
    class RemovePermissionsCommand(PermissionAwareCommand[vo.UserId]):
        removed_by: vo.UserId
        permissions: Set[vo.PermissionId]

    @dataclass(kw_only=True)
    class PermissionsRemoved(AggregateEvent):
        event_type: str = "ROLE_PERMISSIONS_REMOVED"
        removed_by: vo.UserId
        permissions: Set[vo.PermissionId]

        def handle(self, aggregate: "Role"):
            for permission in self.permissions:
                aggregate.permissions.remove(permission)

            aggregate.mark_updated_by(self.removed_by)

    @dataclass
    class DeleteRoleCommand(PermissionAwareCommand[vo.UserId]):
        deleted_by: vo.UserId

    @dataclass(kw_only=True)
    class RoleDeleted(AggregateEvent):
        event_type: str = "ROLE_DELETED"
        deleted_by: vo.UserId

        def handle(self, aggregate: "Role"):
            aggregate.permissions = set()
            aggregate.mark_deleted_by(self.deleted_by)

    name: str
    permissions: Set[vo.PermissionId] = set()

    @staticmethod
    def create(cmd: CreateRoleCommand):
        cmd.check_permission(permissions.ROLES_CREATE, cmd.created_by)
        return Role(id=cmd.next_id()).append(Role.RoleCreated(name=cmd.name, created_by=cmd.created_by))

    def add_permissions(self, cmd: AddPermissionsCommand):
        cmd.check_permission(permissions.ROLES_MODIFY, cmd.added_by)
        return self.append(Role.PermissionsAdded(permissions=cmd.permissions, added_by=cmd.added_by))

    def remove_permissions(self, cmd: RemovePermissionsCommand):
        cmd.check_permission(permissions.ROLES_MODIFY, cmd.removed_by)
        return self.append(Role.PermissionsRemoved(permissions=cmd.permissions, removed_by=cmd.removed_by))

    def delete(self, cmd: DeleteRoleCommand):
        cmd.check_permission(permissions.ROLES_DELETE, cmd.deleted_by)
        return self.append(Role.RoleDeleted(deleted_by=cmd.deleted_by))

    @property
    def aggregate_type(self) -> str:
        return "ROLE"
