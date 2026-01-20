from dataclasses import dataclass


@dataclass(frozen=True)
class PermissionId:
    id: str


@dataclass
class UserId:
    id: str


@dataclass
class RoleId:
    id: str
