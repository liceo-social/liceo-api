from liceo.infra.adapters.rest.endpoints import RestGroupSpec, open_api_permissions
from liceo.security.common.adapters.di import has_permission
from . import permissions

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
def list(requester: object, service: object):
    pass


@router.get(
    path="/{id}",
    summary="Shows a specific role detail",
    dependencies=[has_permission(permissions.ROLES_SHOW)],
    openapi_extra={**open_api_permissions([permissions.ROLES_SHOW])}
)
def show(request: object, service: object):
    pass


@router.post(
    path="/",
    summary="Creates a new role",
    dependencies=[has_permission(permissions.ROLES_CREATE)],
    openapi_extra={**open_api_permissions([permissions.ROLES_CREATE])}
)
def create(request: object, service: object):
    pass


@router.put(
    path="/{id}/name",
    summary="Changes role name",
    dependencies=[has_permission(permissions.ROLES_MODIFY)],
    openapi_extra={**open_api_permissions([permissions.ROLES_MODIFY])}
)
def change_name(request: object, service: object):
    pass


@router.put(
    path="/{id}/permissions",
    summary="Modify which permissions are attached to the role",
    dependencies=[has_permission(permissions.ROLES_MODIFY)],
    openapi_extra={**open_api_permissions([permissions.ROLES_MODIFY])}
)
def upate_permissions(request: object, service: object):
    pass
