from typing import Annotated
from fastapi import Depends, Query, Body

from liceo.infra.adapters.di import ConnectionFactoryDependency, EventStoreDependency, ConnectionManagerDependency, TransactionManagerDependency
from liceo.security.common.adapters.di import SecurityServiceDependency, UserInfo

from .repositories import SQLUsersRepository, SQLUsersImagesRepository
from .requests import CreateUserRequest, FilteringUsersRequest, CreateUserFields
from ..application.service import UsersService
from ..application.repository import UsersRepository, UsersImagesRepository


# ----- REPOSITORIES
def repository(connection_factory: ConnectionFactoryDependency) -> UsersRepository:
    return SQLUsersRepository(factory=connection_factory)


RepositoryDependency = Annotated[UsersRepository, Depends(repository)]


def images_repository(connection_factory: ConnectionFactoryDependency) -> UsersImagesRepository:
    return SQLUsersImagesRepository(factory=connection_factory)


ImagesRepositoryDependency = Annotated[UsersImagesRepository, Depends(
    images_repository)]


# ---- SERVICES
def users_service(
    repository: RepositoryDependency,
    images_repository: ImagesRepositoryDependency,
    event_store: EventStoreDependency,
    security: SecurityServiceDependency,
    transaction_manager: TransactionManagerDependency,
    connection_manager: ConnectionManagerDependency
) -> UsersService:
    return UsersService(
        repository=repository,
        images_repository=images_repository,
        security=security,
        event_store=event_store,
        connection_manager=connection_manager,
        transaction_manager=transaction_manager
    )


UsersServiceDependency = Annotated[UsersService, Depends(users_service)]

# ------ REQUESTS

FilteringUsersRequestDependency = Annotated[FilteringUsersRequest, Query()]


def get_create_user_request(
    user: UserInfo,
    fields: CreateUserFields = Body()
):
    return CreateUserRequest(fields=fields, created_by=user)


CreateUserRequestDependency = Annotated[CreateUserRequest, Depends(
    get_create_user_request)]
