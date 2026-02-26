from dataclasses import dataclass


@dataclass
class CreatePersonContactDTO:
    person_id: str
    type: str
    value: str
    created_by: str
    is_emergency: bool
    relationship: str
    notes: str | None
