from dataclasses import dataclass
from typing import Iterator
from filetype import filetype
from liceo.infra.application.output import EventStore
from liceo.infra.storage.application.dtos import FileDTO, LoadFileDTO, SaveFileDTO
from liceo.labs.db.core import managed_service, AbstractService, transactional
from ..application.service import StorageService
from ..application.repository import FileMetadataRepository
from ..application.storage import Storage
from ..application.dtos import FileDTO, DeleteFileDTO
from ..domain.entities import FileMetadata


@dataclass
@managed_service
class LocalStorageService(StorageService, AbstractService):
    storage: Storage
    repository: FileMetadataRepository
    event_store: EventStore

    @transactional()
    def save_file(self, dto: SaveFileDTO) -> FileDTO:
        file_type = filetype.guess(dto.data)

        if file_type is None:
            raise Exception("No supported file type!")

        file_id = self.repository.generate_id()
        file_name = dto.filename if dto.filename else f"{file_id}.{file_type.extension}"
        file_path = self.storage.write(key=file_name, data=dto.data)

        file_metadata = FileMetadata.create(FileMetadata.CreateFileMetadataCommand(
            next_id=file_id,
            filename=file_name,
            path=file_path,
            created_by=dto.created_by
        ))

        saved_metadata = self.repository.save_file_metadata(file_metadata)
        self.event_store.append(saved_metadata)

        return FileDTO(
            id=saved_metadata.id.id,
            filename=saved_metadata.filename,
            file_type=file_type.mime
        )

    def load_file_content(self, dto: LoadFileDTO) -> Iterator[bytes]:
        return super().load_file_content(dto)

    def load_file_info(self, dto: LoadFileDTO) -> FileDTO:
        raise Exception("Not implemented yet")

    def delete_file(self, dto: DeleteFileDTO) -> None:
        raise Exception("Not implemented yet")
