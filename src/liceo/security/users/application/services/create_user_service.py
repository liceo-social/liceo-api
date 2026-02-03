from liceo.security.users.domain.entities import User
from liceo.infra.application.output import LedgerPort, TransactionManager
from ..cases import CreateUserCase
from ..ports import SavePort


class CreateUserService(CreateUserCase):
    def __init__(
        self,
        repository: SavePort,
        ledger: LedgerPort,
        tx_manager: TransactionManager
    ):
        self.repository = repository
        self.tx_manager = tx_manager
        self.ledger = ledger

    def create_user(self, cmd: User.CreateUserCommand) -> User | None:
        with self.tx_manager.create() as tx:
            created_user = User.create(cmd)
            saved_user = self.repository.save_user(
                name=created_user.name,
                surname=created_user.surname,
                username=created_user.username,
                password=created_user.password
            )
            self.ledger.persist(saved_user)
            return saved_user
