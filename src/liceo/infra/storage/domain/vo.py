from dataclasses import dataclass
from liceo.labs.sherlock.core import AggregateId


@dataclass
class FileMetadataId(AggregateId):
    id: str
