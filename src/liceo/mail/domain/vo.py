from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import AggregateId


@dataclass
class MailId(AggregateId):
    id: str
