from liceo.labs.db.sql import SQLRepository, sql
from liceo.security.authentication.domain.vo import UserAuthentication, UserId
from ..application.repository import AuthenticationRepository


def row_to_user_authentication(row: dict) -> UserAuthentication | None:
    if not row:
        return None

    return UserAuthentication(
        id=UserId(id=row["id"]),
        hashed=row["hashed"],
        roles=row["roles"],
        username=row["username"]
    )


class SQLAuthenticationRepository(AuthenticationRepository, SQLRepository):
    @sql(row_to_user_authentication)
    def find_user_by_username(self, username: str) -> UserAuthentication | None:
        return None
