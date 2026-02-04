from typing import Annotated
from fastapi import Depends

from liceo.infra.adapters.di import ConnectionFactoryDependency, EventStoreDependency
from liceo.security.common.adapters.di import SecurityServiceDependency

from .repositories import PoirotUsersRepository
from ..application.service import UsersService
from ..application.repository import UsersRepository


# ----- REPOSITORIES
def repository(connection_factory: ConnectionFactoryDependency) -> UsersRepository:
    return PoirotUsersRepository(factory=connection_factory)


RepositoryDependency = Annotated[UsersRepository, Depends(repository)]


# ---- SERVICES
def users_service(repository: RepositoryDependency, factory: ConnectionFactoryDependency, event_store: EventStoreDependency, security: SecurityServiceDependency) -> UsersService:
    return UsersService(
        tx_factory=factory,
        repository=repository,
        security=security,
        event_store=event_store
    )


UsersServiceDependency = Annotated[UsersService, Depends(users_service)]
