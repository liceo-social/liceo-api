from typing import Callable, List, Set
from datetime import datetime
from dataclasses import dataclass, field
from liceo.labs.sherlock.core import Aggregate, AggregateEvent
from liceo.security.roles.domain import vo


class Role(Aggregate):
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
            aggregate.created_by = self.created_by
            aggregate.created_at = datetime.now()
            aggregate.last_modified_by = self.created_by
            aggregate.last_modified_at = datetime.now()

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

            aggregate.last_modified_by = self.added_by
            aggregate.last_modified_at = datetime.now()

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

            aggregate.last_modified_by = self.removed_by
            aggregate.last_modified_at = datetime.now()

    name: str
    permissions: Set[vo.PermissionId] = set()
    created_by: vo.UserId
    created_at: datetime
    last_modified_by: vo.UserId
    last_modified_at: datetime

    @staticmethod
    def create(command: CreateRoleCommand):
        return Role(id=command.next_id()).append(Role.RoleCreated(name=command.name, created_by=command.created_by))

    def add_permissions(self, command: AddPermissionsCommand):
        return self.append(Role.PermissionsAdded(permissions=command.permissions, added_by=command.added_by))

    def remove_permissions(self, command: RemovePermissionsCommand):
        return self.append(Role.PermissionsRemoved(permissions=command.permissions, removed_by=command.removed_by))
