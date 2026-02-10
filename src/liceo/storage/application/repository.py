from abc import ABC, abstractmethod
from ..domain.entities import FileMetadata


class FileMetadataRepository(ABC):
    @abstractmethod
    def generate_id(self) -> str:
        pass

    @abstractmethod
    def save_file_metadata(self, file: FileMetadata) -> FileMetadata:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> FileMetadata | None:
        pass
