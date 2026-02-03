from dataclasses import dataclass
from enum import Enum
from liceo.labs.sherlock.core import AggregateId


@dataclass
class UserId(AggregateId):
    id: str


@dataclass(frozen=True)
class UserDetails():
    id: str
    full_name: str
    username: str
    roles: list[str]


class Role(Enum):
    ROLE_USER = 1
    ROLE_ADMIN = 2
    ROLE_AUDITOR = 3
