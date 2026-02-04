from datetime import datetime
from dataclasses import dataclass
from liceo.labs.sherlock.core import Aggregate, AggregateEvent
from liceo.security.common.domain.errors import AuthenticationException
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
        authentication: Callable[[str, str], UserId | None]
        token_generator: Callable[[str], str]

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
    token: str
    last_authenticated: datetime

    @staticmethod
    def authenticate(cmd: AuthenticationCommand):
        if not cmd.username or len(cmd.username.strip()) < USERNAME_MIN_LENGTH:
            raise AuthenticationException()

        if not cmd.password or len(cmd.password.strip()) < PASSWORD_MIN_LENGTH:
            raise AuthenticationException()

        user_id = cmd.authentication(cmd.username, cmd.password)

        if (user_id is None):
            raise AuthenticationException()

        token = cmd.token_generator(cmd.username)

        return User(id=user_id)\
            .append(User.UserAuthenticated(username=cmd.username, token=token))
