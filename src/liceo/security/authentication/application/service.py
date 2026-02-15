from abc import abstractmethod
from .dtos import CredentialsDTO


class AbstractAuthenticationService():
    @abstractmethod
    def authenticate(self, dto: CredentialsDTO) -> str | None:
        pass
