from typing import Annotated
from fastapi import Depends, Query, Path, Body

from liceo.infra.adapters.di import ConnectionManagerDependency, TransactionManagerDependency, ConnectionFactoryDependency, EventStoreDependency
from liceo.security.common.adapters.di import UserInfo
from .requests import ListRolesRequest, ShowRoleRequest, CreateRoleRequest, CreateRoleRequestDetails, UpdateRoleDetailsRequest, UpdateRoleDetails, UpdateRolePermissionsRequest, UpdateRolePermissionsDetails, DeleteRoleRequest, DeleteRoleDetails
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


def create_create_role_request(user: UserInfo, details: CreateRoleRequestDetails = Body()):
    return CreateRoleRequest(
        user=user,
        details=details
    )


CreateRoleRequestDependency = Annotated[CreateRoleRequest, Depends(
    create_create_role_request)]


def create_update_role_request(user: UserInfo, id: str = Path(), details: UpdateRoleDetails = Body()):
    return UpdateRoleDetailsRequest(id=id, user=user, details=details)


UpdateRoleDetailsRequestDependency = Annotated[UpdateRoleDetailsRequest, Depends(
    create_update_role_request)]


def create_update_permissions_request(user: UserInfo, id: str = Path(), details: UpdateRolePermissionsDetails = Body()):
    return UpdateRolePermissionsRequest(id=id, user=user, details=details)


UpdateRolePermissionsRequestDependency = Annotated[UpdateRolePermissionsRequest, Depends(
    create_update_permissions_request)]


def create_delete_role_request(
        user: UserInfo,
        id: str = Path(),
        details: DeleteRoleDetails = Body()
):
    return DeleteRoleRequest(id=id, details=details, deleted_by=user)


DeleteRoleRequestDependency = Annotated[DeleteRoleRequest, Depends(
    create_delete_role_request)]
