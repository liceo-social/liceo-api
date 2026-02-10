from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Iterator
from .dtos import SaveFileDTO, LoadFileDTO, DeleteFileDTO, FileDTO


@dataclass
class StorageService(ABC):
    @abstractmethod
    def save_file(self, dto: SaveFileDTO) -> FileDTO:
        pass

    @abstractmethod
    def load_file_info(self, dto: LoadFileDTO) -> FileDTO:
        pass

    @abstractmethod
    def load_file_content(self, dto: LoadFileDTO) -> Iterator[bytes]:
        pass

    @abstractmethod
    def delete_file(self, dto: DeleteFileDTO) -> None:
        pass
