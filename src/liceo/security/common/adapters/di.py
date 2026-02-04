from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from liceo.infra.adapters.di import ConfigurationDependency
from liceo.security.common.application.service import SecurityService
from .requests import UserContextModel


def security_service(config: ConfigurationDependency):
    return SecurityService(config=config)


SecurityServiceDependency = Annotated[SecurityService, Depends(security_service)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/security/auth")

TokenRequest = Annotated[str, Depends(oauth2_scheme)]


# def get_dummy_user_details(token: TokenRequest):
def get_dummy_user_details():
    return UserContextModel(id="eZ6AuHsQHACU5GXZTxDTS9", username="john.doe@liceo.com", roles=["ROLE_USER"])


# def get_dummy_user_model(token: TokenRequest):
def get_dummy_user_model():
    return UserContextModel.empty()


UserInfo = Annotated[UserContextModel, Depends(get_dummy_user_details)]
# $2b$10$Yxoh.mrE75jD1U.U7dBYV.pPLkgh1pwpUKPXavugoFLuujp98Radu
