from dataclasses import dataclass
from ..domain import entities


@dataclass
class PersonDetailsResponse:
    name: str
    surname: str


@dataclass
class EmergencyContactResponse:
    type: str
    value: str
    relationship: str
    notes: str | None


@dataclass
class MainIdentificationResponse:
    type: str
    value: str


@dataclass
class CreatePersonResponse:
    id: str
    version: int
    details: PersonDetailsResponse
    emergency_contact: EmergencyContactResponse
    main_id: MainIdentificationResponse | None

    @staticmethod
    def from_person(person: entities.Person | None):
        if not person:
            return

        response = CreatePersonResponse(
            id=person.id.id,
            version=person._version,
            details=PersonDetailsResponse(
                name=person.basic_details.name,
                surname=person.basic_details.surname
            ),
            emergency_contact=EmergencyContactResponse(
                type=person.emergency_contact.type.value,
                value=person.emergency_contact.value,
                relationship=person.emergency_contact.relationship.value,
                notes=person.emergency_contact.notes
            ),
            main_id=None
        )

        if person.main_id:
            response.main_id = MainIdentificationResponse(
                type=person.main_id.type,
                value=person.main_id.value
            )

        return response
