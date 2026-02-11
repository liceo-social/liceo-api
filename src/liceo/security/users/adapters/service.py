from abc import abstractmethod
from dataclasses import dataclass
from liceo.security.common.application.service import SecurityService
from liceo.infra.application.output import EventStore
from liceo.labs.db.core import managed_service, transactional
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from ..domain.vo import UserId
from ..application.dtos import CreateUserCaseDTO, FilterUsersDTO, UserDTO, SaveUserImageDTO
from ..application.repository import UsersRepository, UsersImagesRepository
from ..application.service import AbstractUsersService


@dataclass
@managed_service
class UsersService(AbstractUsersService):
    repository: UsersRepository
    images_repository: UsersImagesRepository
    security: SecurityService
    event_store: EventStore

    def list(self, input: FilterUsersDTO) -> Paged[UserDTO]:
        return self.repository.filter_users(input)

    @transactional()
    def create_user(self, input: CreateUserCaseDTO) -> User:
        command = User.CreateUserCommand(
            next_id=self.repository.generate_id,
            created_by_admin=input.created_by.is_admin,
            name=input.name,
            photo=input.photo,
            surname=input.surname,
            username=input.username,
            role=input.role,
            created_by=UserId(id=input.created_by.id)
        )
        # saving user
        saved_user = self.repository.save_user(User.create(command))
        # saving user photo
        if (input.photo):
            self.images_repository.save_user_image(
                SaveUserImageDTO(
                    user_id=saved_user.id.id,
                    photo_id=input.photo,
                    dimension="original",
                    created_by=saved_user.created_by.id,
                    created_at=saved_user.created_at
                )
            )
        # saving event trail
        self.event_store.append(saved_user)
        return saved_user
