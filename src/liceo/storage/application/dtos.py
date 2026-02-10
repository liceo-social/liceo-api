from dataclasses import dataclass
from typing import Iterator


@dataclass
class FileDTO:
    id: str
    filename: str
    file_type: str


@dataclass
class SaveFileDTO:
    data: Iterator[bytes]
    filename: str | None
    file_type: str | None
    created_by: str


@dataclass
class LoadFileDTO:
    id: str
    loaded_by: str


@dataclass
class LoadedFileDTO:
    data: Iterator[bytes]
    content_type: str


@dataclass
class DeleteFileDTO:
    id: str
    deleted_by: str
