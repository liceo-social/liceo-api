from liceo.infra.adapters.rest.endpoints import RestGroupSpec, open_api_permissions
from liceo.security.common.adapters.di import has_permission
from .responses import CreateUserResponse, ListUsersResponse, UpdateUserResponse, UpdatePasswordResponse
from .permissions import USERS_LIST, USERS_CREATE, USERS_UPDATE_DETAILS, USERS_UPDATE_PASSWORD
from .di import (
    UsersServiceDependency,
    CreateUserRequestDependency,
    FilteringUsersRequestDependency,
    UpdateUserRequestDependency,
    UpdatePasswordRequestDependency
)

specs = RestGroupSpec(
    name="USERS",
    path="/admin/users",
    description="Operations for managing users",
)

router = specs.create_router()


@router.get(
    path="/",
    summary="Allows admins to list and filters users",
    dependencies=[has_permission(USERS_LIST)],
    openapi_extra={**open_api_permissions([USERS_LIST])}
)
def list_users(
    request: FilteringUsersRequestDependency,
    service: UsersServiceDependency
) -> ListUsersResponse:
    return ListUsersResponse.fromDTO(dto=service.list(request.toDTO()))


@router.post(
    path="/",
    summary="Allows admins to create a new user",
    dependencies=[has_permission(USERS_CREATE)],
    openapi_extra={**open_api_permissions([USERS_CREATE])}
)
def create_user(
    request: CreateUserRequestDependency,
    service: UsersServiceDependency
) -> CreateUserResponse:
    return CreateUserResponse.from_user(service.create_user(request.to_input()))


@router.put(
    path="/{id}",
    summary="Updates user's basic details",
    dependencies=[has_permission(USERS_UPDATE_DETAILS)],
    openapi_extra={**open_api_permissions([USERS_UPDATE_DETAILS])}
)
def update_user(
    request: UpdateUserRequestDependency,
    service: UsersServiceDependency
) -> UpdateUserResponse | None:
    return UpdateUserResponse.from_user(service.update_user(request.to_input()))


@router.put(
    path="/password/{id}",
    summary="Updates user's password",
    dependencies=[has_permission(USERS_UPDATE_PASSWORD)],
    openapi_extra={**open_api_permissions([USERS_UPDATE_PASSWORD])}
)
def update_password(
    request: UpdatePasswordRequestDependency,
    service: UsersServiceDependency
) -> UpdatePasswordResponse | None:
    return UpdatePasswordResponse.from_user(service.update_password(request.to_input()))
