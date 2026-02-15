from json import dumps
from shortuuid import uuid
from datetime import datetime
from liceo.labs.db.sql import SQLRepository
from liceo.labs.sherlock.domain.entities import AggregateEvent
from ..application.repository import EventStoreRepository


class SQLEventStoreRepository(EventStoreRepository, SQLRepository):
    def append_event(self, event: AggregateEvent) -> None:
        self._get_connection().execute(
            self.resolve_sql(self.append_event),
            params={
                "id": uuid(),
                "aggregate_id": event.aggregate_id,
                "aggregate_type": event.aggregate_type,
                "event_type": event.event_type,
                "when": event.when,
                "version": event.version,
                "data": dumps(event.unsecure_dict()),
                "created_at": datetime.now()
            }
        )
