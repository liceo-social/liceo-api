from liceo.labs.poirot.core import Repository, sql
from liceo.security.authentication.domain.vo import UserId
from ..application.repository import AuthenticationRepository


class PoirotAuthenticationRepository(AuthenticationRepository, Repository):
    @sql(lambda id: UserId(id=id))
    def find_user_by_credentials(self, username: str, password: str) -> UserId | None:
        pass
