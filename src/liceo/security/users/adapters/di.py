from typing import Annotated
from fastapi import Depends
from liceo.infra.adapters.ledger import LedgerPort, ConsoleLedger
from liceo.infra.adapters.persistence import TransactionManager, DummyTransactionManager
from .repositories import MemoryRepository
from ..application.services.create_user_service import CreateUserService

# ----- COMMON


def create_ledger():
    return ConsoleLedger()


LedgerDependency = Annotated[LedgerPort, Depends(create_ledger)]

TransactionManagerDependency = Annotated[TransactionManager, Depends(
    DummyTransactionManager)]


# ----- REPOSITORIES


def create_repository() -> MemoryRepository:
    return MemoryRepository()


RepositoryDependency = Annotated[MemoryRepository, Depends(create_repository)]


# ---- SERVICES

def create_user_service_dependency(repository: RepositoryDependency, ledger: LedgerDependency, tx_manager: TransactionManagerDependency) -> CreateUserService:
    return CreateUserService(repository=repository, ledger=ledger, tx_manager=tx_manager)


CreateUserServiceDependency = Annotated[CreateUserService, Depends(
    create_user_service_dependency)]
