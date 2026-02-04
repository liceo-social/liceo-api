from dataclasses import dataclass
from liceo.security.common.application.service import SecurityService
from liceo.infra.application.output import EventStore
from ..domain.entities import User
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
                authentication=self.repository.find_user_by_credentials,
                token_generator=self.security.generate_token
            )
        )

        self.event_store.append(authenticated)
        return authenticated.token
