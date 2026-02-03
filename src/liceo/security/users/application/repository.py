from abc import ABC, abstractmethod
from liceo.infra.application.output import AbstractRepository
from ..domain.entities import User


class UsersRepository(AbstractRepository):
    @abstractmethod
    def save_user(self, user: User) -> User:
        pass
