from dataclasses import dataclass, field
from typing import Callable

from liceo.infra.domain.entities import AuditableAggregate, PermissionAwareCommand
from liceo.labs.sherlock.core import AggregateEvent, Sensitive
from liceo.security.users.domain import vo
from liceo.security.users.domain import errors


@dataclass(init=False)
class User(AuditableAggregate[vo.UserId]):
    @dataclass
    class ChangeNameCommand:
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
    class ChangePasswordCommand:
        old_password: str | None
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
        role_to_add: str

    @dataclass(kw_only=True)
    class RoleAdded(AggregateEvent):
        event_type: str = "USER_ROLE_ADDED"
        added_by: vo.UserId
        role: str

        def handle(self, aggregate: "User"):
            aggregate.roles.append(self.role)
            aggregate.mark_modified_by(self.added_by)

    @dataclass
    class RemoveRoleCommand(PermissionAwareCommand[vo.UserId]):
        removed_by: vo.UserId
        role_to_delete: str
        admin_check_handler: Callable[[vo.UserId], bool]

    @dataclass(kw_only=True)
    class RoleRemoved(AggregateEvent):
        event_type: str = "USER_ROLE_REMOVED"
        removed_by: vo.UserId
        role: str

        def handle(self, aggregate: "User"):
            aggregate.roles.remove(self.role)
            aggregate.mark_modified_by(self.removed_by)

    @dataclass
    class CreateUserCommand:
        next_id: Callable[[], str]
        name: str
        photo: str | None
        surname: str
        username: str
        role: str
        created_by: vo.UserId
        created_by_admin: bool

    @dataclass(kw_only=True)
    class UserCreated(AggregateEvent):
        event_type: str = "USER_CREATED"
        name: str
        surname: str
        photo: str | None
        username: str
        role: str
        created_by: vo.UserId

        def handle(self, aggregate: "User"):
            aggregate.mark_created_by(self.created_by)
            aggregate.name = self.name
            aggregate.surname = self.surname
            aggregate.username = self.username
            aggregate.roles = [self.role]

    name: str = field()
    surname: str = field()
    username: str = field()
    password: str | None = field(default=None)
    photo: str | None = field(default=None)
    active: bool = field(default=False)
    roles: list[str] = field(default_factory=list)

    @staticmethod
    def create(cmd: CreateUserCommand):
        if (not cmd.created_by_admin):
            raise errors.AttemptedByNoAdmin()

        return User(id=vo.UserId(id=cmd.next_id()))\
            .append(User.UserCreated(
                created_by=cmd.created_by,
                name=cmd.name,
                photo=cmd.photo,
                surname=cmd.surname,
                username=cmd.username,
                role=cmd.role,
            ))

    def _is_changed_by_same_user(self, changed_by: vo.UserId):
        return self.id and self.id == changed_by

    def change_name(self, cmd: ChangeNameCommand):
        if not self._is_changed_by_same_user(cmd.changed_by):
            raise errors.NotChangedBySameUserError()

        return self.append(User.NameChanged(name=cmd.name, changed_by=cmd.changed_by))

    def change_password(self, cmd: ChangePasswordCommand):
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
        if not cmd.admin_check_handler(cmd.added_by):
            raise errors.AttemptedByNoAdmin()

        if cmd.role_to_add in self.roles:
            return self

        return self.append(User.RoleAdded(added_by=cmd.added_by, role=cmd.role_to_add))

    def remove_role(self, cmd: RemoveRoleCommand) -> "User":
        if not cmd.admin_check_handler(cmd.removed_by):
            raise errors.AttemptedByNoAdmin()

        if cmd.role_to_delete in self.roles:
            return self.append(
                User.RoleRemoved(role=cmd.role_to_delete, removed_by=cmd.removed_by)
            )

        return self
