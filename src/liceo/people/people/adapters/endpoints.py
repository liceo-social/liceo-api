from liceo.infra.adapters.rest.endpoints import RestGroupSpec, open_api_permissions
from liceo.security.common.adapters.di import has_permission
from . import di, permissions, responses

specs = RestGroupSpec(
    name="PEOPLE",
    path="/people",
    description="Operations for managing people",
)


router = specs.create_router()


@router.post(
    path="/",
    summary="Adds a new person",
    dependencies=[has_permission(permissions.PEOPLE_CREATE)],
    openapi_extra={**open_api_permissions([permissions.PEOPLE_CREATE])}
)
def create(
    request: di.CreatePersonRequestDependency,
    service: di.PersonServiceDependency
) -> responses.CreatePersonResponse | None:
    responses.CreatePersonResponse.from_person(service.save_person(request.to_dto()))
