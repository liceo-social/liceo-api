from dataclasses import dataclass
from liceo.security.common.application.service import SecurityService
from liceo.infra.application.output import EventStore
from liceo.labs.db.core import AbstractService, ManagedService, transactional
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from ..domain.vo import UserId
from .dtos import CreateUserCaseDTO, FilterUsersDTO, UserDTO
from .repository import UsersRepository


@ManagedService
class UsersService(AbstractService):
    repository: UsersRepository
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
            surname=input.surname,
            username=input.username,
            password=self.security.hash_passw(input.password),
            roles=input.roles,
            created_by=UserId(id=input.created_by.id)
        )
        saved_user = self.repository.save_user(User.create(command))
        self.event_store.append(saved_user)
        return saved_user
