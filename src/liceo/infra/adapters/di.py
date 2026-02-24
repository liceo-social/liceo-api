from typing import Annotated
from fastapi import Depends

from liceo.infra.adapters.persistence import SQLAlchemyConnectionFactory
from liceo.infra.domain.vo import LiceoConfiguration
from liceo.labs.db.core import ConnectionFactory, ConnectionManagerFactory, TransactionManagerFactory
from liceo.labs.sherlock.application.service import EventStoreService
from liceo.labs.sherlock.application.repository import EventStoreRepository
from liceo.labs.sherlock.adapters.service import DatabaseEventStoreService
from liceo.labs.sherlock.adapters.repository import SQLEventStoreRepository

from .migrations import MigrationLoader

# ------------ CONFIGURATION

ConfigurationDependency = Annotated[LiceoConfiguration,
                                    Depends(lambda: LiceoConfiguration())]

# ------------ DATABASE


def load_connection_factory(cfg: ConfigurationDependency) -> ConnectionFactory:
    return SQLAlchemyConnectionFactory(database_config=cfg.db)


ConnectionFactoryDependency = Annotated[ConnectionFactory, Depends(
    load_connection_factory)]


def create_connection_manager(connection_factory: ConnectionFactoryDependency):
    return ConnectionManagerFactory(connection_factory)


ConnectionManagerDependency = Annotated[ConnectionManagerFactory, Depends(
    create_connection_manager)]


def create_transaction_factory(connection_factory: ConnectionFactoryDependency):
    return TransactionManagerFactory(connection_factory)


TransactionManagerDependency = Annotated[TransactionManagerFactory, Depends(
    create_transaction_factory)]


def load_migration_loader(connection_factory: ConnectionFactoryDependency):
    return MigrationLoader(connection_factory)

# -------------- DATABASE - MIGRATIONS


MigrationsDependency = Annotated[MigrationLoader, Depends(load_migration_loader)]

# -------------- EVENT STORE


def event_store_repository(
        factory: ConnectionFactoryDependency
) -> EventStoreRepository:
    return SQLEventStoreRepository(factory=factory)


EventStoreRepositoryDependency = Annotated[EventStoreRepository, Depends(
    event_store_repository)]


def event_store(
        transaction_manager: TransactionManagerDependency,
        connection_manager: ConnectionManagerDependency,
        repository: EventStoreRepositoryDependency,
) -> EventStoreService:
    return DatabaseEventStoreService(
        transaction_manager_factory=transaction_manager,
        connection_manager_factory=connection_manager,
        events=repository
    )


EventStoreDependency = Annotated[EventStoreService, Depends(event_store)]
