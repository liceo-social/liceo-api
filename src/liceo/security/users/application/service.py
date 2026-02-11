from abc import abstractmethod
from liceo.labs.db.core import AbstractService
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from .dtos import CreateUserCaseDTO, FilterUsersDTO, UserDTO


class AbstractUsersService(AbstractService):
    @abstractmethod
    def list(self, input: FilterUsersDTO) -> Paged[UserDTO]:
        pass

    @abstractmethod
    def create_user(self, input: CreateUserCaseDTO) -> User:
        pass
