from typing import Annotated
from fastapi import Depends
from liceo.security.common.application.service import SecurityService

# ----- COMMON


def security_service():
    return SecurityService()


SecurityServiceDependency = Annotated[SecurityService, Depends(security_service)]
