from dataclasses import dataclass
from liceo.labs.db.core import AbstractService, managed_service, transactional
from liceo.labs.sherlock.application.service import EventStoreService
from ..application import service, dtos, repository
from ..domain import entities, vo
from . import mappers


@dataclass
@managed_service
class DatabasePersonService(service.PersonService, AbstractService):
    people: repository.PersonRepository
    contacts: repository.PersonContactRepository
    identifications: repository.PersonIdentificationRepository
    event_store: EventStoreService

    @transactional()
    def save_person(self, dto: dtos.CreatePersonDTO) -> entities.Person | None:
        is_responsible_from_projects = False
        person = entities.Person.create(
            entities.Person.CreatePersonCommand(
                id=self.people.generate_id(),
                name=dto.name,
                surname=dto.surname,
                photo=dto.photo,
                alias=dto.alias,
                birthdate=dto.birthdate,
                sex=vo.Sex(dto.sex),
                genre=vo.Genre(dto.genre),
                main_id=mappers.Create.from_dto_to_identification(dto),
                emergency_contact=mappers.Create.from_dto_to_emergency_contact(dto),
                projects=[vo.ProjectId(p) for p in dto.projects],
                responsible=vo.UserId(dto.responsible),
                is_responsible_from_projects=is_responsible_from_projects,
                created_by=vo.UserId(dto.created_by)
            )
        )
        saved = self.people.save(person)
        self.event_store.append(person)

        emergency_contact = entities.PersonContact.create(
            mappers.Create.from_person_to_create_emergency_command(
                id=self.contacts.generate_id(),
                person=person
            )
        )
        self.contacts.save(emergency_contact)
        self.event_store.append(emergency_contact)

        main_id_cmd = mappers.Create.from_person_to_create_identification_command(
            id=self.identifications.generate_id(),
            person=person
        )

        if main_id_cmd:
            main_id = entities.PersonIdentification.create(main_id_cmd)
            self.identifications.save(main_id)
            self.event_store.append(main_id)

        return saved
