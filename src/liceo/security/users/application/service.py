from abc import abstractmethod
from liceo.labs.db.core import AbstractService
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from .dtos import CreateUserDTO, FilterUsersDTO, UserDTO, UpdateUserDetailsDTO, UpdatePasswordDTO


class AbstractUsersService(AbstractService):
    @abstractmethod
    def list(self, input: FilterUsersDTO) -> Paged[UserDTO]:
        pass

    @abstractmethod
    def create_user(self, input: CreateUserDTO) -> User:
        pass

    @abstractmethod
    def update_user(self, input: UpdateUserDetailsDTO) -> User | None:
        pass

    @abstractmethod
    def update_password(self, input: UpdatePasswordDTO) -> User | None:
        pass
