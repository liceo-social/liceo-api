from typing import Annotated

from fastapi import Depends

from liceo.infra.adapters.persistence import SQLAlchemyConnectionFactory
from liceo.infra.domain.vo import LiceoConfiguration
from liceo.labs.db.core import ConnectionFactory, ConnectionManager, TransactionManager

from .migrations import MigrationLoader
from ..application.output import EventStore
from .event_store import ConsoleEventStore

# ------------ CONFIGURATION

ConfigurationDependency = Annotated[LiceoConfiguration,
                                    Depends(lambda: LiceoConfiguration())]

# ------------ DATABASE


def load_connection_factory(cfg: ConfigurationDependency) -> ConnectionFactory:
    return SQLAlchemyConnectionFactory(url=cfg.db.get_url())


ConnectionFactoryDependency = Annotated[ConnectionFactory, Depends(
    load_connection_factory)]


def create_connection_manager(connection_factory: ConnectionFactoryDependency):
    return ConnectionManager(connection_factory)


ConnectionManagerDependency = Annotated[ConnectionManager, Depends(
    create_connection_manager)]


def create_transaction_factory(connection_factory: ConnectionFactoryDependency):
    return TransactionManager(connection_factory)


TransactionManagerDependency = Annotated[TransactionManager, Depends(
    create_transaction_factory)]


def load_migration_loader(connection_factory: ConnectionFactoryDependency):
    return MigrationLoader(connection_factory)


MigrationsDependency = Annotated[MigrationLoader, Depends(load_migration_loader)]

# -------------- EVENT STORE


def event_store():
    return ConsoleEventStore()


EventStoreDependency = Annotated[EventStore, Depends(event_store)]
