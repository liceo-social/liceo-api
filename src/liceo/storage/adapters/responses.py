from dataclasses import dataclass
from fastapi.responses import StreamingResponse
from ..application.dtos import FileDTO


@dataclass
class UploadResponse:
    id: str

    @staticmethod
    def from_dto(dto: FileDTO):
        return UploadResponse(id=dto.id)


def from_dto_to_streaming_response(dto):
    return StreamingResponse(
        None,
        media_type="image/png",
        headers={
            "Cache-Control": 'private, max-age={cache_max_age}'
        }
    )
