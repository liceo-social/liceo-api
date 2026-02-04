from abc import abstractmethod
from liceo.infra.application.output import AbstractRepository
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from .dtos import FilterUsersDTO, UserDTO


class UsersRepository(AbstractRepository):
    @abstractmethod
    def filter_users(self, filter: FilterUsersDTO) -> Paged[UserDTO]:
        pass

    @abstractmethod
    def save_user(self, user: User) -> User:
        pass
