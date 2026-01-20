from abc import ABC, abstractmethod

from optiak.infra.domain.events import Event


class LedgerPort(ABC):
    # Aggregate
    @abstractmethod
    def persist(self, event: Event) -> None:
        pass


class TransactionalOutputPort(ABC):
    def __enter__(self):
        return self

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass


class TransactionalSupportOutputPort(ABC):
    @abstractmethod
    def create(self) -> TransactionalOutputPort:
        pass
