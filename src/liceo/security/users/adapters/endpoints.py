from liceo.infra.adapters.rest.endpoints import RestGroupSpec, open_api_permissions
from liceo.security.common.adapters.di import has_permission
from . import di, responses, permissions

specs = RestGroupSpec(
    name="USERS",
    path="/users",
    description="Operations for managing users",
)

router = specs.create_router()


@router.get(
    path="/",
    summary="Allows admins to list and filters users",
    dependencies=[has_permission(permissions.USERS_LIST)],
    openapi_extra={**open_api_permissions([permissions.USERS_LIST])}
)
def list_users(
    request: di.FilteringUsersRequestDependency,
    service: di.UsersServiceDependency
) -> responses.ListUsersResponse:
    return responses.ListUsersResponse.from_dto(dto=service.list(request.toDTO()))


@router.get(
    path="/{id}",
    summary="Allows admins to show a specific user",
    dependencies=[has_permission(permissions.USERS_SHOW)],
    openapi_extra={**open_api_permissions([permissions.USERS_SHOW])}
)
def show(
    request: di.ShowUserRequestDependency,
    service: di.UsersServiceDependency
) -> responses.ShowUserResponse | None:
    return responses.ShowUserResponse.from_dto(service.get_user(request.to_dto()))


@router.post(
    path="/",
    summary="Allows admins to create a new user",
    dependencies=[has_permission(permissions.USERS_CREATE)],
    openapi_extra={**open_api_permissions([permissions.USERS_CREATE])}
)
def create_user(
    request: di.CreateUserRequestDependency,
    service: di.UsersServiceDependency
) -> responses.CreateUserResponse:
    return responses.CreateUserResponse.from_user(service.create_user(request.to_input()))


@router.put(
    path="/{id}",
    summary="Updates user's basic details",
    dependencies=[has_permission(permissions.USERS_UPDATE_DETAILS)],
    openapi_extra={**open_api_permissions([permissions.USERS_UPDATE_DETAILS])}
)
def update_user(
    request: di.UpdateUserRequestDependency,
    service: di.UsersServiceDependency
) -> responses.UpdateUserResponse | None:
    return responses.UpdateUserResponse.from_user(service.update_user(request.to_input()))


@router.put(
    path="/{id}/security",
    summary="Updates user's security params (account blocked, expired...)",
    dependencies=[has_permission(permissions.USERS_UPDATE_SECURITY)],
    openapi_extra={**open_api_permissions([permissions.USERS_UPDATE_SECURITY])}
)
def update_security_properties(
    request: di.UpdateSecurityRequestDependency,
    service: di.UsersServiceDependency
) -> responses.UpdatedSecurityResponse | None:
    return responses.UpdatedSecurityResponse.from_dto(service.update_security(request.to_input()))


@router.put(
    path="/{id}/password",
    summary="Updates user's password",
    dependencies=[has_permission(permissions.USERS_UPDATE_PASSWORD)],
    openapi_extra={**open_api_permissions([permissions.USERS_UPDATE_PASSWORD])}
)
def update_password(
    request: di.UpdatePasswordRequestDependency,
    service: di.UsersServiceDependency
) -> responses.UpdatePasswordResponse | None:
    return responses.UpdatePasswordResponse.from_user(service.update_password(request.to_input()))
