from typing import Callable
from dataclasses import dataclass

from liceo.labs.sherlock.core import AggregateEvent
from liceo.infra.domain.entities import AuditableAggregate, PermissionAwareCommand
from liceo.security.permissions.domain import vo
from liceo.security.permissions.domain import permissions


class Permission(AuditableAggregate[vo.UserId]):
    @dataclass
    class CreatePermissionCommand(PermissionAwareCommand[vo.UserId]):
        name: str
        next_id: Callable[[], str]
        created_by: vo.UserId

    @dataclass(kw_only=True)
    class PermissionCreated(AggregateEvent):
        event_type: str = "PERMISSION_CREATED"
        name: str
        created_by: vo.UserId

        def handle(self, aggregate: "Permission"):
            aggregate.name = self.name
            aggregate.mark_created_by(self.created_by)

    @dataclass
    class ChangeNameCommand(PermissionAwareCommand[vo.UserId]):
        new_name: str
        changed_by: vo.UserId

    @dataclass(kw_only=True)
    class NameChanged(AggregateEvent):
        event_type: str = "PERMISSION_NAME_CHANGED"
        new_name: str
        changed_by: vo.UserId

        def handle(self, aggregate: "Permission"):
            aggregate.name = self.new_name
            aggregate.mark_modified_by(self.changed_by)

    @dataclass
    class DeletePermissionCommand(PermissionAwareCommand[vo.UserId]):
        deleted_by: vo.UserId

    @dataclass(kw_only=True)
    class PermissionDeleted(AggregateEvent):
        event_type: str = "PERMISSION_DELETED"
        deleted_by: vo.UserId

        def handle(self, aggregate: "Permission"):
            aggregate.mark_deleted_by(self.deleted_by)

    name: str
    description: str

    @staticmethod
    def create(cmd: CreatePermissionCommand):
        cmd.check_permission(permissions.PERMISSION_CREATE, cmd.created_by)
        return Permission(id=cmd.next_id()).append(Permission.PermissionCreated(created_by=cmd.created_by, name=cmd.name))

    def change_name(self, cmd: ChangeNameCommand):
        cmd.check_permission(permissions.PERMISSION_MODIFY, cmd.changed_by)
        return self.append(Permission.NameChanged(changed_by=cmd.changed_by, new_name=cmd.new_name))

    def delete(self, cmd: DeletePermissionCommand):
        cmd.check_permission(permissions.PERMISSION_DELETE, cmd.deleted_by)
        return self.append(Permission.PermissionDeleted(deleted_by=cmd.deleted_by))
