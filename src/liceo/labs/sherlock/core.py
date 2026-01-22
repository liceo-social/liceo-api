from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, List, Self, TypeVar

T = TypeVar("T")


@dataclass
class Sensitive(Generic[T]):
    value: T


@dataclass(kw_only=True)
class AggregateEvent(Generic[T], ABC):
    id: str = ""
    aggregate_id: str = ""
    event_type: str
    version: int = 0

    @abstractmethod
    def handle(self, aggregate: T) -> None:
        pass

    def unsecure_dict(self):
        unsecured = {}
        filtered = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ["id", "aggregate_id", "event_type", "version"]
        }
        for k, v in filtered.items():
            if type(v) is Sensitive:
                unsecured.update({k: v.value})
            else:
                unsecured.update({k: str(v)})

        return unsecured


class AggregateId:
    id: str


ID = TypeVar("ID", bound=AggregateId)


@dataclass
class Aggregate(Generic[ID]):
    id: ID
    _version: int = field(default=0)
    _events: List[AggregateEvent[Self]] = field(default_factory=list)

    def append(self, event: AggregateEvent[Self]):
        if not event.aggregate_id:
            if self.id:
                event.aggregate_id = self.id.id
            else:
                raise Exception("Can't add without aggregate id")

        event.handle(self)
        self._events.append(event)
        return self


@dataclass
class AggregateRoot:
    _version: int = field(default=0)
    _events: List[AggregateEvent] = field(default_factory=list)

    def append(self, event: AggregateEvent[Self]):
        event.handle(self)
        self._events.append(event)
        return self

    def append_child_aggregate_events(self, aggregate: "Aggregate | AggregateRoot"):
        for ev in aggregate._events:
            self._events.append(ev)
        return self
