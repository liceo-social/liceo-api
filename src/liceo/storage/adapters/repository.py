from shortuuid import random
from liceo.labs.db.sql import SQLRepository
from ..application.repository import FileMetadataRepository
from ..domain.entities import FileMetadata


class SQLFileMetadataRepository(FileMetadataRepository, SQLRepository):
    def save_file_metadata(self, file: FileMetadata) -> FileMetadata:
        self._get_connection().execute(
            self.resolve_sql(self.save_file_metadata),
            params={
                "id": file.id.id,
                "filename": file.filename,
                "path": file.path,
                "created_by": file.created_by,
                "created_at": file.created_at
            })
        return file

    def generate_id(self) -> str:
        return random()
