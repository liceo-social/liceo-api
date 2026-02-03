from abc import ABC, abstractmethod
from ..domain.entities import User


class SavePort(ABC):
    @abstractmethod
    def save_user(self, name: str, surname: str, username: str, password: str) -> User:
        pass
