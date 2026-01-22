from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from liceo.security.authentication.adapters.vo import UserContextModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/security/auth")


TokenRequest = Annotated[str, Depends(oauth2_scheme)]


def check_role(role: str):
    def anonymous():
        return UserContextModel.empty()

    def check_role_check(
        token: TokenRequest,
        service: GetCurrentUserDependency,
    ):
        current_user = service.get_current_user(token)
        if current_user and (role in current_user.roles):
            return UserContextModel(
                username=current_user.username, roles=current_user.roles
            )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if role == "ROLE_ANONYMOUS":
        return anonymous

    return check_role_check


ROLE_ANONYMOUS = Annotated[UserContextModel, Depends(check_role(Role.ROLE_ANONYMOUS))]


ROLE_USER = Annotated[UserContextModel, Depends(check_role(Role.ROLE_USER))]


ROLE_ADMIN = Annotated[UserContextModel, Depends(check_role(Role.ROLE_ADMIN))]
