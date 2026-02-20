from ..domain import entities, vo
from ..application import dtos


class Create:
    @staticmethod
    def from_dto_to_identification(dto: dtos.CreatePersonDTO):
        if not (dto.official_id_type and dto.official_id_value):
            return

        return vo.Identification(
            type=dto.official_id_type,
            value=dto.official_id_value
        )

    @staticmethod
    def from_dto_to_emergency_contact(dto: dtos.CreatePersonDTO):
        return vo.EmergencyContact(
            type=dto.emergency_contact_type,
            value=dto.emergency_contact_value
        )

    @staticmethod
    def from_person_to_create_identification_command(id: vo.PersonIdentificationId, person: entities.Person):
        if person.main_id:
            return entities.PersonIdentification.CreateIdCommand(
                person_id=person.id.id,
                id=id,
                type=person.main_id.type,
                value=person.main_id.value,
                created_by=person.created_by.id,
                is_main_id=True
            )

    @staticmethod
    def from_person_to_create_emergency_command(id: vo.PersonContactId, person: entities.Person):
        return entities.PersonContact.CreateContactCommand(
            id=id,
            person_id=person.id.id,
            type=person.emergency_contact.type,
            value=person.emergency_contact.value,
            created_by=person.created_by.id,
            is_emergency=True
        )
