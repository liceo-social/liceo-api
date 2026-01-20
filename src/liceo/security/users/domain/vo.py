from dataclasses import dataclass
from enum import Enum


@dataclass
class UserId:
    id: str


class Role(Enum):
    ROLE_USER = 1
    ROLE_ADMIN = 2
    ROLE_AUDITOR = 3
