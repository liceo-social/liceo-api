from datetime import datetime
from dataclasses import dataclass


@dataclass
class CreatePersonDTO:
    # basic details
    name: str
    surname: str
    photo: str | None
    alias: str | None
    birthdate: datetime
    sex: str
    genre: str
    # official id
    official_id_type: str | None
    official_id_value: str | None
    official_id_expiration_date: datetime | None
    # emergency contact
    emergency_contact_type: str
    emergency_contact_value: str
    emergency_contact_relationship: str
    emergency_contact_notes: str | None
    # projects
    projects: list[str]
    # responsible
    responsible: str
    # user
    created_by: str
