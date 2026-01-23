from liceo.infra.adapters.rest.endpoints import RestGroupSpec
from liceo.security.permissions.adapters import di
from liceo.security.permissions.application.cases.create_permission import CreatePermissionCase
from liceo.security.permissions.domain.permissions import (
    PERMISSION_LIST,
    PERMISSION_CREATE,
)

from .responses import CreatePermissionResponse

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
    request: di.CreatePermissionRequestDependency,
    service: di.CreatePermissionServiceDependency
) -> CreatePermissionResponse:
    saved = service.create_permission(
        CreatePermissionCase.Input(
            name=request.name,
            created_by=userCtx.user_id,
            description=request.description
        )
    )
    return CreatePermissionResponse.model_validate(saved)
