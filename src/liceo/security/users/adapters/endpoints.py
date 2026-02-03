from liceo.infra.adapters.rest.endpoints import RestGroupSpec
from .di import CreateUserServiceDependency
from .requests import CreateUserRequest, ListUsersRequest
from .responses import CreateUserResponse, ListUsersResponse
from ..domain.entities import User

specs = RestGroupSpec(
    name="USERS",
    path="/admin/users",
    description="Operations for maging a user in the system",
)

router = specs.create_router()


@router.get("/")
def list_users(
        requester: object, request: ListUsersRequest, service: object
) -> ListUsersResponse:
    return ListUsersResponse(data=[])


@router.post("/")
def create_user(
    requester: object, request: CreateUserRequest, service: CreateUserServiceDependency
) -> CreateUserResponse:
    return CreateUserResponse(id="aloha")
