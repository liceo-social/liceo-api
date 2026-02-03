from liceo.security.users.domain.entities import User
from liceo.infra.application.output import LedgerPort, TransactionManager
from ..cases import CreateUserCase
from ..ports import SaveUserPort


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

    def create_user(self, cmd: User.CreateUserCommand) -> User | None:
        with self.tx_manager.create() as tx:
            saved_user = self.repository.save_user(User.create(cmd))
            self.ledger.persist(saved_user)
            return saved_user
