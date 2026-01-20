from typing import Callable
from dataclasses import dataclass
from liceo.labs.sherlock.core import AggregateEvent
from liceo.infra.domain.entities import AuditableAggregate
from liceo.security.permissions.domain import vo


class Permission(AuditableAggregate[vo.UserId]):
    @dataclass
    class CreatePermissionCommand:
        name: str
        next_id: Callable[[], vo.PermissionId]
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
    class ChangeNameCommand:
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
    class DeletePermissionCommand:
        deleted_by: vo.UserId

    @dataclass(kw_only=True)
    class PermissionDeleted(AggregateEvent):
        event_type: str = "PERMISSION_DELETED"
        deleted_by: vo.UserId

        def handle(self, aggregate: "Permission"):
            aggregate.mark_deleted_by(self.deleted_by)

    name: str

    @staticmethod
    def create(command: CreatePermissionCommand):
        return Permission(id=command.next_id()).append(Permission.PermissionCreated(created_by=command.created_by, name=command.name))

    def change_name(self, command: ChangeNameCommand):
        return self.append(Permission.NameChanged(changed_by=command.changed_by, new_name=command.new_name))

    def delete(self, command: DeletePermissionCommand):
        return self.append(Permission.PermissionDeleted(deleted_by=command.deleted_by))
