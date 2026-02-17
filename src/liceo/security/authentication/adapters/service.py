from dataclasses import dataclass
from liceo.security.common.application.service import SecurityService
from liceo.security.common.domain.errors import AuthenticationException
from liceo.labs.sherlock.application.service import EventStoreService
from liceo.labs.db.core import managed_service, AbstractService, transactional
from ..domain.entities import User
from ..application.repository import AuthenticationRepository
from ..application.service import AbstractAuthenticationService
from ..application.dtos import CredentialsDTO


@dataclass
@managed_service
class AuthenticationService(AbstractAuthenticationService, AbstractService):
    repository: AuthenticationRepository
    security: SecurityService
    event_store: EventStoreService

    @transactional()
    def authenticate(self, dto: CredentialsDTO) -> str | None:
        user = self.repository.find_user_by_username(dto.username)

        if not user:
            raise AuthenticationException()

        authenticated = user.authenticate(
            User.AuthenticationCommand(
                dto.username,
                dto.password,
                password_matches=self.security.verify(dto.password, user.password),
                token_generator=self.security.generate_token
            )
        )
        self.repository.update_user_versioning(user.id.id, user._version)
        self.event_store.append(authenticated)
        return authenticated.token
