from abc import ABC, abstractmethod
from liceo.labs.sherlock.core import AggregateEvent, Aggregate


class LedgerPort(ABC):
    @abstractmethod
    def persist_event(self, event: AggregateEvent) -> None:
        pass

    @abstractmethod
    def persist(self, aggregate: Aggregate) -> None:
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


class TransactionManager(ABC):
    @abstractmethod
    def create(self) -> TransactionalOutputPort:
        pass
