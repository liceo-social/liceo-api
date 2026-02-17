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
    version: int
    full_name: str
    name: str
    surname: str
    username: str
    photo: str | None
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
    expected_version: int
    name: str
    surname: str
    username: str
    photo: str | None
    role: str
    updated_by: CurrentUserDTO


@dataclass
class UpdatePasswordDTO:
    id: str
    expected_version: int
    old_password: str
    new_password: str
    new_password_repeated: str
    updated_by: CurrentUserDTO


@dataclass
class UpdateSecurityDTO:
    id: str
    expected_version: int
    password_expired: bool
    account_active: bool
    account_blocked: bool
    account_expired: bool
    updated_by: CurrentUserDTO


@dataclass
class UpdatedSecurityDTO:
    version: int
    password_expired: bool
    account_active: bool
    account_blocked: bool
    account_expired: bool


@dataclass
class GetUserDTO:
    id: str
