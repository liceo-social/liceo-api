from dataclasses import dataclass
from abc import abstractmethod
from liceo.labs.db.core import AbstractService
from typing import Iterator
from .dtos import SaveFileDTO, LoadFileDTO, LoadedFileDTO, DeleteFileDTO, FileDTO


@dataclass
class StorageService(AbstractService):
    @abstractmethod
    def save_file(self, dto: SaveFileDTO) -> FileDTO:
        pass

    @abstractmethod
    def load_file_info(self, dto: LoadFileDTO) -> FileDTO:
        pass

    @abstractmethod
    def load_file_content(self, dto: LoadFileDTO) -> LoadedFileDTO | None:
        pass

    @abstractmethod
    def delete_file(self, dto: DeleteFileDTO) -> None:
        pass
