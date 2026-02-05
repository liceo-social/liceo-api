from typing import Annotated
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from liceo.infra.adapters.di import ConfigurationDependency, ConnectionFactoryDependency
from liceo.security.common.application.service import SecurityService
from .requests import UserContextModel
from .repositories import PoirotPermissionsRepository
from ..application.repositories import PermissionsRepository


def create_repository(factory: ConnectionFactoryDependency):
    return PoirotPermissionsRepository(factory=factory)


PermissionsRepositoryDependency = Annotated[PermissionsRepository, Depends(
    create_repository)]


def security_service(
    config: ConfigurationDependency,
    repository: PermissionsRepositoryDependency
):
    return SecurityService(config=config, repository=repository)


SecurityServiceDependency = Annotated[SecurityService, Depends(security_service)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/security/auth")

TokenRequest = Annotated[str, Depends(oauth2_scheme)]


def get_user_details(token: TokenRequest, security: SecurityServiceDependency):
    decoded = security.decode_token(token)
    return UserContextModel(username=decoded["username"], roles=decoded["roles"])


UserInfo = Annotated[UserContextModel, Depends(get_user_details)]


def has_permission(permission: str):
    def dependency(
        service: SecurityServiceDependency,
        user: UserInfo
    ):
        if not user or len(user.roles) == 0:
            print("============> NO ROLES")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        if not service.check_permission_in_roles(permission, user.roles):
            print("============> USER BUT NOT REQUIRED PERMISSIONS")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return True
    return Depends(dependency)
