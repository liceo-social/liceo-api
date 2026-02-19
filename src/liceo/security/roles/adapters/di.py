from typing import Annotated
from fastapi import Depends, Query, Path

from liceo.infra.adapters.di import ConnectionManagerDependency, TransactionManagerDependency, ConnectionFactoryDependency, EventStoreDependency
from .requests import ListRolesRequest, ShowRoleRequest
from .repository import SQLRolesRepository
from .service import DatabaseRolesService
from ..application.service import RolesService
from ..application.repository import RolesRepository

ListRequestDependency = Annotated[ListRolesRequest, Query()]


def create_roles_repository(factory: ConnectionFactoryDependency):
    return SQLRolesRepository(factory=factory)


RolesRepositoryDependency = Annotated[RolesRepository, Depends(create_roles_repository)]


def create_roles_service(
    connection_manager_factory: ConnectionManagerDependency,
    transaction_manager_factory: TransactionManagerDependency,
    repository: RolesRepositoryDependency,
    event_store: EventStoreDependency
):
    return DatabaseRolesService(
        connection_manager_factory=connection_manager_factory,
        transaction_manager_factory=transaction_manager_factory,
        roles=repository,
        event_store=event_store
    )


RolesServiceDependency = Annotated[RolesService, Depends(create_roles_service)]


def create_show_role_request(id: str = Path()):
    return ShowRoleRequest(id=id)


ShowRoleRequestDependency = Annotated[ShowRoleRequest,
                                      Depends(create_show_role_request)]
