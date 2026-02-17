from abc import ABC, abstractmethod
from ..domain.entities import User


class AuthenticationRepository(ABC):
    @abstractmethod
    def find_user_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    def update_user_versioning(self, user_id: str, version: int) -> None:
        pass
