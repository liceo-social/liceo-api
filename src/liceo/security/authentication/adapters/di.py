from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from liceo.security.common.adapters.di import SecurityServiceDependency
from liceo.infra.adapters.di import EventStoreDependency, ConnectionFactoryDependency
from ..application.repository import AuthenticationRepository
from ..application.service import AuthenticationService
from .repositories import PoirotAuthenticationRepository

AuthRequestDependency = Annotated[OAuth2PasswordRequestForm, Depends()]


def create_repository(factory: ConnectionFactoryDependency):
    return PoirotAuthenticationRepository(factory=factory)


AuthenticationRepositoryDependency = Annotated[AuthenticationRepository, Depends(
    create_repository)]


def create_authentication_service(
    repository: AuthenticationRepositoryDependency,
    security: SecurityServiceDependency,
    event_store: EventStoreDependency
):
    return AuthenticationService(
        repository=repository,
        security=security,
        event_store=event_store
    )


AuthenticationServiceDependency = Annotated[AuthenticationService, Depends(
    create_authentication_service)]
