from dataclasses import dataclass
from fastapi import status
from fastapi.responses import StreamingResponse, Response
from ..application.dtos import FileDTO, LoadedFileDTO


@dataclass
class UploadResponse:
    id: str

    @staticmethod
    def from_dto(dto: FileDTO):
        return UploadResponse(id=dto.id)


def from_dto_to_streaming_response(dto: LoadedFileDTO | None) -> Response:
    if not dto:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return StreamingResponse(
        dto.data,
        media_type=dto.content_type
    )
