from typing import Iterator
from abc import ABC, abstractmethod
from shortuuid import uuid
from typing import AsyncIterator
from liceo.labs.sherlock.core import AggregateEvent, Aggregate


class EventStore(ABC):
    @abstractmethod
    def append_event(self, event: AggregateEvent) -> None:
        pass

    @abstractmethod
    def append(self, aggregate: Aggregate) -> None:
        pass


class AbstractRepository(ABC):
    def generate_id(self) -> str:
        return uuid()
