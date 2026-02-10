from dataclasses import dataclass
from datetime import datetime
from liceo.labs.sherlock.core import Aggregate, AggregateEvent
from .vo import FileMetadataId


@dataclass(init=False)
class FileMetadata(Aggregate[FileMetadataId]):
    @dataclass
    class CreateFileMetadataCommand:
        next_id: str
        filename: str
        path: str
        created_by: str

    @dataclass(kw_only=True)
    class FileMetadataCreated(AggregateEvent):
        event_type: str = "STORED_FILE_CREATED"
        filename: str
        created_by: str
        path: str

        def handle(self, aggregate: "FileMetadata"):
            aggregate.filename = self.filename
            aggregate.created_by = self.created_by
            aggregate.created_at = datetime.now()
            aggregate.path = self.path

    created_by: str
    created_at: datetime
    filename: str
    path: str

    @staticmethod
    def create(cmd: CreateFileMetadataCommand):
        return FileMetadata(id=FileMetadataId(id=cmd.next_id))\
            .append(
                FileMetadata.FileMetadataCreated(
                    filename=cmd.filename,
                    created_by=cmd.created_by,
                    path=cmd.path
                )
        )
