from dataclasses import dataclass
from liceo.security.common.application.service import SecurityService
from liceo.infra.application.output import EventStore
from ..domain.entities import User
from ..domain.vo import UserAuthentication
from .repository import AuthenticationRepository
from .dtos import CredentialsDTO


@dataclass
class AuthenticationService:
    repository: AuthenticationRepository
    security: SecurityService
    event_store: EventStore

    def authenticate(self, dto: CredentialsDTO) -> str | None:
        authenticated = User.authenticate(
            User.AuthenticationCommand(
                dto.username,
                dto.password,
                authentication=self._check_password,
                token_generator=self.security.generate_token
            )
        )

        self.event_store.append(authenticated)
        return authenticated.token

    def _check_password(self, username: str, password: str) -> UserAuthentication | None:
        user = self.repository.find_user_by_username(username)

        if (not user):
            return None

        if not self.security.verify(password, user.hashed):
            return None

        return user
