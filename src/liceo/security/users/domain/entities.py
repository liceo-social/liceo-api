from dataclasses import dataclass, field
from typing import Callable

from liceo.infra.domain.entities import AuditableAggregate, VersionAwareCommand
from liceo.labs.sherlock.domain.entities import AggregateEvent, Sensitive
from liceo.security.users.domain import vo
from liceo.security.users.domain import errors


@dataclass(init=False)
class User(AuditableAggregate[vo.UserId, vo.UserId]):
    @dataclass
    class UpdateDetailsCommand(VersionAwareCommand):
        name: str
        photo: str | None
        surname: str
        username: str
        role: str
        changed_by_admin: bool
        changed_by: vo.UserId

    @dataclass(kw_only=True)
    class DetailsChanged(AggregateEvent):
        event_type: str = "USER_BASIC_DETAILS_CHANGED"
        name: str
        photo: str | None
        surname: str
        username: str
        role: str
        changed_by: vo.UserId

        def handle(self, aggregate: "User"):
            aggregate.mark_updated_by(self.changed_by)
            aggregate.photo = self.photo
            aggregate.name = self.name
            aggregate.surname = self.surname
            aggregate.username = self.username
            aggregate.roles = [self.role]

    @dataclass
    class ChangePasswordCommand(VersionAwareCommand):
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
            aggregate.mark_updated_by(self.changed_by)

    @dataclass
    class UpdateSecurityCommand(VersionAwareCommand):
        password_expired: bool
        account_active: bool
        account_blocked: bool
        account_expired: bool
        updated_by: vo.UserId
        updated_by_admin: bool

    @dataclass(kw_only=True)
    class SecurityUpdated(AggregateEvent):
        event_type: str = "USER_SECURITY_UPDATED"
        password_expired: bool
        account_active: bool
        account_blocked: bool
        account_expired: bool
        updated_by: vo.UserId

        def handle(self, aggregate: "User"):
            aggregate.password_expired = self.password_expired
            aggregate.account_active = self.account_active
            aggregate.account_blocked = self.account_blocked
            aggregate.account_expired = self.account_expired
            aggregate.mark_updated_by(self.updated_by)

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
            aggregate.photo = self.photo
            aggregate.surname = self.surname
            aggregate.username = self.username
            aggregate.roles = [self.role]

    # details
    name: str = field()
    surname: str = field()
    username: str = field()
    photo: str | None = field(default=None)
    active: bool = field(default=False)
    roles: list[str] = field(default_factory=list)
    # changed individually
    password: str | None = field(default=None)
    password_expired: bool = field(default=False)
    account_active: bool = field(default=False)
    account_blocked: bool = field(default=False)
    account_expired: bool = field(default=False)

    @staticmethod
    def create(cmd: CreateUserCommand):
        if (not cmd.created_by_admin):
            raise errors.AttemptedByNoAdmin()

        return User(id=vo.UserId(id=cmd.next_id()))\
            .append(User.UserCreated(
                event_by=cmd.created_by,
                created_by=cmd.created_by,
                name=cmd.name,
                photo=cmd.photo,
                surname=cmd.surname,
                username=cmd.username,
                role=cmd.role,
            ))

    def _is_changed_by_same_user(self, changed_by: vo.UserId):
        return self.id and self.id == changed_by

    def update_details(self, cmd: UpdateDetailsCommand):
        if not self.check_version_matches(cmd.expected_version):
            raise errors.EditedByOtherUser()

        if not (self._is_changed_by_same_user(cmd.changed_by) or cmd.changed_by_admin):
            raise errors.NotChangedBySameUserError()

        return self.append(
            User.DetailsChanged(
                event_by=cmd.changed_by,
                changed_by=cmd.changed_by,
                name=cmd.name,
                surname=cmd.surname,
                username=cmd.username,
                photo=cmd.photo,
                role=cmd.role
            )
        )

    def change_password(self, cmd: ChangePasswordCommand):
        if not self.check_version_matches(cmd.expected_version):
            raise errors.EditedByOtherUser()

        if not self._is_changed_by_same_user(cmd.changed_by):
            raise errors.NotChangedBySameUserError()

        if not cmd.is_new_password_repeated_correct():
            raise errors.RepeatedPasswordNotCorrect()

        if cmd.old_password is None or not cmd.old_password_check_handler(cmd.old_password):
            raise errors.OldPasswordNotCorrect()

        return self.append(
            User.PasswordChanged(
                event_by=cmd.changed_by,
                changed_by=cmd.changed_by,
                new_password=Sensitive(
                    cmd.new_password_hashing_handler(cmd.new_password)
                ),
            )
        )

    def update_security(self, cmd: UpdateSecurityCommand):
        if not self.check_version_matches(cmd.expected_version):
            raise errors.EditedByOtherUser()

        if not cmd.updated_by_admin:
            raise errors.AttemptedByNoAdmin()

        return self.append(
            User.SecurityUpdated(
                event_by=cmd.updated_by,
                updated_by=cmd.updated_by,
                account_active=cmd.account_active,
                account_blocked=cmd.account_blocked,
                account_expired=cmd.account_expired,
                password_expired=cmd.password_expired
            )
        )

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"

    @property
    def aggregate_type(self) -> str:
        return "USER"
