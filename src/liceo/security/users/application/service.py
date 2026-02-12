from abc import abstractmethod
from liceo.labs.db.core import AbstractService
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from . import dtos


class AbstractUsersService(AbstractService):
    @abstractmethod
    def list(self, input: dtos.FilterUsersDTO) -> Paged[dtos.UserDTO]:
        pass

    @abstractmethod
    def create_user(self, input: dtos.CreateUserDTO) -> User:
        pass

    @abstractmethod
    def update_user(self, input: dtos.UpdateUserDetailsDTO) -> User | None:
        pass

    @abstractmethod
    def update_password(self, input: dtos.UpdatePasswordDTO) -> User | None:
        pass

    @abstractmethod
    def update_security(self, input: dtos.UpdateSecurityDTO) -> dtos.UpdatedSecurityDTO | None:
        pass
