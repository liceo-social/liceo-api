from ..domain import entities, vo
from ..application import dtos
from liceo.people.identifications.application.dtos import CreatePersonIdentificationDTO
from liceo.people.contacts.application.dtos import CreatePersonContactDTO


class Create:
    @staticmethod
    def from_dto_to_create_person_command(
        id: vo.PersonId,
        dto: dtos.CreatePersonDTO,
        is_responsible_from_projects: bool
    ):
        return entities.Person.CreatePersonCommand(
            id=id,
            name=dto.name,
            surname=dto.surname,
            photo=dto.photo,
            alias=dto.alias,
            birthdate=dto.birthdate,
            sex=vo.Sex(dto.sex),
            genre=vo.Genre(dto.genre),
            main_id=Create.from_dto_to_identification(dto),
            emergency_contact=Create.from_dto_to_emergency_contact(dto),
            projects=[vo.ProjectId(p) for p in dto.projects],
            responsible=vo.UserId(dto.responsible),
            is_responsible_from_projects=is_responsible_from_projects,
            created_by=vo.UserId(dto.created_by)
        )

    @staticmethod
    def from_dto_to_identification(dto: dtos.CreatePersonDTO):
        if not (dto.official_id_type and dto.official_id_value):
            return

        return vo.Identification(
            type=dto.official_id_type,
            value=dto.official_id_value,
            expiration_date=dto.official_id_expiration_date
        )

    @staticmethod
    def from_dto_to_emergency_contact(dto: dtos.CreatePersonDTO):
        return vo.EmergencyContact(
            type=vo.ContactType(dto.emergency_contact_type),
            value=dto.emergency_contact_value,
            relationship=vo.ContactRelationship(dto.emergency_contact_relationship),
            notes=dto.emergency_contact_notes
        )

    @staticmethod
    def from_person_to_create_identification_dto(person: entities.Person) -> CreatePersonIdentificationDTO | None:
        if person.main_id:
            return CreatePersonIdentificationDTO(
                person_id=person.id.id,
                type=person.main_id.type,
                value=person.main_id.value,
                created_by=person.created_by.id,
                is_main_id=True,
                expiration_date=person.main_id.expiration_date
            )

    @staticmethod
    def from_person_to_create_emergency_dto(person: entities.Person) -> CreatePersonContactDTO:
        return CreatePersonContactDTO(
            person_id=person.id.id,
            type=person.emergency_contact.type.value,
            value=person.emergency_contact.value,
            created_by=person.created_by.id,
            is_emergency=True,
            relationship=person.emergency_contact.relationship.value,
            notes=person.emergency_contact.notes
        )
