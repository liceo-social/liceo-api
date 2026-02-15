
from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import AggregateId


@dataclass
class UserId(AggregateId):
    id: str


@dataclass
class PermissionId(AggregateId):
    id: str
