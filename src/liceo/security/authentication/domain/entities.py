from datetime import datetime
from dataclasses import dataclass
from liceo.labs.sherlock.core import Aggregate, AggregateEvent
from typing import Callable
from .vo import UserId, Authentication
from .errors import NotValidCredentials, NotFoundUser

PASSWORD_MIN_LENGTH = 8
USERNAME_MIN_LENGTH = 6  # a@a.uk


@dataclass(init=False)
class User(Aggregate[UserId]):
    @dataclass
    class AuthenticationCommand:
        username: str
        password: str
        authentication: Callable[[str, str], Authentication | None]

        def check_credentials(self):
            if not self.username or len(self.username.strip()) < USERNAME_MIN_LENGTH:
                raise NotValidCredentials()

            if not self.password or len(self.password.strip()) < PASSWORD_MIN_LENGTH:
                raise NotValidCredentials()

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
        cmd.check_credentials()
        authentication = cmd.authentication(cmd.username, cmd.password)

        if (authentication is None):
            raise NotFoundUser()

        return User(id=authentication.user_id)\
            .append(User.UserAuthenticated(username=cmd.username, token=authentication.token))
