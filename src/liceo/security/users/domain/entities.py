from dataclasses import dataclass, field
from typing import Callable

from liceo.infra.domain.entities import AuditableAggregate, PermissionAwareCommand
from liceo.labs.sherlock.core import AggregateEvent, Sensitive
from liceo.security.users.domain import vo
from liceo.security.users.domain import errors
from liceo.security.users.domain import permissions


@dataclass
class User(AuditableAggregate[vo.UserId]):
    @dataclass
    class ChangeNameCommand(PermissionAwareCommand[vo.UserId]):
        name: str
        changed_by: vo.UserId

    @dataclass(kw_only=True)
    class NameChanged(AggregateEvent):
        event_type: str = "USER_NAME_CHANGED"
        name: str
        changed_by: vo.UserId

        def handle(self, aggregate: "User"):
            aggregate.name = self.name
            aggregate.mark_modified_by(self.changed_by)

    @dataclass
    class ChangePasswordCommand(PermissionAwareCommand[vo.UserId]):
        old_password: str
        new_password: str
        new_password_repeated: str
        changed_by: vo.UserId
        old_password_check_handler: Callable[[str], bool]
        new_password_hashing_handler: Callable[[str], str]

        def is_new_password_repeated_correct(self):
            return self.new_password == self.new_password_repeated

    @dataclass(kw_only=True)
    class PasswordChanged(AggregateEvent):
        event_type: str = "USER_PASSWORD_CHANGED"
        changed_by: vo.UserId
        new_password: Sensitive[str]

        def handle(self, aggregate: "User"):
            aggregate.password = self.new_password.value
            aggregate.mark_modified_by(self.changed_by)

    @dataclass
    class AddRoleCommand(PermissionAwareCommand[vo.UserId]):
        added_by: vo.UserId
        admin_check_handler: Callable[[vo.UserId], bool]
        role_to_add: vo.Role

    @dataclass(kw_only=True)
    class RoleAdded(AggregateEvent):
        event_type: str = "USER_ROLE_ADDED"
        added_by: vo.UserId
        role: vo.Role

        def handle(self, aggregate: "User"):
            aggregate.roles.append(self.role)
            aggregate.mark_modified_by(self.added_by)

    @dataclass
    class RemoveRoleCommand(PermissionAwareCommand[vo.UserId]):
        removed_by: vo.UserId
        role_to_delete: vo.Role
        admin_check_handler: Callable[[vo.UserId], bool]

    @dataclass(kw_only=True)
    class RoleRemoved(AggregateEvent):
        event_type: str = "USER_ROLE_REMOVED"
        removed_by: vo.UserId
        role: vo.Role

        def handle(self, aggregate: "User"):
            aggregate.roles.remove(self.role)
            aggregate.mark_modified_by(self.removed_by)

    @dataclass
    class CreateUserCommand(PermissionAwareCommand[vo.UserId]):
        next_id: Callable[[], str]
        name: str
        surname: str
        username: str
        password: str
        created_by: vo.UserId

    @dataclass(kw_only=True)
    class UserCreated(AggregateEvent):
        event_type: str = "USER_CREATED"
        name: str
        surname: str
        username: str
        password: str
        created_by: vo.UserId

        def handle(self, aggregate: "User"):
            aggregate.mark_created_by(self.created_by)
            aggregate.name = self.name
            aggregate.surname = self.surname
            aggregate.username = self.username
            aggregate.password = self.password

    id: vo.UserId | None = field(default=None)
    name: str | None = field(default=None)
    surname: str | None = field(default=None)
    active: bool = field(default=False)
    username: str | None = field(default=None)
    password: str | None = field(default=None)
    roles: list[vo.Role] = field(default_factory=list)

    @staticmethod
    def create(cmd: CreateUserCommand):
        cmd.check_permission(permissions.USERS_CREATE, cmd.created_by)

        return User(id=vo.UserId(id=cmd.next_id()))\
            .append(User.UserCreated(
                created_by=cmd.created_by,
                name=cmd.name,
                surname=cmd.surname,
                username=cmd.username,
                password=cmd.password
            ))

    def _is_changed_by_same_user(self, changed_by: vo.UserId):
        return self.id and self.id == changed_by

    def change_name(self, cmd: ChangeNameCommand):
        cmd.check_permission(permissions.USERS_MODIFY, cmd.changed_by)

        if not self._is_changed_by_same_user(cmd.changed_by):
            raise errors.NotChangedBySameUserError()

        return self.append(User.NameChanged(name=cmd.name, changed_by=cmd.changed_by))

    def change_password(self, cmd: ChangePasswordCommand):
        cmd.check_permission(permissions.USERS_CREATE, cmd.changed_by)

        if not self._is_changed_by_same_user(cmd.changed_by):
            raise errors.NotChangedBySameUserError()

        if not cmd.is_new_password_repeated_correct():
            raise errors.RepeatedPasswordNotCorrect()

        return self.append(
            User.PasswordChanged(
                changed_by=cmd.changed_by,
                new_password=Sensitive(
                    cmd.new_password_hashing_handler(cmd.new_password)
                ),
            )
        )

    def add_role(self, cmd: AddRoleCommand) -> "User":
        cmd.check_permission(permissions.USERS_MODIFY, cmd.added_by)

        if not cmd.admin_check_handler(cmd.added_by):
            raise errors.RoleAddedByNoAdmin()

        if cmd.role_to_add in self.roles:
            return self

        return self.append(User.RoleAdded(added_by=cmd.added_by, role=cmd.role_to_add))

    def remove_role(self, cmd: RemoveRoleCommand) -> "User":
        cmd.check_permission(permissions.USERS_MODIFY, cmd.removed_by)

        if not cmd.admin_check_handler(cmd.removed_by):
            raise errors.RoleRemovedByNoAdmin()

        if cmd.role_to_delete in self.roles:
            return self.append(
                User.RoleRemoved(role=cmd.role_to_delete, removed_by=cmd.removed_by)
            )

        return self
