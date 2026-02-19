from dataclasses import dataclass


@dataclass
class ShowRoleDTO:
    id: str


@dataclass
class RoleDTO:
    id: str
    version: int
    name: str
    description: str


@dataclass
class PermissionDTO:
    id: str
    name: str
    description: str


@dataclass
class FullRoleDTO(RoleDTO):
    permissions: list[PermissionDTO]


@dataclass
class CreateRoleDTO:
    name: str
    description: str
    permissions: list[str]
    is_admin: bool
    created_by: str


@dataclass
class UpdateRoleDetailsDTO:
    id: str
    version: int
    name: str
    description: str
    is_admin: bool
    updated_by: str


@dataclass
class UpdateRolePermissionsDTO:
    id: str
    version: int
    permissions: list[str]
    is_admin: bool
    updated_by: str


@dataclass
class DeleteRoleDTO:
    id: str
    version: int
    is_admin: bool
    deleted_by: str
