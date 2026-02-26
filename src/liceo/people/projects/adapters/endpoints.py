from liceo.infra.adapters.rest.endpoints import RestGroupSpec, open_api_permissions
from liceo.security.common.adapters.di import has_permission
from . import di, permissions, responses

specs = RestGroupSpec(
    name="PROJECTS",
    path="/projects",
    description="Operations for managing projects",
)


router = specs.create_router()


@router.get(
    path="/",
    summary="Lists projects and could filter by name",
    dependencies=[has_permission(permissions.PROJECTS_LIST)],
    openapi_extra={**open_api_permissions([permissions.PROJECTS_LIST])}
)
def list(
    request: di.ListProjectsRequestDependency,
    service: di.ProjectServiceDependency
) -> responses.ListProjectsResponse:
    return responses.ListProjectsResponse.from_paged(service.filter_projects(request.to_dto()))


@router.post(
    path="/",
    summary="Adds a new project",
    dependencies=[has_permission(permissions.PROJECTS_CREATE)],
    openapi_extra={**open_api_permissions([permissions.PROJECTS_CREATE])}
)
def create(
    request: di.CreateProjectRequestDependency,
    service: di.ProjectServiceDependency
) -> responses.SimpleProjectResponse:
    return responses.SimpleProjectResponse.from_project(service.create_project(request.to_dto()))
