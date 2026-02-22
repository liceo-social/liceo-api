from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from liceo.labs.sherlock.domain.entities import AggregateId


@dataclass
class PersonId(AggregateId):
    id: str


@dataclass
class UserId(AggregateId):
    id: str


@dataclass
class PersonContactId(AggregateId):
    id: str


@dataclass
class ProjectId(AggregateId):
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


@dataclass
class EmergencyContact:
    type: ContactType
    relationship: ContactRelationship
    value: str
    notes: str | None


@dataclass
class PersonIdentificationId(AggregateId):
    id: str


class IdentificationType(Enum):
    NATIONAL_ID = "NATIONAL_ID"
    PASSPORT = "PASSPORT"
    HEALTH_ID = "HEALTH_ID"
    OTHER = "OTHER"


@dataclass
class Identification:
    type: str
    value: str
    expiration_date: datetime | None


class Sex(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Genre(Enum):
    HETERO = "HETERO"
    NO_BINARY = "NO_BINARY"
    LESBIAN = "LESBIAN"
    GAY = "GAY"
    TRANS = "TRANS"
    BISEXUAL = "BISEXUAL"
    INTERSEXUAL = "INTERSEXUAL"
    PLUS = "PLUS"
    UNDEFINED = "UNDEFINED"


@dataclass
class BasicDetails:
    name: str
    surname: str
    photo: str | None
    alias: str | None
    birthdate: datetime
    sex: Sex
    genre: Genre
