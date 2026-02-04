from liceo.infra.adapters.rest.endpoints import RestGroupSpec
from .di import UsersServiceDependency, CreateUserRequestDependency, FilteringUsersRequestDependency
from .responses import CreateUserResponse, ListUsersResponse

specs = RestGroupSpec(
    name="USERS",
    path="/admin/users",
    description="Operations for maging a user in the system",
)

router = specs.create_router()


@router.get("/")
def list_users(
    request: FilteringUsersRequestDependency,
    service: UsersServiceDependency
) -> ListUsersResponse:
    return ListUsersResponse.fromDTO(dto=service.list(request.toDTO()))


@router.post("/")
def create_user(
    request: CreateUserRequestDependency,
    service: UsersServiceDependency
) -> CreateUserResponse:
    return CreateUserResponse.from_user(service.create_user(request.to_input()))
