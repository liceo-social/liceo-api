from typing import Annotated
from fastapi import Depends, HTTPException

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


CreatePermissionRequest = Annotated[str, Depends(lambda: "")]
CreatePermissionServiceDependency = Annotated[str, Depends(lambda: "")]

ModifyPermissionRequest = Annotated[str, Depends(lambda: "")]
ModifyPermissionServiceDependency = Annotated[str, Depends(lambda: "")]

DeletePermissionRequest = Annotated[str, Depends(lambda: "")]
DeletePermissionServiceDependency = Annotated[str, Depends(lambda: "")]
