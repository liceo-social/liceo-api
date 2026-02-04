from dataclasses import dataclass, field
from liceo.infra.domain.vo import Pagination
from ..domain.vo import UserDetails


@dataclass
class CreateUserCaseDTO:
    name: str
    surname: str
    username: str
    password: str
    roles: list[str]
    created_by: UserDetails


@dataclass
class FilterUsersDTO:
    name: str | None = field(default=None)
    order: tuple[str, bool] | None = field(default=None)
    pagination: Pagination = field(default_factory=lambda: Pagination())


@dataclass
class UserDTO:
    id: str
    name: str
    username: str
    total_count: int
