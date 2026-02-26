from dataclasses import dataclass
from liceo.labs.sherlock.application.service import EventStoreService
from liceo.people.contacts.application.dtos import CreatePersonContactDTO
from liceo.people.contacts.domain.entities import PersonContact
from ..application.service import PersonContactService
from liceo.labs.db.core import AbstractService, managed_service, transactional
from ..application.repository import PersonContactRepository
from ..domain import entities


@dataclass
@managed_service
class DatabaseAwarePersonContactService(PersonContactService, AbstractService):
    repository: PersonContactRepository
    event_store: EventStoreService

    @transactional()
    def save_contact(self, dto: CreatePersonContactDTO) -> PersonContact:
        contact = entities.PersonContact.create(
            PersonContact.CreateContactCommand(
                id=self.repository.generate_id(),
                person_id=dto.person_id,
                type=dto.type,
                relationship=dto.relationship,
                value=dto.value,
                notes=dto.notes,
                is_emergency=dto.is_emergency,
                created_by=dto.created_by
            )
        )
        self.repository.save_contact(contact)
        self.event_store.append(contact)
        return contact
