from typing import Annotated
from fastapi import Depends
from liceo.infra.adapters.di import ConnectionFactoryDependency, ConnectionManagerDependency, TransactionManagerDependency, EventStoreDependency
from .repository import SQLIdentificationRepository
from .service import DatabaseAwarePersonIdentificationService
from ..application.repository import PersonIdentificationRepository
from ..application.service import PersonIdentificationService

# ----- REPOSITORIES


def create_identification_repository(factory: ConnectionFactoryDependency) -> PersonIdentificationRepository:
    return SQLIdentificationRepository(factory=factory)


IdentificationRepositoryDependency = Annotated[PersonIdentificationRepository, Depends(
    create_identification_repository)]

# ----- SERVICES


def create_person_identification_service(
        repository: IdentificationRepositoryDependency,
        transaction_manager_factory: TransactionManagerDependency,
        connection_manager_factory: ConnectionManagerDependency,
        event_store: EventStoreDependency
) -> PersonIdentificationService:
    return DatabaseAwarePersonIdentificationService(
        repository=repository,
        transaction_manager_factory=transaction_manager_factory,
        connection_manager_factory=connection_manager_factory,
        event_store=event_store
    )


PersonIdentificationServiceDependency = Annotated[PersonIdentificationService, Depends(
    create_person_identification_service)]
