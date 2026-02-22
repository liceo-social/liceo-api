from fastapi import Depends, Body
from typing import Annotated
from liceo.infra.adapters.di import ConnectionFactoryDependency, ConnectionManagerDependency, TransactionManagerDependency, EventStoreDependency
from liceo.security.common.adapters.di import UserInfo

from . import requests
from ..application import service, repository
from ..adapters.repository import SQLPersonRepository, SQLContactRepository, SQLIdentificationRepository
from ..adapters.service import DatabasePersonService

# --- REPOSITORIES


def create_person_repository(factory: ConnectionFactoryDependency):
    return SQLPersonRepository(factory=factory)


PersonRepositoryDependency = Annotated[repository.PersonRepository, Depends(
    create_person_repository)]


def create_contact_repository(factory: ConnectionFactoryDependency):
    return SQLContactRepository(factory=factory)


ContactRepositoryDependency = Annotated[repository.PersonContactRepository, Depends(
    create_contact_repository)]


def create_identification_repository(factory: ConnectionFactoryDependency):
    return SQLIdentificationRepository(factory=factory)


IdentificationRepositoryDependency = Annotated[repository.PersonIdentificationRepository, Depends(
    create_identification_repository)]

# --- SERVICE


def create_person_service(
        connection_manager_factory: ConnectionManagerDependency,
        transaction_manager_factory: TransactionManagerDependency,
        people: PersonRepositoryDependency,
        contacts: ContactRepositoryDependency,
        identifications: IdentificationRepositoryDependency,
        event_store: EventStoreDependency
):
    return DatabasePersonService(
        connection_manager_factory=connection_manager_factory,
        transaction_manager_factory=transaction_manager_factory,
        people=people,
        contacts=contacts,
        identifications=identifications,
        event_store=event_store)


PersonServiceDependency = Annotated[service.PersonService, Depends(
    create_person_service)]

# --- REQUEST


def create_person_request(
        user: UserInfo,
        details: requests.CreatePersonDetails = Body()
):
    return requests.CreatePersonRequest(
        user=user,
        details=details
    )


CreatePersonRequestDependency = Annotated[requests.CreatePersonRequest, Depends(
    create_person_request)]
