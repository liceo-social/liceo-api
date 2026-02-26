from datetime import datetime
from dataclasses import dataclass


@dataclass
class CreatePersonIdentificationDTO:
    person_id: str
    type: str
    value: str
    created_by: str
    is_main_id: bool
    expiration_date: datetime | None
