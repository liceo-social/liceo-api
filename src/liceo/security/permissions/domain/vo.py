
from dataclasses import dataclass
from liceo.labs.sherlock.core import AggregateId


@dataclass
class UserId(AggregateId):
    id: str


@dataclass
class PermissionId:
    id: str
