from typing import Annotated
from fastapi import Depends
from liceo.security.common.adapters.di import SecurityServiceDependency
from liceo.infra.adapters.di import EventStoreDependency, ConnectionFactoryDependency, ConnectionManagerDependency, TransactionManagerDependency
from ..application.repository import AuthenticationRepository
from .service import AuthenticationService
from .repositories import SQLAuthenticationRepository


def create_repository(factory: ConnectionFactoryDependency):
    return SQLAuthenticationRepository(factory=factory)


AuthenticationRepositoryDependency = Annotated[AuthenticationRepository, Depends(
    create_repository)]


def create_authentication_service(
    repository: AuthenticationRepositoryDependency,
    security: SecurityServiceDependency,
    event_store: EventStoreDependency,
    connection_manager: ConnectionManagerDependency,
    transaction_manager: TransactionManagerDependency
):
    return AuthenticationService(
        repository=repository,
        security=security,
        event_store=event_store,
        connection_manager=connection_manager,
        transaction_manager=transaction_manager
    )


AuthenticationServiceDependency = Annotated[AuthenticationService, Depends(
    create_authentication_service)]
