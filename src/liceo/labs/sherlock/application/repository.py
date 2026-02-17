from abc import ABC, abstractmethod
from ..domain import entities


class EventStoreRepository(ABC):
    @abstractmethod
    def append_batched_events(self, events: list[entities.AggregateEvent]) -> int:
        pass
