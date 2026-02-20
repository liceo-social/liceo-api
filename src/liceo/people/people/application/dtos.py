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
    # emergency contact
    emergency_contact_type: str
    emergency_contact_value: dict
    # projects
    projects: list[str]
    # responsible
    responsible: str
    # user
    created_by: str
