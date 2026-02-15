from dataclasses import dataclass
from enum import Enum
from liceo.labs.sherlock.domain.entities import AggregateId


@dataclass
class UserId(AggregateId):
    id: str


class Role(Enum):
    ROLE_USER = 1
    ROLE_ADMIN = 2
    ROLE_AUDITOR = 3
