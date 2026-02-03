from abc import ABC, abstractmethod
from ..domain.entities import User


class CreateUserCase(ABC):
    @abstractmethod
    def create_user(self, cmd: User.CreateUserCommand) -> User:
        pass
