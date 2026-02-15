from abc import ABC, abstractmethod
from ..domain import entities


class EventStoreRepository(ABC):
    @abstractmethod
    def append_event(self, event: entities.AggregateEvent) -> None:
        pass
