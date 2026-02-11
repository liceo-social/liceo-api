from abc import abstractmethod
from liceo.labs.db.core import AbstractService
from .dtos import CredentialsDTO


class AbstractAuthenticationService(AbstractService):
    @abstractmethod
    def authenticate(self, dto: CredentialsDTO) -> str | None:
        pass
