from abc import abstractmethod
from liceo.infra.application.output import AbstractRepository
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from .dtos import FilterUsersDTO, UserDTO, UpsertUserImageDTO


class UsersRepository(AbstractRepository):
    @abstractmethod
    def find_user_by_id(self, id: str) -> User | None:
        pass

    @abstractmethod
    def find_user_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    def find_user_by_token(self, token: str) -> User | None:
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

    @abstractmethod
    def update_password(self, user: User) -> User:
        pass

    @abstractmethod
    def update_security(self, user: User) -> User:
        pass


class UsersImagesRepository(AbstractRepository):
    @abstractmethod
    def save_user_image(self, dto: UpsertUserImageDTO) -> None:
        pass


class UsersOneTimeTokensRepository(AbstractRepository):
    @abstractmethod
    def delete_all_tokens_by_user_id(self, user_id: str) -> None:
        pass

    @abstractmethod
    def save_reset_hashed_token(self, user: User) -> None:
        pass
