from .repositories import FilterUsersDTO
from liceo.infra.adapters.rest.endpoints import RestGroupSpec
from .di import UsersServiceDependency
from .requests import CreateUserRequest, ListUsersRequest
from .responses import CreateUserResponse, ListUsersResponse

specs = RestGroupSpec(
    name="USERS",
    path="/admin/users",
    description="Operations for maging a user in the system",
)

router = specs.create_router()


@router.get("/")
def list_users(
        service: UsersServiceDependency
) -> ListUsersResponse:
    return ListUsersResponse.fromDTO(dto=service.list(FilterUsersDTO()))


@router.post("/")
def create_user(
    request: CreateUserRequest, service: UsersServiceDependency
) -> CreateUserResponse:
    return CreateUserResponse.from_user(service.create_user(request.to_input()))
