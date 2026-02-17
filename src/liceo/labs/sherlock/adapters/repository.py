from json import dumps
from shortuuid import uuid
from liceo.labs.db.sql import SQLRepository
from liceo.labs.sherlock.domain.entities import AggregateEvent
from ..application.repository import EventStoreRepository


class SQLEventStoreRepository(EventStoreRepository, SQLRepository):
    def append_batched_events(self, events: list[AggregateEvent]) -> int:
        # preparing a batched execution
        param_list = [
            {
                "id": uuid(),
                "aggregate_id": event.aggregate_id,
                "aggregate_type": event.aggregate_type,
                "event_type": event.event_type,
                "created_at": event.created_at,
                "version": event.version,
                "data": dumps(event.unsecure_dict())
            } for event in events
        ]
        # using executemany semantics
        result = self._get_connection().execute(
            sql=self.resolve_sql(self.append_batched_events),
            params=param_list
        )
        return result.rowcount
