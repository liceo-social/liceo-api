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


class Storage(ABC):
    @abstractmethod
    def write(self, key: str, data: Iterator[bytes]) -> None:
        pass

    @abstractmethod
    def read(
        self,
        key: str,
        chunk_size: int = 1024 * 1024,
    ) -> Iterator[bytes]:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass
