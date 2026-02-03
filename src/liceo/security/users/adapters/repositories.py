from liceo.security.users.domain.entities import User
from liceo.labs.poirot.core import sql, Repository
from ..application.ports import SavePort


def save_user_mapper(result: dict) -> User:
    pass


class UserRepository(SavePort, Repository):
    @sql(save_user_mapper)
    def save_user(self, name: str, surname: str, username: str, password: str) -> User | None:
        pass
