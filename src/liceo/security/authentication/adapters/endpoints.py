from liceo.infra.adapters.rest.endpoints import RestGroupSpec
from .di import AuthRequestDependency, AuthenticationServiceDependency
from .responses import TokenResponse
from .errors import AuthenticationException
from ..application.dtos import CredentialsDTO
specs = RestGroupSpec(
    name="SECURITY",
    path="/auth",
    description="Operations accessing the system",
)

router = specs.create_router()


@router.post("/")
async def authenticate(
    request: AuthRequestDependency,
    service: AuthenticationServiceDependency,
) -> TokenResponse | None:
    token = service.authenticate(CredentialsDTO(
        username=request.username,
        password=request.password
    )
    )

    if not token:
        raise AuthenticationException()

    return TokenResponse.from_token(token)
