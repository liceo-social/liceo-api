from abc import ABC, abstractmethod
from ..domain.entities import User


class SaveUserPort(ABC):
    @abstractmethod
    def save_user(self, user: User) -> User:
        pass
