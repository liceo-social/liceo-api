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
) -> responses.ProjectResponse:
    return responses.ProjectResponse.from_project(service.create_project(request.to_dto()))


@router.post(
    path="/{id}/memberships/{person_id}",
    summary="Adds a person membership to the project",
    dependencies=[has_permission(permissions.PROJECTS_ADD_MEMBERSHIP)],
    openapi_extra={**open_api_permissions([permissions.PROJECTS_ADD_MEMBERSHIP])}
)
def add_member(
    request: di.AddMemberToProjectRequestDependency,
    service: di.ProjectServiceDependency
) -> responses.ProjectMembershipResponse | None:
    return responses.ProjectMembershipResponse.from_project_membership(service.add_new_member(request.to_dto()))


@router.post(
    path="/{id}/coordinators/{user_id}",
    summary="Adds a coordinator to the project",
    dependencies=[has_permission(permissions.PROJECTS_ADD_COORDINATOR)],
    openapi_extra={**open_api_permissions([permissions.PROJECTS_ADD_COORDINATOR])}
)
def add_coordinator(
    request: di.AddCoordinatorRequestDependency,
    service: di.ProjectServiceDependency
) -> responses.ProjectCoordinatorResponse | None:
    return responses.ProjectCoordinatorResponse.from_coordinator(service.add_coordinator(request.to_dto()))


@router.post(
    path="/query/coordinators-by-projects",
    summary="Query to get a distinct limited number of coordinators in the projects passed",
    dependencies=[has_permission(permissions.PROJECTS_QUERY_COORDINATORS_BY_PROJECTS)],
    openapi_extra={
        **open_api_permissions([permissions.PROJECTS_QUERY_COORDINATORS_BY_PROJECTS])}
)
def find_all_coordinators_by_project_ids(
    request: di.FindAllCoordinatorsByProjectsRequestDependency,
    service: di.ProjectServiceDependency
) -> responses.ListProjectsCoordinatorsResponse:
    return responses.ListProjectsCoordinatorsResponse.from_paged(
        service.find_all_coordinators_by_project_ids(request.to_dto())
    )
