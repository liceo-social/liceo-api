from dataclasses import dataclass, field
from typing import Callable

from liceo.infra.domain.error import OptiakError
from liceo.infra.domain.entities import AuditableAggregate
from liceo.labs.sherlock.core import AggregateEvent, Sensitive
from liceo.security.users.domain.vo import Role, UserId


@dataclass
class User(AuditableAggregate[UserId]):
    @dataclass
    class ChangeNameCommand:
        name: str
        changed_by: UserId

    class NotChangedBySameUserError(OptiakError):
        def __init__(self):
            super().__init__(
                "security.users.error.not_changed_by_same_user",
                "property can only be changed by user",
            )

    class RepeatedPasswordNotCorrect(OptiakError):
        def __init__(self):
            super().__init__(
                "security.users.error.repeated_password",
                "repeated password is not correct",
            )

    @dataclass(kw_only=True)
    class NameChanged(AggregateEvent):
        event_type: str = "NAME_CHANGED"

        name: str
        changed_by: UserId

        def handle(self, aggregate: "User"):
            aggregate.name = self.name
            aggregate.mark_modified_by(self.changed_by)

    @dataclass
    class ChangePasswordCommand:
        old_password: str
        new_password: str
        new_password_repeated: str
        changed_by: UserId
        old_password_check_handler: Callable[[str], bool]
        new_password_hashing_handler: Callable[[str], str]

        def is_new_password_repeated_correct(self):
            return self.new_password == self.new_password_repeated

    @dataclass(kw_only=True)
    class PasswordChanged(AggregateEvent):
        event_type: str = "PASSWORD_CHANGED"

        changed_by: UserId
        new_password: Sensitive[str]

        def handle(self, aggregate: "User"):
            aggregate.password = self.new_password.value
            aggregate.mark_modified_by(self.changed_by)

    @dataclass
    class AddRoleCommand:
        added_by: UserId
        admin_check_handler: Callable[[UserId], bool]
        role_to_add: Role

    class RoleAddedByNoAdmin(OptiakError):
        def __init__(self):
            super().__init__(
                "security.users.error.role_added_by_no_admin",
                "role added by a non admin user",
            )

    @dataclass(kw_only=True)
    class RoleAdded(AggregateEvent):
        event_type: str = "ROLE_ADDED"

        added_by: UserId
        role: Role

        def handle(self, aggregate: "User"):
            aggregate.roles.append(self.role)
            aggregate.mark_modified_by(self.added_by)

    @dataclass
    class RemoveRoleCommand:
        removed_by: UserId
        role_to_delete: Role
        admin_check_handler: Callable[[UserId], bool]

    class RoleRemovedByNoAdmin(OptiakError):
        def __init__(self):
            super().__init__(
                "security.users.error.role_removed_by_no_admin",
                "role removed by a non admin user",
            )

    @dataclass(kw_only=True)
    class RoleRemoved(AggregateEvent):
        event_type: str = "ROLE_REMOVED"

        removed_by: UserId
        role: Role

        def handle(self, aggregate: "User"):
            aggregate.roles.remove(self.role)
            aggregate.mark_modified_by(self.removed_by)

    @dataclass
    class CreateUserCommand:
        next_id: Callable[[], str]
        name: str
        surname: str
        username: str
        password: str
        created_by: UserId

    @dataclass(kw_only=True)
    class UserCreated(AggregateEvent):
        event_type: str = "USER_CREATED"
        name: str
        surname: str
        username: str
        password: str
        created_by: UserId

        def handle(self, aggregate: "User"):
            aggregate.mark_created_by(self.created_by)
            aggregate.name = self.name
            aggregate.surname = self.surname
            aggregate.username = self.username
            aggregate.password = self.password

    id: UserId | None = field(default=None)
    name: str | None = field(default=None)
    surname: str | None = field(default=None)
    active: bool = field(default=False)
    username: str | None = field(default=None)
    password: str | None = field(default=None)
    roles: list[Role] = field(default_factory=list)

    @staticmethod
    def create(command: CreateUserCommand):
        return User(id=UserId(id=command.next_id()))\
            .append(User.UserCreated(
                created_by=command.created_by,
                name=command.name,
                surname=command.surname,
                username=command.username,
                password=command.password
            ))

    def _is_changed_by_same_user(self, changed_by: UserId):
        return self.id and self.id == changed_by

    def change_name(self, cmd: ChangeNameCommand):
        if not self._is_changed_by_same_user(cmd.changed_by):
            raise User.NotChangedBySameUserError()

        return self.append(User.NameChanged(name=cmd.name, changed_by=cmd.changed_by))

    def change_password(self, cmd: ChangePasswordCommand):
        if not self._is_changed_by_same_user(cmd.changed_by):
            raise User.NotChangedBySameUserError()

        if not cmd.is_new_password_repeated_correct():
            raise User.RepeatedPasswordNotCorrect()

        return self.append(
            User.PasswordChanged(
                changed_by=cmd.changed_by,
                new_password=Sensitive(
                    cmd.new_password_hashing_handler(cmd.new_password)
                ),
            )
        )

    def add_role(self, cmd: AddRoleCommand) -> "User":
        if not cmd.admin_check_handler(cmd.added_by):
            raise User.RoleAddedByNoAdmin()

        if cmd.role_to_add in self.roles:
            return self

        return self.append(User.RoleAdded(added_by=cmd.added_by, role=cmd.role_to_add))

    def remove_role(self, cmd: RemoveRoleCommand) -> "User":
        if not cmd.admin_check_handler(cmd.removed_by):
            raise User.RoleRemovedByNoAdmin()

        if cmd.role_to_delete in self.roles:
            return self.append(
                User.RoleRemoved(role=cmd.role_to_delete, removed_by=cmd.removed_by)
            )

        return self
