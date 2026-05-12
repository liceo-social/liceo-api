from fastapi import UploadFile, Path, Depends
from pydantic import BaseModel
from typing import Annotated
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


class GetImageRequest(BaseModel):
    id: Annotated[str, Depends(Path())]
    downloaded_by: UserInfo

    def to_dto(self) -> LoadFileDTO:
        return LoadFileDTO(id=self.id, loaded_by=self.downloaded_by.id)
