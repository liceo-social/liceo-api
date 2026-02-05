from liceo.infra.adapters.rest.endpoints import RestGroupSpec
from .di import AuthenticationServiceDependency
from .responses import TokenResponse
from .requests import OAuth2PasswordJSON
from ..application.dtos import CredentialsDTO

specs = RestGroupSpec(
    name="SECURITY",
    path="/auth",
    description="Operations accessing the system",
)

router = specs.create_router()


@router.post("/")
async def authenticate(
    request: OAuth2PasswordJSON,
    service: AuthenticationServiceDependency,
) -> TokenResponse | None:
    token = service.authenticate(
        CredentialsDTO(
            username=request.username,
            password=request.password
        )
    )

    return TokenResponse.from_token(token)
