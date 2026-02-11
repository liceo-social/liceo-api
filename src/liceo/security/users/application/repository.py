from abc import abstractmethod
from liceo.infra.application.output import AbstractRepository
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from .dtos import FilterUsersDTO, UserDTO, SaveUserImageDTO


class UsersRepository(AbstractRepository):
    @abstractmethod
    def find_user_by_id(self, id: str) -> User | None:
        pass

    @abstractmethod
    def filter_users(self, filter: FilterUsersDTO) -> Paged[UserDTO]:
        pass

    @abstractmethod
    def save_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass


class UsersImagesRepository(AbstractRepository):
    @abstractmethod
    def save_user_image(self, dto: SaveUserImageDTO) -> None:
        pass
