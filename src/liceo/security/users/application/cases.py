from dataclasses import dataclass
from abc import ABC, abstractmethod
from ..domain.entities import User
from ..domain.vo import UserDetails


class CreateUserCase(ABC):
    @dataclass
    class Input:
        name: str
        surname: str
        username: str
        password: str
        roles: list[str]
        created_by: UserDetails

    @abstractmethod
    def create_user(self, input: Input) -> User:
        pass
