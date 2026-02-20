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


@dataclass
class EmergencyContact:
    type: str
    value: dict


@dataclass
class PersonIdentificationId(AggregateId):
    id: str


@dataclass
class Identification:
    type: str
    value: str


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


class EmergencyContactType(Enum):
    PHONE = "PHONE"
    MOBILE = "MOBILE"
    EMAIL = "EMAIL"


@dataclass
class BasicDetails:
    name: str
    surname: str
    photo: str | None
    alias: str | None
    birthdate: datetime
    sex: Sex
    genre: Genre
