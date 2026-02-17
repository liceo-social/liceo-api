from fastapi import Depends
from typing import Annotated
from liceo.infra.adapters.di import (
    ConfigurationDependency,
    EventStoreDependency,
    TransactionManagerDependency,
    ConnectionManagerDependency,
    ConnectionFactoryDependency
)
from ..application.service import StorageService
from ..application.storage import Storage
from ..application.repository import FileMetadataRepository
from .storage import LocalStorage
from .service import LocalStorageService
from .repository import SQLFileMetadataRepository


def create_storage(config: ConfigurationDependency):
    return LocalStorage(configuration=config.file)


StorageDependency = Annotated[Storage, Depends(create_storage)]


def create_repository(connection_factory: ConnectionFactoryDependency):
    return SQLFileMetadataRepository(factory=connection_factory)


RepositoryDependency = Annotated[FileMetadataRepository, Depends(create_repository)]


def create_storage_service(
    repository: RepositoryDependency,
    event_store: EventStoreDependency,
    storage: StorageDependency,
    transaction_manager: TransactionManagerDependency,
    connection_manager: ConnectionManagerDependency
):
    return LocalStorageService(
        repository=repository,
        storage=storage,
        event_store=event_store,
        connection_manager_factory=connection_manager,
        transaction_manager_factory=transaction_manager,
    )


StorageServiceDependency = Annotated[StorageService, Depends(create_storage_service)]
