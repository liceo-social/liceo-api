from enum import Enum
from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import AggregateId


@dataclass
class PersonContactId(AggregateId):
    id: str


@dataclass
class UserId(AggregateId):
    id: str


@dataclass
class PersonId(AggregateId):
    id: str


class ContactType(Enum):
    PHONE = "PHONE"
    MOBILE = "MOBILE"
    EMAIL = "EMAIL"
    SOCIAL = "SOCIAL"
    OTHER = "OTHER"


class ContactRelationship(Enum):
    FAMILY = "FAMILY"
    COUPLE = "COUPLE"
    FRIEND = "FRIEND"
    OWN = "OWN"
    OTHER = "OTHER"
