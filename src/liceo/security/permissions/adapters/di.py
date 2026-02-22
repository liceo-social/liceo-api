from typing import Annotated
from fastapi import Depends, Query
from liceo.infra.adapters.di import ConnectionFactoryDependency, ConnectionManagerDependency, TransactionManagerDependency
from . import requests, repository, service
from ..application.service import PermissionsService
from ..application.repository import PermissionsRepository

FilterPermissionsRequestDependency = Annotated[requests.FilterPermissionsRequest, Query(
)]


def create_permissions_repository(factory: ConnectionFactoryDependency):
    return repository.SQLPermissionsRepository(factory=factory)


FilterPermissionsRepositoryDependency = Annotated[PermissionsRepository, Depends(
    create_permissions_repository)]


def create_permissions_service(
    connection_manager_dependency: ConnectionManagerDependency,
    transaction_manager_dependency: TransactionManagerDependency,
    permissions_repository: FilterPermissionsRepositoryDependency
):
    return service.DatabasePermissionService(
        connection_manager_factory=connection_manager_dependency,
        transaction_manager_factory=transaction_manager_dependency,
        permissions=permissions_repository
    )


PermissionsServiceDependency = Annotated[PermissionsService, Depends(
    create_permissions_service)]
