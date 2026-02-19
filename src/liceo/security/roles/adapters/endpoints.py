from liceo.infra.adapters.rest.endpoints import RestGroupSpec, open_api_permissions
from liceo.security.common.adapters.di import has_permission
from . import permissions, di, responses

specs = RestGroupSpec(
    name="ROLES",
    path="/roles",
    description="Operations for managing roles",
)


router = specs.create_router()


@router.get(
    path="/",
    summary="List roles",
    dependencies=[has_permission(permissions.ROLES_LIST)],
    openapi_extra={**open_api_permissions([permissions.ROLES_LIST])}
)
def list_roles(
    request: di.ListRequestDependency,
    service: di.RolesServiceDependency
) -> responses.ListRolesResponses:
    return responses.ListRolesResponses.from_dto(service.list(request.to_pagination()))


@router.get(
    path="/{id}",
    summary="Shows a specific role detail",
    dependencies=[has_permission(permissions.ROLES_SHOW)],
    openapi_extra={**open_api_permissions([permissions.ROLES_SHOW])}
)
def show(
    request: di.ShowRoleRequestDependency,
    service: di.RolesServiceDependency
) -> responses.ShowRoleResponse | None:
    return responses.ShowRoleResponse.from_dto(service.show(request.to_dto()))


@router.post(
    path="/",
    summary="Creates a new role",
    dependencies=[has_permission(permissions.ROLES_CREATE)],
    openapi_extra={**open_api_permissions([permissions.ROLES_CREATE])}
)
def create(
    request: di.CreateRoleRequestDependency,
    service: di.RolesServiceDependency
) -> responses.CreateRoleResponse:
    return responses.CreateRoleResponse.from_dto(service.create_role(request.to_dto()))


@router.put(
    path="/{id}",
    summary="Changes role details (name, description)",
    dependencies=[has_permission(permissions.ROLES_UPDATE)],
    openapi_extra={**open_api_permissions([permissions.ROLES_UPDATE])}
)
def change_name(
    request: di.UpdateRoleDetailsRequestDependency,
    service: di.RolesServiceDependency
) -> responses.UpdateRoleDetailsResponse | None:
    return responses.UpdateRoleDetailsResponse.from_role(service.update_role_details(request.to_dto()))


@router.put(
    path="/{id}/permissions",
    summary="Modify which permissions are attached to the role",
    dependencies=[has_permission(permissions.ROLES_UPDATE)],
    openapi_extra={**open_api_permissions([permissions.ROLES_UPDATE])}
)
def upate_permissions(
    request: di.UpdateRolePermissionsRequestDependency,
    service: di.RolesServiceDependency
) -> responses.UpdateRolePermissionsResponse | None:
    return responses.UpdateRolePermissionsResponse.from_role(service.update_role_permissions(request.to_dto()))
