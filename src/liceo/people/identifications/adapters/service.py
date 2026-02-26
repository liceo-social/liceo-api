from dataclasses import dataclass
from liceo.labs.db.core import AbstractService, managed_service, transactional
from liceo.labs.sherlock.application.service import EventStoreService
from liceo.people.identifications.application.dtos import CreatePersonIdentificationDTO
from liceo.people.identifications.domain.entities import PersonIdentification
from ..application.service import PersonIdentificationService
from ..application.repository import PersonIdentificationRepository


@dataclass
@managed_service
class DatabaseAwarePersonIdentificationService(PersonIdentificationService, AbstractService):
    repository: PersonIdentificationRepository
    event_store: EventStoreService

    @transactional()
    def save_identification(self, dto: CreatePersonIdentificationDTO) -> PersonIdentification:
        identification = PersonIdentification.create(
            PersonIdentification.CreateIdCommand(
                id=self.repository.generate_id(),
                person_id=dto.person_id,
                type=dto.type,
                value=dto.value,
                expiration_date=dto.expiration_date,
                created_by=dto.created_by,
                is_main_id=dto.is_main_id
            )
        )

        self.repository.save_identification(identification)
        self.event_store.append(identification)
        return identification
