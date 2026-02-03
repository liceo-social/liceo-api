from abc import ABC, abstractmethod
from shortuuid import uuid
from liceo.labs.sherlock.core import AggregateEvent, Aggregate


class EventStore(ABC):
    @abstractmethod
    def append_event(self, event: AggregateEvent) -> None:
        pass

    @abstractmethod
    def append(self, aggregate: Aggregate) -> None:
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


class AbstractRepository(ABC):
    def generate_id(self) -> str:
        return uuid()
