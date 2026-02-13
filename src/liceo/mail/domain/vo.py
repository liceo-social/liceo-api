from dataclasses import dataclass
from liceo.labs.sherlock.core import AggregateId


@dataclass
class MailId(AggregateId):
    id: str
