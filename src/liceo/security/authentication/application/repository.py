from abc import ABC, abstractmethod
from ..domain.vo import UserAuthentication


class AuthenticationRepository(ABC):
    @abstractmethod
    def find_user_by_username(self, username: str) -> UserAuthentication | None:
        pass
