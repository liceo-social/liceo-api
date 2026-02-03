from dataclasses import dataclass
from liceo.security.common.application.service import SecurityService
from liceo.infra.application.output import EventStore
from ..domain.entities import User
from ..domain.vo import UserId
from .dtos import CreateUserCaseDTO
from .repository import UsersRepository


@dataclass
class UsersService:
    db: UsersRepository
    security: SecurityService
    event_store: EventStore

    def create_user(self, input: CreateUserCaseDTO) -> User:
        with self.db.with_transaction() as tx:
            command = User.CreateUserCommand(
                next_id=self.db.generate_id,
                check_permissions=lambda ps, uid: self.security.check_permissions(
                    ps, uid.id),
                name=input.name,
                surname=input.surname,
                username=input.username,
                password=self.security.hash_passw(input.password),
                roles=input.roles,
                created_by=UserId(id=input.created_by.id)
            )
            saved_user = tx.save_user(User.create(command))
            self.event_store.append(saved_user)
            return saved_user
