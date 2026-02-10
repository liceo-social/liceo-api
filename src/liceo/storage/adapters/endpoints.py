from fastapi import UploadFile
from liceo.infra.adapters.rest.endpoints import RestGroupSpec, open_api_permissions
from liceo.security.common.adapters.di import has_permission, UserInfo
from fastapi.responses import StreamingResponse
from .di import StorageServiceDependency
from .permissions import STORAGE_UPLOAD, STORAGE_DOWNLOAD
from .requests import UploadRequest, DownloadRequest
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
    userInfo: UserInfo,
    service: StorageServiceDependency
) -> UploadResponse:
    return UploadResponse.from_dto(service.save_file(UploadRequest(file=file, uploaded_by=userInfo).to_dto()))


@router.get(
    path="/download/{id}",
    summary="Allows users to download files by id",
    dependencies=[has_permission(STORAGE_DOWNLOAD)],
    openapi_extra={**open_api_permissions([STORAGE_DOWNLOAD])}
)
def download(
    request: DownloadRequest,
    service: StorageServiceDependency
) -> StreamingResponse:
    return from_dto_to_streaming_response(service.load_file_content(request.to_dto()))
