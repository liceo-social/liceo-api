from shortuuid import random
from liceo.labs.db.sql import SQLRepository, sql
from ..application.repository import FileMetadataRepository
from ..domain.entities import FileMetadata


def _to_file_metadata(row: dict) -> FileMetadata | None:
    if not row:
        return None
    metadata = FileMetadata(id=row["id"])
    metadata.filename = row["filename"]
    metadata.type = row["type"]
    metadata.path = row["path"]
    metadata.created_at = row["created_at"]
    metadata.created_by = row["created_by"]
    return metadata


class SQLFileMetadataRepository(FileMetadataRepository, SQLRepository):
    def save_file_metadata(self, file: FileMetadata) -> FileMetadata:
        self._get_connection().execute(
            self.resolve_sql(self.save_file_metadata),
            params={
                "id": file.id.id,
                "filename": file.filename,
                "type": file.type,
                "path": file.path,
                "created_by": file.created_by,
                "created_at": file.created_at
            })
        return file

    def generate_id(self) -> str:
        return random()

    @sql(_to_file_metadata)
    def find_by_id(self, id: str) -> FileMetadata | None:
        pass
