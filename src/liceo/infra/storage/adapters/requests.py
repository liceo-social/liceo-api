from dataclasses import dataclass
from fastapi import UploadFile
from pydantic import BaseModel
from liceo.security.common.adapters.di import UserInfo
from ..application.dtos import SaveFileDTO, LoadFileDTO


class UploadRequest(BaseModel):
    file: UploadFile
    uploaded_by: UserInfo

    def to_dto(self) -> SaveFileDTO:
        return SaveFileDTO(
            data=self.file.file,
            filename=self.file.filename,
            file_type=self.file.content_type,
            created_by=self.uploaded_by.id
        )


class DownloadRequest(BaseModel):
    id: str
    downloaded_by: UserInfo

    def to_dto(self) -> LoadFileDTO:
        return LoadFileDTO(id=self.id, loaded_by=self.downloaded_by.id)
