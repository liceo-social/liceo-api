from typing import Callable, Set
from dataclasses import dataclass
from liceo.labs.sherlock.core import AggregateEvent
from liceo.infra.domain.entities import AuditableAggregate
from liceo.security.roles.domain import vo


class Role(AuditableAggregate[vo.UserId]):
    @dataclass
    class CreateRoleCommand:
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
    class AddPermissionsCommand:
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

            aggregate.mark_modified_by(self.added_by)

    @dataclass
    class RemovePermissionsCommand:
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

            aggregate.mark_modified_by(self.removed_by)

    @dataclass
    class DeleteRoleCommand:
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
    def create(command: CreateRoleCommand):
        return Role(id=command.next_id()).append(Role.RoleCreated(name=command.name, created_by=command.created_by))

    def add_permissions(self, command: AddPermissionsCommand):
        return self.append(Role.PermissionsAdded(permissions=command.permissions, added_by=command.added_by))

    def remove_permissions(self, command: RemovePermissionsCommand):
        return self.append(Role.PermissionsRemoved(permissions=command.permissions, removed_by=command.removed_by))

    def delete(self, command: DeleteRoleCommand):
        return self.append(Role.RoleDeleted(deleted_by=command.deleted_by))
