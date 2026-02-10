from fastapi import UploadFile, Path
from liceo.infra.adapters.rest.endpoints import RestGroupSpec, open_api_permissions
from liceo.security.common.adapters.di import has_permission, UserInfo
from fastapi.responses import Response
from .di import StorageServiceDependency
from .permissions import STORAGE_UPLOAD, STORAGE_DOWNLOAD
from .requests import UploadRequest, GetImageRequest
from .responses import UploadResponse, from_dto_to_streaming_response

specs = RestGroupSpec(
    name="STORAGE",
    path="/storage",
    description="Operations for managing files",
)

router = specs.create_router()


@router.post(
    path="/upload",
    summary="Allows users to upload a file",
    dependencies=[has_permission(STORAGE_UPLOAD)],
    openapi_extra={**open_api_permissions([STORAGE_UPLOAD])}
)
def upload(
    file: UploadFile,
    user_info: UserInfo,
    service: StorageServiceDependency
) -> UploadResponse:
    return UploadResponse.from_dto(service.save_file(UploadRequest(file=file, uploaded_by=user_info).to_dto()))


@router.get(
    path="/images/{id}",
    summary="Allows users to download images by id",
    dependencies=[has_permission(STORAGE_DOWNLOAD)],
    openapi_extra={**open_api_permissions([STORAGE_DOWNLOAD])}
)
def download(
    downloaded_by: UserInfo,
    service: StorageServiceDependency,
    id: str = Path(),
) -> Response:
    return from_dto_to_streaming_response(
        service.load_file_content(
            GetImageRequest(
                id=id,
                downloaded_by=downloaded_by
            ).to_dto()
        )
    )
