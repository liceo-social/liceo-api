from typing import Annotated
from fastapi import Depends, HTTPException
from liceo.security.permissions.application.cases.create_permission import CreatePermissionCase, CreatePermissionService
from liceo.security.permissions.application import ports
from .repository import PermissionMemoryRepository
from .infra import ShortIdGenerator, DummySecurityService
from .requests import CreatePermissionRequest


AdminUserContext = Annotated[str, Depends(lambda: "")]
AnonymousContext = Annotated[str, Depends(lambda: "")]


class UserContext:
    def __init__(self, user_id: str, permissions: set[str]):
        self.user_id = user_id
        self.permissions = permissions


def decode_and_verify_jwt():
    return {}


def get_current_user() -> UserContext:
    payload = decode_and_verify_jwt()  # signature, exp, etc.

    roles = payload["roles"]           # e.g. ["admin", "support"]

    permissions = set()
    for role in roles:
        permissions.update(ROLE_PERMISSION_MAP[role])

    return UserContext(
        user_id=payload["sub"],
        permissions=permissions
    )


def has_permission(permission: str):
    def dependency(user: UserContext = Depends(get_current_user)):
        if permission not in user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return True
    return Depends(dependency)


ListPermissionsRequest = Annotated[str, Depends(lambda: "")]
ListPermissionsServiceDependency = Annotated[str, Depends(lambda: "")]


def create_repository() -> PermissionMemoryRepository:
    return PermissionMemoryRepository()


PersistenceDependency = Annotated[PermissionMemoryRepository, Depends(
    create_repository)]


def create_id_generator() -> ports.GenerateIdPort:
    return ShortIdGenerator()


IdGeneratorDependency = Annotated[ports.GenerateIdPort, Depends(create_id_generator)]


def create_security_service() -> ports.SecurityPort:
    return DummySecurityService()


SecurityDependency = Annotated[ports.SecurityPort, Depends(create_security_service)]


def create_permission_service(
    id_generator_service: IdGeneratorDependency,
    security_service: SecurityDependency,
    repository: PersistenceDependency
) -> CreatePermissionCase:
    return CreatePermissionService(
        id_gen_port=id_generator_service,
        security_port=security_service,
        save_port=repository,
    )


CreatePermissionRequestDependency = Annotated[CreatePermissionRequest, Depends(
    CreatePermissionRequest)]
CreatePermissionServiceDependency = Annotated[CreatePermissionCase, Depends(
    create_permission_service)]
