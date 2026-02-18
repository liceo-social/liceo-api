from liceo.infra.adapters.rest.endpoints import RestGroupSpec
from typing import Annotated
from fastapi import Depends, Form
from .di import AuthenticationServiceDependency
from .responses import TokenResponse
from .requests import OAuth2PasswordJSON
from ..application.dtos import CredentialsDTO

specs = RestGroupSpec(
    name="AUTH",
    path="/auth",
    description="Operations accessing the system",
)

router = specs.create_router()


@router.post(
    path="/",
    summary="Authenticates a user passing credentials as JSON"
)
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


@router.post(
    path="/oauth2",
    summary="Authenticates a user passing credentials using form data (oauth2 compatible)"
)
async def authenticate_oauth(
    service: AuthenticationServiceDependency,
    request: Annotated[OAuth2PasswordJSON, Form()]
) -> TokenResponse | None:
    token = service.authenticate(
        CredentialsDTO(
            username=request.username,
            password=request.password
        )
    )

    return TokenResponse.from_token(token)
