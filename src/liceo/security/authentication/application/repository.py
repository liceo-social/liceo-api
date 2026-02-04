from abc import ABC, abstractmethod
from ..domain.vo import UserId


class AuthenticationRepository(ABC):
    @abstractmethod
    def find_user_by_credentials(self, username: str, password: str) -> UserId | None:
        pass
