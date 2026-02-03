from liceo.security.users.domain.entities import User
from liceo.infra.application.output import LedgerPort, TransactionManager
from ..cases import CreateUserCase
from ..ports import SaveUserPort
from ...domain.vo import UserId


class CreateUserService(CreateUserCase):
    def __init__(
        self,
        repository: SaveUserPort,
        ledger: LedgerPort,
        tx_manager: TransactionManager
    ):
        self.repository = repository
        self.tx_manager = tx_manager
        self.ledger = ledger

    def create_user(self, input: CreateUserCase.Input) -> User:
        with self.tx_manager.create() as tx:
            command = User.CreateUserCommand(
                next_id=lambda: "",  # TODO: central way of creating ids
                check_permissions=lambda ps, uid: "",  # TODO: link to common security service
                name=input.name,
                surname=input.surname,
                username=input.username,
                password="??????",  # TODO: link to common security service to hash passwords
                roles=input.roles,
                created_by=UserId(id=input.created_by.id)
            )
            saved_user = self.repository.save_user(User.create(command))
            self.ledger.persist(saved_user)
            return saved_user
