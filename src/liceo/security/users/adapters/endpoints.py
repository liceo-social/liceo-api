from liceo.infra.adapters.rest.endpoints import RestGroupSpec, open_api_permissions
from liceo.security.common.adapters.di import has_permission
from .di import UsersServiceDependency, CreateUserRequestDependency, FilteringUsersRequestDependency
from .responses import CreateUserResponse, ListUsersResponse
from .permissions import USERS_LIST, USERS_CREATE

specs = RestGroupSpec(
    name="USERS",
    path="/admin/users",
    description="Operations for maging a user in the system",
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
