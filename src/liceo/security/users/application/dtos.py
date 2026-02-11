from datetime import datetime
from dataclasses import dataclass, field
from liceo.infra.domain.vo import Pagination
from liceo.security.common.application.dto import CurrentUserDTO


@dataclass
class CreateUserDTO:
    name: str
    surname: str
    username: str
    photo: str | None
    role: str
    created_by: CurrentUserDTO


@dataclass
class FilterUsersDTO:
    name: str | None = field(default=None)
    surname: str | None = field(default=None)
    username: str | None = field(default=None)
    order: tuple[str, bool] | None = field(default=None)
    pagination: Pagination = field(default_factory=lambda: Pagination())


@dataclass
class UserDTO:
    id: str
    full_name: str
    username: str
    photo: str
    roles: list[str]
    password_expired: bool
    account_active: bool
    account_blocked: bool
    account_expired: bool


@dataclass
class SaveUserImageDTO:
    user_id: str
    photo_id: str
    dimension: str
    created_by: str
    created_at: datetime


@dataclass
class UpdateUserDetailsDTO:
    id: str
    name: str
    surname: str
    username: str
    photo: str | None
    role: str
    updated_by: CurrentUserDTO


@dataclass
class UpdatePasswordDTO:
    id: str
    old_password: str
    new_password: str
    updated_by: CurrentUserDTO
