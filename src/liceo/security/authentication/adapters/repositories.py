from liceo.labs.db.sql import SQLRepository, sql
from ..domain.vo import UserId
from ..domain.entities import User
from ..application.repository import AuthenticationRepository


def row_to_user_authentication(row: dict) -> User | None:
    if not row:
        return None

    user = User(id=UserId(id=row["id"]))
    user._version = row["version"]
    user.password = row["hashed"]
    user.roles = row["roles"]
    user.username = row["username"]
    return user


class SQLAuthenticationRepository(AuthenticationRepository, SQLRepository):
    @sql(row_to_user_authentication)
    def find_user_by_username(self, username: str) -> User | None:
        return None

    @sql()
    def update_user_versioning(self, user_id: str, version: int) -> None:
        return None
