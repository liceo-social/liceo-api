from dataclasses import dataclass
from liceo.labs.db.core import AbstractService, managed_service, transactional
from liceo.labs.sherlock.application.service import EventStoreService
from liceo.people.contacts.application.service import PersonContactService
from liceo.people.identifications.application.service import PersonIdentificationService
from ..application import service, dtos, repository
from ..domain import entities
from . import mappers


@dataclass
@managed_service
class DatabasePersonService(service.PersonService, AbstractService):
    people: repository.PersonRepository
    contacts: PersonContactService
    identifications: PersonIdentificationService
    event_store: EventStoreService

    @transactional()
    def save_person(self, dto: dtos.CreatePersonDTO) -> entities.Person | None:
        # TODO: projects
        is_responsible_from_projects = False
        # creating person entity
        person = entities.Person.create(
            mappers.Create.from_dto_to_create_person_command(
                id=self.people.generate_id(),
                dto=dto,
                is_responsible_from_projects=is_responsible_from_projects
            )
        )
        saved = self.people.save_person(person)
        self.event_store.append(person)
        # saving emergency contact
        self.contacts.save_contact(
            mappers.Create.from_person_to_create_emergency_dto(person))
        # saving main id
        main_id = mappers.Create.from_person_to_create_identification_dto(person)
        if (main_id):
            self.identifications.save_identification(main_id)
        # return registered person
        return saved
