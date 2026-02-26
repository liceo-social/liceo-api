from typing import Annotated
from fastapi import Depends
from liceo.infra.adapters.di import ConnectionFactoryDependency, ConnectionManagerDependency, TransactionManagerDependency, EventStoreDependency
from .repository import SQLContactRepository
from .service import DatabaseAwarePersonContactService
from ..application.repository import PersonContactRepository
from ..application.service import PersonContactService

# ----- REPOSITORIES


def create_person_contact_repository(factory: ConnectionFactoryDependency):
    return SQLContactRepository(factory=factory)


PersonContactRepositoryDependency = Annotated[PersonContactRepository, Depends(
    create_person_contact_repository)]


# ----- SERVICES

def create_person_contact_service(
        repository: PersonContactRepositoryDependency,
        transaction_manager_factory: TransactionManagerDependency,
        connection_manager_factory: ConnectionManagerDependency,
        event_store: EventStoreDependency
) -> PersonContactService:
    return DatabaseAwarePersonContactService(
        repository=repository,
        transaction_manager_factory=transaction_manager_factory,
        connection_manager_factory=connection_manager_factory,
        event_store=event_store
    )


PersonContactServiceDependency = Annotated[PersonContactService, Depends(
    create_person_contact_service)]
