from datetime import datetime
from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import Aggregate, AggregateEvent
from liceo.security.authentication.domain.errors import AuthenticationException
from typing import Callable
from .vo import UserId

PASSWORD_MIN_LENGTH = 8
USERNAME_MIN_LENGTH = 6  # a@a.uk


@dataclass(init=False)
class User(Aggregate[UserId]):
    @dataclass
    class AuthenticationCommand:
        username: str
        password: str
        password_matches: bool
        token_generator: Callable[[str, list[str]], str]

    @dataclass(kw_only=True)
    class UserAuthenticated(AggregateEvent):
        event_type: str = "USER_AUTHENTICATED"
        username: str
        token: str

        def handle(self, aggregate: "User"):
            aggregate.username = self.username
            aggregate.token = self.token
            aggregate.last_authenticated = datetime.now()

    username: str
    password: str
    roles: list[str]
    token: str
    last_authenticated: datetime

    def authenticate(self, cmd: AuthenticationCommand):
        if not cmd.username or len(cmd.username.strip()) < USERNAME_MIN_LENGTH:
            raise AuthenticationException()

        if not cmd.password or len(cmd.password.strip()) < PASSWORD_MIN_LENGTH:
            raise AuthenticationException()

        if not cmd.password_matches:
            raise AuthenticationException()

        token = cmd.token_generator(self.id.id, self.roles)

        return self.append(User.UserAuthenticated(username=cmd.username, token=token))

    @property
    def aggregate_type(self) -> str:
        return "USER"
