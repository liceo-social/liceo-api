from typing import Annotated
from fastapi import Depends

from liceo.infra.adapters.di import ConnectionDependency, EventStoreDependency
from liceo.security.common.adapters.di import SecurityServiceDependency

from .repositories import PoirotUsersRepository
from ..application.service import UsersService
from ..application.repository import UsersRepository


# ----- REPOSITORIES
def repository(connection: ConnectionDependency) -> UsersRepository:
    return PoirotUsersRepository(connection=connection)


RepositoryDependency = Annotated[UsersRepository, Depends(repository)]


# ---- SERVICES
def users_service(repository: RepositoryDependency, event_store: EventStoreDependency, security: SecurityServiceDependency) -> UsersService:
    return UsersService(
        db=repository,
        security=security,
        event_store=event_store
    )


UsersServiceDependency = Annotated[UsersService, Depends(users_service)]
