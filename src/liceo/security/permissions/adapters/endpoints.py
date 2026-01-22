from liceo.infra.adapters.rest.endpoints import RestGroupSpec
from liceo.security.permissions.adapters import di
from liceo.security.permissions.domain.permissions import (
    PERMISSION_LIST,
    PERMISSION_CREATE,
    PERMISSION_DELETE,
    PERMISSION_MODIFY
)

specs = RestGroupSpec(
    name="PERMISSIONS",
    path="/auth/permissions",
    description="Operations for maging permissions",
)

router = specs.create_router()


@router.get(
    path="/",
    dependencies=[di.has_permission(PERMISSION_LIST)]
)
def list(
    userCtx: di.UserContext,
    request: di.ListPermissionsRequest,
    service: di.ListPermissionsServiceDependency
):
    pass


@router.post(
    path="/",
    dependencies=[di.has_permission(PERMISSION_CREATE)]
)
def create(
    userCtx: di.UserContext,
    request: di.CreatePermissionRequest,
    service: di.CreatePermissionServiceDependency
):
    pass


@router.put(
    path="/",
    dependencies=[di.has_permission(PERMISSION_MODIFY)]
)
def modify(
    userCtx: di.UserContext,
    request: di.ModifyPermissionRequest,
    service: di.ModifyPermissionServiceDependency
):
    pass


@router.delete(
    path="/",
    dependencies=[di.has_permission(PERMISSION_DELETE)]
)
def delete(
    userCtx: di.UserContext,
    request: di.DeletePermissionRequest,
    service: di.DeletePermissionServiceDependency
):
    pass
