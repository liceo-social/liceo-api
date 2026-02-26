from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import AggregateId


@dataclass
class UserId(AggregateId):
    id: str


@dataclass
class ProjectId(AggregateId):
    id: str


@dataclass
class ProjectMembershipId(AggregateId):
    id: str


@dataclass
class ProjectCoordinatorId(AggregateId):
    id: str


@dataclass
class PersonId(AggregateId):
    id: str
