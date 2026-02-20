from dataclasses import dataclass
from liceo.labs.db.core import AbstractService, managed_service, transactional
from liceo.labs.sherlock.application.service import EventStoreService
from ..application import service, dtos, repository
from ..domain import entities
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
            mappers.Create.from_dto_to_create_person_command(
                id=self.people.generate_id(),
                dto=dto,
                is_responsible_from_projects=is_responsible_from_projects
            )
        )
        saved = self.people.save_person(person)
        self.event_store.append(person)

        emergency_contact = entities.PersonContact.create(
            mappers.Create.from_person_to_create_emergency_command(
                id=self.contacts.generate_id(),
                person=person
            )
        )
        self.contacts.save_contact(emergency_contact)
        self.event_store.append(emergency_contact)

        main_id_cmd = mappers.Create.from_person_to_create_identification_command(
            id=self.identifications.generate_id(),
            person=person
        )

        if main_id_cmd:
            main_id = entities.PersonIdentification.create(main_id_cmd)
            self.identifications.save_identification(main_id)
            self.event_store.append(main_id)

        return saved
