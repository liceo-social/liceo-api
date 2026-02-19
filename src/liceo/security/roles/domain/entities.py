from typing import Callable, Set
from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import AggregateEvent
from liceo.labs.sherlock.domain.errors import ConcurrentException
from liceo.infra.domain.entities import AuditableAggregate, VersionAwareCommand
from liceo.security.roles.domain import vo
from .errors import AttemptedByNoAdmin


class Role(AuditableAggregate[vo.RoleId, vo.UserId]):
    @dataclass
    class CreateRoleCommand:
        next_id: Callable[[], vo.RoleId]
        is_admin: bool
        name: str
        description: str
        permissions: Set[vo.PermissionId]
        created_by: vo.UserId

    @dataclass(kw_only=True)
    class RoleCreated(AggregateEvent):
        event_type: str = "ROLE_CREATED"
        name: str
        description: str
        permissions: Set[vo.PermissionId]
        created_by: vo.UserId

        def handle(self, aggregate: "Role"):
            aggregate.mark_created_by(self.created_by)
            aggregate.name = self.name
            aggregate.description = self.description
            aggregate.permissions = self.permissions

    @dataclass
    class ChangeRoleDetailsCommand(VersionAwareCommand):
        name: str
        description: str
        is_admin: bool
        updated_by: vo.UserId

    @dataclass(kw_only=True)
    class RoleDetailsChanged(AggregateEvent):
        event_type: str = "ROLE_DETAILS_CHANGED"
        name: str
        description: str
        updated_by: vo.UserId

        def handle(self, aggregate: "Role"):
            aggregate.mark_updated_by(self.updated_by)
            aggregate.name = self.name
            aggregate.description = self.description

    @dataclass
    class ModifyPermissionsCommand(VersionAwareCommand):
        permissions: Set[vo.PermissionId]
        is_admin: bool
        changed_by: vo.UserId

    @dataclass(kw_only=True)
    class PermissionsModified(AggregateEvent):
        event_type: str = "ROLE_PERMISSIONS_MODIFIED"
        permissions: Set[vo.PermissionId]
        changed_by: vo.UserId

        def handle(self, aggregate: "Role"):
            aggregate.mark_updated_by(self.changed_by)
            for permission in self.permissions:
                aggregate.permissions.add(permission)

            aggregate.mark_updated_by(self.changed_by)

    @dataclass
    class DeleteRoleCommand(VersionAwareCommand):
        is_admin: bool
        deleted_by: vo.UserId

    @dataclass(kw_only=True)
    class RoleDeleted(AggregateEvent):
        event_type: str = "ROLE_DELETED"
        deleted_by: vo.UserId

        def handle(self, aggregate: "Role"):
            aggregate.mark_deleted_by(self.deleted_by)
            aggregate.permissions = set()

    name: str
    description: str
    permissions: Set[vo.PermissionId] = set()

    @staticmethod
    def create(cmd: CreateRoleCommand):
        if not cmd.is_admin:
            raise AttemptedByNoAdmin()

        return Role(id=cmd.next_id()).append(
            Role.RoleCreated(
                name=cmd.name,
                description=cmd.description,
                created_by=cmd.created_by,
                permissions=cmd.permissions
            )
        )

    def modify_details(self, cmd: ChangeRoleDetailsCommand):
        if not self.check_version_matches(cmd.expected_version):
            raise ConcurrentException()

        if not cmd.is_admin:
            raise AttemptedByNoAdmin()

        return self.append(
            Role.RoleDetailsChanged(
                name=cmd.name,
                description=cmd.description,
                updated_by=cmd.updated_by
            )
        )

    def modify_permissions(self, cmd: ModifyPermissionsCommand):
        if not self.check_version_matches(cmd.expected_version):
            raise ConcurrentException()

        if not cmd.is_admin:
            raise AttemptedByNoAdmin()

        return self.append(Role.PermissionsModified(permissions=cmd.permissions, changed_by=cmd.changed_by))

    def delete(self, cmd: DeleteRoleCommand):
        if not self.check_version_matches(cmd.expected_version):
            raise ConcurrentException()

        if not cmd.is_admin:
            raise AttemptedByNoAdmin()

        return self.append(Role.RoleDeleted(deleted_by=cmd.deleted_by))

    @property
    def aggregate_type(self) -> str:
        return "ROLE"
